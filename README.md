# LLM API Gateway

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/gateway/main.py`](src/gateway/main.py) | HTTP handlers: `POST /complete` |
| [`src/gateway/route.py`](src/gateway/route.py) | Functions: `complete` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/gateway/__init__.py`](src/gateway/__init__.py) | Implementation or supporting configuration |
| [`tests/test_gateway.py`](tests/test_gateway.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn gateway.main:app --reload
```

<!-- project-guide:end -->

Level: 13 — LLMOps

Skills: Python, an allowlist, a token budget

Accept only `local-small` and `local-large`. Price the call from the token cap and reject it when the spend would pass 100. The completion is a local stub. No provider is called.

```bash
pip install -r requirements.txt
pytest -q
```
