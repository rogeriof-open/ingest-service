from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest-file")
async def ingest_file(
    file: UploadFile = File(...),
    userId: str = Form(...),
    namespace: str = Form(...),
    filename: str = Form(...)
):
    # Apenas simulação de ingestão (placeholder)
    return JSONResponse({
        "message": f"Arquivo {filename} recebido para o usuário {userId} no namespace {namespace}."
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
