from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()

# CORS (opcional para testes com frontend ou Postman)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest-file")
async def ingest_file(
    file: UploadFile = File(...),
    user: str = Form(...),
    namespace: str = Form(...)
):
    # Para teste, apenas printa ou retorna os dados
    contents = await file.read()
    return {
        "filename": file.filename,
        "user": user,
        "namespace": namespace,
        "filesize_bytes": len(contents)
    }

