import tempfile

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

from smartlog.analyzer import Analyzer


class AnalyzeRequest(BaseModel):
    file_path: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".log")
    tmp.file.write(await file.read())

    return {"file_path": tmp.name}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    path = request.file_path
    a = Analyzer(path)
    result = a.ask()
    return {"result": result}