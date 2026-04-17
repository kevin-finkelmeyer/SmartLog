import tempfile

from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".log")
    tmp.file.write(await file.read())

    return {"file_path": tmp.name}