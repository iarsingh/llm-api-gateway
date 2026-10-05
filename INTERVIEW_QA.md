# llm-api-gateway — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does llm-api-gateway address, and what can you demonstrate?

Accept only `local-small` and `local-large`. Price the call from the token cap and reject it when the spend would pass 100. The completion is a local stub. No provider is called.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/gateway/main.py`](src/gateway/main.py): Implementation or supporting configuration.
- [`src/gateway/route.py`](src/gateway/route.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/gateway/__init__.py`](src/gateway/__init__.py): Implementation or supporting configuration.
- [`tests/test_gateway.py`](tests/test_gateway.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `complete` and explain the decision it makes?

The main walkthrough here is `complete(model, prompt, max_tokens, spent)` in [`src/gateway/route.py`](src/gateway/route.py#L4).

```python
def complete(model, prompt, max_tokens, spent):
    if model not in MODELS:
        return {"allowed": False, "reason": "Model is not on the allowlist.", "called_provider": False}
    cost = MODELS[model] * max_tokens
    if spent + cost > BUDGET:
        return {"allowed": False, "reason": "Token budget exceeded.", "cost": cost, "called_provider": False}
    words = len(prompt.split())
    return {"allowed": True, "completion": f"local-stub:{words} words", "cost": cost, "called_provider": False}
```

The implementation calls `len`, `prompt.split`. In an interview, trace those calls in execution order using a fixture input.

## 4. Where would you add input-validation tests?

Start with the handlers `post_complete` in [`src/gateway/main.py`](src/gateway/main.py#L7). Use the request schema or body access in each handler to build valid, missing-field, wrong-type, and boundary inputs. I would inspect existing tests before claiming coverage.

## 5. Which test would you use to demonstrate correctness?

[`tests/test_gateway.py`](tests/test_gateway.py#L4) contains `test_allowlist_and_budget`:

```python
def test_allowlist_and_budget():
    client = TestClient(app)
    good = client.post("/complete", json={"model": "local-small", "prompt": "Summarize the budget.", "max_tokens": 20, "spent": 0}).json()
    assert good["allowed"] is True
    assert good["called_provider"] is False
    assert good["cost"] == 20
    blocked = client.post("/complete", json={"model": "hosted-xl", "prompt": "hi", "max_tokens": 10, "spent": 0}).json()
    assert blocked["allowed"] is False
    over = client.post("/complete", json={"model": "local-large", "prompt": "hi", "max_tokens": 30, "spent": 0}).json()
    assert over["allowed"] is False
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 6. What HTTP interface does the code expose?

- `POST /complete` → `post_complete` in [`src/gateway/main.py`](src/gateway/main.py#L7).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 7. Where does state live, and what happens with multiple workers?

Module-level containers include `MODELS` in [`src/gateway/route.py`](src/gateway/route.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 8. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 9. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 10. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 11. What is the input-to-output contract of `complete`?

In [`src/gateway/route.py`](src/gateway/route.py#L4), `complete(model, prompt, max_tokens, spent)` receives the inputs. The function computes these intermediate values:

- `cost = MODELS[model] * max_tokens`
- `words = len(prompt.split())`

Its result is defined by:

- `{'allowed': True, 'completion': f'local-stub:{words} words', 'cost': cost, 'called_provider': False}`
- `{'allowed': False, 'reason': 'Model is not on the allowlist.', 'called_provider': False}`
- `{'allowed': False, 'reason': 'Token budget exceeded.', 'cost': cost, 'called_provider': False}`

## 12. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/gateway/route.py`](src/gateway/route.py#L4) branches on:

- `model not in MODELS`
- `spent + cost > BUDGET`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
