from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir CORS (útil para testes com Postman ou frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota para teste rápido se API está de pé
@app.get("/")
def root():
    return {"message": "API online e funcionando."}

# Rota para envio de arquivo
@app.post("/ingest-file")
async def ingest_file(
    file: UploadFile = File(...),
    user: str = Form(...),
    namespace: str = Form(...)
):
    content = await file.read()
    return {
        "filename": file.filename,
        "user": user,
        "namespace": namespace,
        "size": len(content)
    }
