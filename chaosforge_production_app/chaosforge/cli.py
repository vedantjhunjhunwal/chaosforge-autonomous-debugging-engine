import argparse, json
import uvicorn
from sqlalchemy.orm import Session
from chaosforge.db.session import SessionLocal, Base, engine as db_engine
from chaosforge.db.models import User, Run
from chaosforge.security import get_password_hash, verify_password, create_access_token
from chaosforge.core.contracts import load_contract
from chaosforge.core.engine import ChaosForgeEngine

def main():
    parser = argparse.ArgumentParser(prog="chaosforge")
    sub = parser.add_subparsers(dest="cmd", required=True)

    serve = sub.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)

    cu = sub.add_parser("create-user")
    cu.add_argument("--email", required=True)
    cu.add_argument("--password", required=True)
    cu.add_argument("--name", default="")

    login = sub.add_parser("login")
    login.add_argument("--email", required=True)
    login.add_argument("--password", required=True)

    run = sub.add_parser("run")
    run.add_argument("--contract", required=True)
    run.add_argument("--runs", type=int, default=100)
    run.add_argument("--concurrency", type=int, default=8)
    run.add_argument("--email", default="")
    run.add_argument("--password", default="")
    run.add_argument("--no-auth", action="store_true")

    ls = sub.add_parser("list-runs")

    args = parser.parse_args()
    Base.metadata.create_all(bind=db_engine)

    if args.cmd == "serve":
        uvicorn.run("chaosforge.api.app:app", host=args.host, port=args.port, reload=False)
    elif args.cmd == "create-user":
        db=SessionLocal();
        try:
            if db.query(User).filter(User.email==args.email).first():
                print("User already exists"); return
            user=User(email=args.email, name=args.name or args.email.split('@')[0], hashed_password=get_password_hash(args.password))
            db.add(user); db.commit(); print(f"Created user {args.email}")
        finally: db.close()
    elif args.cmd == "login":
        db=SessionLocal();
        try:
            user=db.query(User).filter(User.email==args.email).first()
            if not user or not verify_password(args.password, user.hashed_password):
                raise SystemExit("Invalid credentials")
            print(create_access_token({"sub": user.email}))
        finally: db.close()
    elif args.cmd == "run":
        contract=load_contract(args.contract)
        db=SessionLocal();
        try:
            user=None
            if not args.no_auth:
                user = db.query(User).filter(User.email==args.email).first() if args.email else None
                if args.email and (not user or not verify_password(args.password, user.hashed_password)):
                    raise SystemExit("Invalid credentials. Use --no-auth for local demo runs.")
            cf_engine=ChaosForgeEngine(db)
            run=cf_engine.create_run(contract, user.id if user else None)
            report=cf_engine.execute_run(run.id, contract, args.runs, args.concurrency)
            print(json.dumps(report, indent=2))
        finally: db.close()
    elif args.cmd == "list-runs":
        db=SessionLocal();
        try:
            for r in db.query(Run).order_by(Run.created_at.desc()).limit(20).all():
                print(f"{r.id} {r.status} {r.target_name} {r.crash_type} {r.ci_passes}/{r.ci_total} {r.artifact_dir}")
        finally: db.close()
