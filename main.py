from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir CORS (opcional, mas útil se usar com frontends)
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
async def ingest_file(file: UploadFile = File(...)):
    content = await file.read()
    # Lógica de ingestão aqui
    return {"filename": file.filename, "size": len(content)}
