# Occupancy AI Agent — LangGraph Workplace Occupancy Intelligence Platform

> A full-stack AI occupancy intelligence product that uses YOLO computer vision, spatial person-chair reasoning, temporal smoothing, LangGraph-orchestrated AI agents, and optional LLM insights to convert workplace videos into occupancy events, annotated outputs, CSV metrics, and executive-ready reports.

---

## What is Occupancy AI Agent?

Occupancy AI Agent is a **computer vision + AI agent platform for workplace seat occupancy analytics**.

In simple words:

Imagine an office, classroom, meeting room, lab, or shared workspace where you want to know:

1. Which chairs are being used?
2. When did a person sit down?
3. How long was each chair occupied?
4. Which detections look reliable?
5. Which results need review?
6. What does the occupancy pattern mean for a non-technical user?

Normally, an engineer or analyst would have to:

1. Run a computer vision model manually.
2. Detect people and chairs.
3. Check overlap frame by frame.
4. Smooth noisy detections.
5. Export CSV files.
6. Review errors manually.
7. Explain results to business teams.
8. Create reports for managers.

Occupancy AI Agent automates this workflow.

It acts like an intelligent occupancy-analysis teammate that can:

- Detect chairs from video.
- Detect people using YOLO segmentation.
- Learn static chair locations.
- Track person-chair interaction over time.
- Apply temporal smoothing to reduce noisy switching.
- Generate annotated output videos.
- Produce occupancy summary CSV files.
- Produce frame-level metrics CSV files.
- Run LangGraph AI agents over the generated evidence.
- Diagnose failures and low-quality outputs.
- Detect anomalies and unstable occupancy behavior.
- Recommend threshold tuning without changing the core algorithm.
- Generate human-readable reports.
- Optionally use Gemini/OpenAI-compatible LLMs for executive insights.

This project is designed as an **AI Agent + Computer Vision + Full-Stack Product + Workplace Analytics project**.

---

## Why This Project Matters

Modern workplaces need better space utilization.

Poor occupancy visibility can cause:

- Unused office space
- Overcrowded seating zones
- Inefficient facility planning
- Manual seat audits
- Inaccurate workplace utilization reports
- Poor meeting-room and classroom planning
- Lack of real-time decision support

A basic computer vision script only detects objects.

Occupancy AI Agent goes further.

It connects real video processing with an AI-agent reliability layer:

- YOLO-based visual perception
- Chair-layout calibration
- Person-chair spatial reasoning
- Temporal smoothing
- Event logging
- Quality scoring
- Anomaly detection
- Failure diagnosis
- Threshold recommendation
- LLM-powered explanation
- Full-stack upload and dashboard workflow

This makes the project closer to a real AI engineering product, not just a notebook or demo script.

---

## Core Idea

```text
Input Workplace Video
        ↓
YOLO Segmentation Engine
        ↓
Chair Layout Calibration
        ↓
Person Detection Per Frame
        ↓
Person-Chair Spatial Reasoning
        ↓
Temporal Smoothing
        ↓
Occupancy Event Logging
        ↓
CSV Metrics + Output Video
        ↓
LangGraph AI Agent Workflow
        ↓
Quality Score + Diagnosis + Anomaly Insights + LLM Report
        ↓
Full-Stack Dashboard
```

Occupancy AI Agent does not blindly ask an LLM to detect occupancy.

The core occupancy decision is handled by deterministic computer vision logic:

1. Detect static chairs.
2. Detect people.
3. Check person-chair overlap.
4. Filter false sitting cases.
5. Apply temporal smoothing.
6. Log state changes.

The LangGraph agent layer runs after the vision pipeline and reviews the generated evidence.

---

## Architecture

```text
 [ User Uploads Video from Flask Dashboard ]
                         │
                         ▼
 ┌───────────────────────────────────────────────────────┐
 │ Flask Full-Stack App                                  │
 │ apps.py + HTML templates + CSS dashboard              │
 └───────────────────────┬───────────────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────────────┐
 │ Pipeline Controller                                   │
 │ Creates job, stores upload, starts background worker   │
 └───────────────────────┬───────────────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────────────┐
 │ YOLO Occupancy Engine                                 │
 │ Loads model, detects chairs and people, processes video│
 └───────────────────────┬───────────────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────────────┐
 │ Chair Calibration                                     │
 │ Learns static chair layout from initial frames         │
 └───────────────────────┬───────────────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────────────┐
 │ Spatial + Temporal Occupancy Logic                    │
 │ Person-chair overlap + behind-person filtering +      │
 │ temporal smoothing                                    │
 └───────────────────────┬───────────────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────────────┐
 │ Output Artifacts                                      │
 │ Annotated video, summary CSV, frame-level metrics CSV  │
 └───────────────────────┬───────────────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────────────┐
 │ LangGraph Multi-Agent Workflow                        │
 │                                                       │
 │ START                                                 │
 │   ↓                                                   │
 │ Diagnosis Agent                                       │
 │   ↓                                                   │
 │ Quality Check Agent                                   │
 │   ↓                                                   │
 │ Threshold Advisor Agent                               │
 │   ↓                                                   │
 │ Anomaly Detection Agent                               │
 │   ↓                                                   │
 │ Report Generation Agent                               │
 │   ↓                                                   │
 │ Optional LLM Insight Agent                            │
 │   ↓                                                   │
 │ Final Report Builder                                  │
 │   ↓                                                   │
 │ END                                                   │
 └───────────────────────┬───────────────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────────────┐
 │ Dashboard Results                                     │
 │ Video preview, downloads, reports, status, findings    │
 └───────────────────────────────────────────────────────┘
```

---

## Technical Stack

| Area | Technology |
|---|---|
| Computer Vision | YOLO11 Segmentation / Ultralytics |
| Video Processing | OpenCV |
| Core Language | Python |
| Agent Orchestration | LangGraph |
| Agent State / Schemas | Python dataclasses / typed schemas |
| LLM Insight Layer | Optional Gemini or OpenAI-compatible API |
| Backend / Web App | Flask |
| Frontend | HTML, CSS, Jinja Templates |
| Data Processing | Pandas, NumPy |
| Database | SQLite |
| Reports | JSON + Markdown |
| Testing | pytest |
| Deployment | Local Python, Docker-ready structure |
| CLI | argparse-based runner |

---

## What the Project Detects

The system detects whether chairs are occupied in a workplace video.

The core occupancy logic checks:

- Chair locations
- Person bounding boxes
- Person masks when available
- Person center position relative to chair
- Person bottom position relative to chair bottom
- Intersection over chair area
- Temporal stability across frames

Example decision flow:

```text
Person detected
      ↓
Person center lies inside chair width?
      ↓
Person is not behind the chair?
      ↓
Person overlaps enough chair area?
      ↓
Temporal counter crosses threshold?
      ↓
Chair marked occupied
```

The LLM does not decide whether a chair is occupied.

The LLM only explains results after the deterministic vision engine has finished.

---

## LangGraph Agent Workflow

The project uses a LangGraph workflow to review the output of the computer vision engine.

```text
START
  ↓
Diagnosis Agent
  ↓
Quality Check Agent
  ↓
Threshold Advisor Agent
  ↓
Anomaly Detection Agent
  ↓
Report Generation Agent
  ↓
Optional LLM Insight Agent
  ↓
Final Report Builder
END
```

### 1. Diagnosis Agent

Checks whether the pipeline produced valid outputs.

It can identify issues such as:

- No chairs detected
- No occupancy events generated
- Missing output video
- Missing summary CSV
- Missing metrics CSV
- Processing failure

---

### 2. Quality Check Agent

Scores the reliability of the run.

It reviews:

- Number of processed frames
- Chair count
- Occupancy event count
- Available metrics
- Output artifact completeness
- Warning and failure patterns

---

### 3. Threshold Advisor Agent

Provides advisory recommendations for threshold tuning.

It does not automatically mutate the core algorithm.

It can recommend reviewing:

- Intersection ratio threshold
- Temporal smoothing threshold
- Confidence threshold
- Calibration window

This keeps the product reliable and explainable.

---

### 4. Anomaly Detection Agent

Finds unusual output behavior.

Examples:

- Chair always occupied
- Chair never occupied
- Too many rapid state switches
- Empty metrics despite successful processing
- Very low occupancy activity
- Possible occlusion or camera-angle issue

---

### 5. Report Generation Agent

Generates structured findings for human review.

The report includes:

- Quality score
- Executive summary
- Agent findings
- Recommendations
- Output artifact paths

---

### 6. Optional LLM Insight Agent

When enabled, the LLM agent converts technical metrics into a human-readable business summary.

It can explain:

- What happened in the video
- Whether the result looks reliable
- Which chairs had unusual behavior
- What a facilities or operations team should review
- What the system did not prove

The LLM is optional.

If no API key is provided, the system still runs with deterministic agents.

---

## Project Features

### 1. Full-Stack Flask Dashboard

Run the app and upload videos from a browser.

The dashboard supports:

- Video upload
- Model path input
- Job tracking
- Status view
- Output video preview
- CSV downloads
- Agent report downloads
- Error display

---

### 2. YOLO-Based Occupancy Detection

The core engine uses YOLO segmentation to detect:

- People
- Chairs

It then applies spatial and temporal logic to detect occupancy events.

---

### 3. Static Chair Layout Learning

The system learns chair positions from the initial video frames.

This allows the system to track fixed seating layouts instead of repeatedly treating every detection as a new chair.

---

### 4. Person-Chair Spatial Reasoning

The project checks whether a detected person is actually interacting with a chair.

It avoids simple object detection mistakes by checking:

- Horizontal chair alignment
- Person bottom position
- Mask overlap when available
- Bounding-box overlap fallback

---

### 5. Temporal Smoothing

Real video detections can flicker.

The system uses temporal counters to avoid marking a chair occupied or empty from a single noisy frame.

---

### 6. Output Video Generation

The app creates an annotated output video showing:

- Chair boxes
- Person boxes
- Occupied/unoccupied visual states

This helps users visually verify the result.

---

### 7. CSV Metrics and Summary Reports

The system generates:

```text
storage/outputs/<run_id>.mp4
storage/outputs/<run_id>_summary.csv
storage/outputs/<run_id>_metrics.csv
storage/reports/<run_id>_agent_report.json
storage/reports/<run_id>_agent_report.md
```

The summary CSV stores occupancy sessions.

The metrics CSV stores frame-level evidence such as IoU, IoCA, chair ID, and occupancy status.

---

### 8. Optional LLM-Powered Executive Insights

The LLM agent can be enabled through environment variables.

Supported modes:

- Gemini
- OpenAI-compatible endpoint

The LLM does not replace YOLO or the algorithm.

It only summarizes and explains the output evidence.

---

## How to Run Locally on Windows

### Step 1: Clone the repository

```cmd
git clone https://github.com/YOUR_USERNAME/occupancy-ai-agent-langgraph.git
cd occupancy-ai-agent-langgraph
```

If you are using the downloaded ZIP, open PowerShell inside the folder that contains:

```text
apps.py
requirements.txt
core/
agents/
templates/
static/
```

---

### Step 2: Create virtual environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

---

### Step 3: Install dependencies

```cmd
python -m pip install --upgrade pip setuptools wheel
python -m pip install --no-cache-dir -r requirements.txt
```

If your environment gives dependency issues, use the minimal requirements file:

```cmd
python -m pip install --no-cache-dir -r requirements-minimal.txt
```

---

### Step 4: Install OpenCV if needed

If you see:

```text
ModuleNotFoundError: No module named 'cv2'
```

Run:

```cmd
python -m pip install opencv-python
```

---

### Step 5: Download or select a YOLO model

Recommended for laptops:

```text
yolo11n-seg.pt
```

This is smaller and easier to run than:

```text
yolo11x-seg.pt
```

Create a models folder:

```cmd
mkdir models
```

Place your model here:

```text
models/yolo11n-seg.pt
```

If the automatic download fails, manually download the model in your browser and put it inside the `models/` folder.

---

### Step 6: Run the Flask full-stack app

```cmd
python apps.py
```

Open:

```text
http://127.0.0.1:5000
```

Upload a video from the dashboard.

In the model path field, use:

```text
models/yolo11n-seg.pt
```

or:

```text
yolo11n-seg.pt
```

---

## How to Run From CLI

You can also run without the browser.

Put your video here:

```text
storage/uploads/input.mp4
```

Run:

```cmd
python run.py --video storage\uploads\input.mp4 --model models\yolo11n-seg.pt --output storage\outputs\result.mp4
```

Expected outputs:

```text
storage/outputs/result.mp4
storage/outputs/result_summary.csv
storage/outputs/result_metrics.csv
storage/reports/<run_id>_agent_report.json
storage/reports/<run_id>_agent_report.md
```

---

## How to Enable the LLM Agent

The project works without an LLM.

To enable the Gemini LLM Insight Agent on Windows PowerShell:

```powershell
$env:OCCUPANCY_LLM_ENABLED="true"
$env:OCCUPANCY_LLM_PROVIDER="gemini"
$env:OCCUPANCY_LLM_MODEL="gemini-1.5-flash"
$env:GEMINI_API_KEY="your_gemini_api_key_here"
python apps.py
```

To enable an OpenAI-compatible LLM:

```powershell
$env:OCCUPANCY_LLM_ENABLED="true"
$env:OCCUPANCY_LLM_PROVIDER="openai"
$env:OCCUPANCY_LLM_MODEL="gpt-4o-mini"
$env:OPENAI_API_KEY="your_openai_api_key_here"
python apps.py
```

If no key is provided, the deterministic LangGraph agents still run.

---

## Running the Dashboard

```cmd
python apps.py
```

Open:

```text
http://127.0.0.1:5000
```

The dashboard lets you:

- Upload a video
- Enter a YOLO model path
- Start processing
- View job status
- Preview the output video
- Download CSV files
- Download AI agent reports

---

## Running Tests

```cmd
pytest -q
```

Expected result:

```text
4 passed
```

---

## Generated Artifacts

Each run creates output files inside:

```text
storage/outputs/
storage/reports/
```

Important files:

```text
<run_id>.mp4
<run_id>_summary.csv
<run_id>_metrics.csv
<run_id>_agent_report.json
<run_id>_agent_report.md
```

The most important files are:

```text
output video
summary CSV
agent_report.md
```

These prove that the system executed the video pipeline and produced human-reviewable AI agent artifacts.

---

## Example Workflow Output

```text
upload_video → Video stored in storage/uploads
create_job → Job saved in SQLite
run_occupancy_pipeline → Vision pipeline started
load_yolo_model → YOLO segmentation model loaded
calibrate_chairs → Static chair layout learned
process_frames → Person-chair occupancy logic executed
save_outputs → Video and CSV artifacts saved
run_langgraph_agents → Agent workflow executed
generate_report → Markdown and JSON reports created
dashboard_preview → Results shown in browser
```

Final status:

```text
completed
```

---

## Repository Structure

```text
occupancy-ai-agent-langgraph/
│
├── apps.py
├── run.py
├── requirements.txt
├── requirements-minimal.txt
├── README.md
├── Dockerfile
├── docker-compose.yml
├── INSTALL_WINDOWS.md
├── LANGGRAPH_ARCHITECTURE.md
│
├── app/
│   ├── db.py
│   ├── main.py
│   └── pipeline.py
│
├── core/
│   ├── config.py
│   ├── exceptions.py
│   ├── occupancy_analyzer.py
│   └── schemas.py
│
├── agents/
│   ├── orchestrator.py
│   ├── diagnosis_agent.py
│   ├── quality_agent.py
│   ├── threshold_agent.py
│   ├── anomaly_agent.py
│   ├── report_agent.py
│   ├── llm_client.py
│   └── llm_insight_agent.py
│
├── templates/
│   ├── index.html
│   ├── job.html
│   └── error.html
│
├── static/
│   └── style.css
│
├── scripts/
│   └── original_occupancy_prototype.py
│
├── tests/
│
├── models/
│
└── storage/
    ├── uploads/
    ├── outputs/
    └── reports/
```

---

## Why This Is More Than a Basic AI Project

A basic computer vision project usually works like this:

```text
Video → Model → Detection Output
```

Occupancy AI Agent works like this:

```text
Video
→ YOLO Vision Engine
→ Spatial Occupancy Reasoning
→ Temporal Smoothing
→ Event Logs
→ Frame-Level Metrics
→ LangGraph Agent Review
→ Optional LLM Explanation
→ Full-Stack Dashboard
→ Downloadable Reports
```

This makes it a real engineering workflow.

It includes computer vision, agent orchestration, stateful processing, evidence generation, human-readable reporting, dashboard-based usage, and production-style artifact management.

---

## Design Principles

### 1. Vision Engine Before LLM

The LLM does not decide occupancy.

The deterministic YOLO and geometry pipeline makes occupancy decisions.

### 2. Evidence Before Explanation

The agent layer reads generated artifacts such as metrics CSV, summary CSV, and processing statistics before producing recommendations.

### 3. Agents Improve Reliability

The agents diagnose problems, score quality, identify anomalies, and recommend review actions.

### 4. Human Review Still Matters

The system creates AI-assisted reports, but important workplace decisions should still be reviewed by a human.

### 5. Product Over Script

The project includes a dashboard, upload flow, background processing, database records, outputs, reports, CLI, tests, and Docker-ready structure.

---


## Common Errors and Fixes

### Error: No module named cv2

Run:

```cmd
python -m pip install opencv-python
```

---

### Error: YOLO model download failed

Use a smaller model:

```text
yolo11n-seg.pt
```

Or manually download the model and place it inside:

```text
models/yolo11n-seg.pt
```

Then use this model path in the dashboard:

```text
models/yolo11n-seg.pt
```

---

### Error: package hash mismatch

Create a fresh virtual environment and reinstall without cache:

```cmd
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
python -m pip cache purge
python -m pip install --no-cache-dir -r requirements.txt
```

If needed:

```cmd
python -m pip install --no-cache-dir -r requirements-minimal.txt
```

---

## License

This project is intended for educational, research, and portfolio purposes.

