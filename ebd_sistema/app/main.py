from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine

# Importação dos módulos independentes
from app.routers import auth, alunos, salas, chamada, dashboard, backup

# Cria as tabelas do banco de dados ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema EBD - Escola Dominical")

# Arquivos estáticos (CSS/JS/Imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# REGISTRO DE MÓDULOS (Para tirar ou por uma função, basta comentar ou descomentar a linha)
app.include_router(auth.router)
app.include_router(alunos.router)
app.include_router(salas.router)
app.include_router(chamada.router)
app.include_router(dashboard.router)
app.include_router(backup.router)

@app.get("/")
def inicio():
    return {"status": "Sistema EBD Ativo e Pronto!"}