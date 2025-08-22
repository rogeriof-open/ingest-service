# main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx

app = FastAPI(title="Ingest Service")

# Habilita CORS para qualquer origem (ajuste conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # coloque seu domínio em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pasta temporária para salvar os arquivos no container
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest-file")
async def ingest_file(
    file: UploadFile = File(...),
    user: str = Form(...),
    namespace: str = Form(default="default")
):
    try:
        content = await file.read()
        save_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(save_path, "wb") as f:
            f.write(content)

        # Simulação do corpo da requisição (exemplo para Rocketment)
        return {
            "user": user,
            "namespace": namespace,
            "filename": file.filename,
            "saved_path": save_path,
            "file_size": len(content)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Upload via link (baixar do Postman ou cliente)
class IngestByURL(BaseModel):
    file_url: str
    user: str
    namespace: str = "default"

@app.post("/ingest")
async def ingest_url(body: IngestByURL):
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.get(body.file_url)
            if r.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Falha ao baixar arquivo: {r.status_code}")

            filename = body.file_url.split("/")[-1].split("?")[0] or "file.bin"
            save_path = os.path.join(UPLOAD_DIR, filename)
            with open(save_path, "wb") as f:
                f.write(r.content)

        return {
            "user": body.user,
            "namespace": body.namespace,
            "filename": filename,
            "saved_path": save_path,
            "file_size": len(r.content)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Execução local (com reload para testes locais)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

