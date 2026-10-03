MODELS = {"local-small": 1, "local-large": 4}
BUDGET = 100

def complete(model, prompt, max_tokens, spent):
    if model not in MODELS:
        return {"allowed": False, "reason": "Model is not on the allowlist.", "called_provider": False}
    cost = MODELS[model] * max_tokens
    if spent + cost > BUDGET:
        return {"allowed": False, "reason": "Token budget exceeded.", "cost": cost, "called_provider": False}
    words = len(prompt.split())
    return {"allowed": True, "completion": f"local-stub:{words} words", "cost": cost, "called_provider": False}
