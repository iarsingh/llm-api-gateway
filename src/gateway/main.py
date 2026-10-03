from fastapi import FastAPI
from gateway.route import complete

app = FastAPI()

@app.post("/complete")
def post_complete(body: dict):
    return complete(body["model"], body["prompt"], body["max_tokens"], body.get("spent", 0))
