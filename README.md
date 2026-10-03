# LLM API Gateway

Level: 13 — LLMOps

Skills: Python, an allowlist, a token budget

Accept only `local-small` and `local-large`. Price the call from the token cap and reject it when the spend would pass 100. The completion is a local stub. No provider is called.

```bash
pip install -r requirements.txt
pytest -q
```
