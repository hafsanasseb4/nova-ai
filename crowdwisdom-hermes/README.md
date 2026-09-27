# CrowdWisdomTrading Hermes

A beginner-readable, modular Python pipeline for competitor ad research, ad analysis, recent web research, script/storyboard generation, and optional video generation.

The pipeline is intentionally runnable without credentials. With no API keys it uses deterministic demo data and writes the same intermediate JSON artifacts as a live run. Real integrations are enabled by adding values to `.env` (never commit that file).

## Setup

```powershell
cd crowdwisdom-hermes
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

## Run demo mode

```powershell
python -m app.main --topic "AI trading education" --competitors "Trade Ideas, Finimize" --demo
```

Run live integrations when the relevant keys are present:

```powershell
python -m app.main --topic "AI trading education" --competitors "Trade Ideas, Finimize"
```

Use an existing storyboard JSON with the video stage:

```powershell
python -m app.main --storyboard outputs/storyboards/<run-id>.json --video
```

Run tests:

```powershell
python -m pytest -q
```

## Architecture

`supervisor.py` coordinates the stages: ads manager -> ad analyzer -> research -> script -> video. Each stage has a narrow typed input/output model and saves JSON through `data_loader.py`. Provider tools fail clearly when a key is missing and fall back to demo mode when the CLI requests it.

Hermes is represented by `app/hermes_runtime.py`, a thin compatibility layer around the optional `hermes-agent` package. This keeps the business logic testable even if the framework is not installed yet, while preserving a single place to adopt the installed Hermes runtime API.

