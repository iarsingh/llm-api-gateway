from gateway.ops import router as ops_router
from fastapi import FastAPI
from gateway.route import complete

app = FastAPI()
app.include_router(ops_router, prefix="/v1")

@app.post("/complete")
def post_complete(body: dict):
    return complete(body["model"], body["prompt"], body["max_tokens"], body.get("spent", 0))
