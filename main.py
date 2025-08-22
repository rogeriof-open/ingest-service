from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API online e funcionando."}

@app.post("/ingest-file")
async def ingest_file(
    file: UploadFile = File(...),
    user: str = Form(...),
    namespace: str = Form(...)
):
    content = await file.read()
    return {
        "filename": file.filename,
        "size": len(content),
        "user": user,
        "namespace": namespace
    }
