from fastapi import FastAPI
from nusy_pm_core.cli import get_version

app = FastAPI(title="NuSy Product Manager Core")

@app.get("/health")
def health():
    return {"status": "ok", "component": "nusy-pm-core"}

@app.get("/version")
def version():
    return {"version": get_version()}
