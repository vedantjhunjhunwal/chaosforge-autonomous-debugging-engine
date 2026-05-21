from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from chaosforge.db.session import get_db
from chaosforge.db.models import User, Run
from chaosforge.security import verify_password, create_access_token, get_password_hash
from chaosforge.schemas import LoginRequest, TokenResponse, RunCreate, RunResponse, TargetContract
from chaosforge.api.deps import current_user
from chaosforge.core.engine import ChaosForgeEngine

app = FastAPI(title="ChaosForge", version="1.0.0")
templates = Jinja2Templates(directory="chaosforge/web/templates")
app.mount("/static", StaticFiles(directory="chaosforge/web/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    runs = db.query(Run).order_by(Run.created_at.desc()).limit(25).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "runs": runs})

@app.post("/api/auth/register", response_model=TokenResponse)
def register(req: LoginRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(409, "User already exists")
    user = User(email=req.email, name=req.email.split("@")[0], hashed_password=get_password_hash(req.password))
    db.add(user); db.commit()
    return TokenResponse(access_token=create_access_token({"sub": user.email}))

@app.post("/api/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    return TokenResponse(access_token=create_access_token({"sub": user.email}))

@app.get("/api/runs", response_model=list[RunResponse])
def list_runs(user: User = Depends(current_user), db: Session = Depends(get_db)):
    runs = db.query(Run).order_by(Run.created_at.desc()).limit(100).all()
    return [RunResponse(id=r.id, status=r.status, target_name=r.target_name, crash_found=r.crash_found, crash_type=r.crash_type, mapped_location=r.mapped_location, ci_passes=r.ci_passes, ci_total=r.ci_total, artifact_dir=r.artifact_dir, error=r.error) for r in runs]

@app.post("/api/runs", response_model=RunResponse)
def create_run(req: RunCreate, background: BackgroundTasks, user: User = Depends(current_user), db: Session = Depends(get_db)):
    engine = ChaosForgeEngine(db)
    run = engine.create_run(req.contract, user.id)
    background.add_task(run_in_background, run.id, req.contract, req.runs, req.concurrency)
    return RunResponse(id=run.id, status=run.status, target_name=run.target_name, crash_found=run.crash_found, artifact_dir=run.artifact_dir)

def run_in_background(run_id: str, contract: TargetContract, runs: int, concurrency: int):
    from chaosforge.db.session import SessionLocal
    db = SessionLocal()
    try:
        ChaosForgeEngine(db).execute_run(run_id, contract, runs, concurrency)
    finally:
        db.close()

@app.get("/api/runs/{run_id}", response_model=RunResponse)
def get_run(run_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    r = db.get(Run, run_id)
    if not r: raise HTTPException(404, "Run not found")
    return RunResponse(id=r.id, status=r.status, target_name=r.target_name, crash_found=r.crash_found, crash_type=r.crash_type, mapped_location=r.mapped_location, ci_passes=r.ci_passes, ci_total=r.ci_total, artifact_dir=r.artifact_dir, error=r.error)

@app.get("/api/runs/{run_id}/artifact/{name}")
def get_artifact(run_id: str, name: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    r = db.get(Run, run_id)
    if not r: raise HTTPException(404, "Run not found")
    path = __import__('pathlib').Path(r.artifact_dir) / name
    if not path.exists(): raise HTTPException(404, "Artifact not found")
    return FileResponse(path)
