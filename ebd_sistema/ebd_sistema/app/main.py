from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine

# Importamos por enquanto apenas o módulo de Autenticação
from app.routers import auth

# Os restantes módulos ficam comentados até serem programados:
# from app.routers import alunos, salas, chamada, dashboard, backup

# Cria as tabelas do banco de dados ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema EBD - Escola Dominical")

# Registo apenas das rotas ativas
app.include_router(auth.router)

# À medida que formos criando os novos módulos, basta descomentar as linhas abaixo:
# app.include_router(alunos.router)
# app.include_router(salas.router)
# app.include_router(chamada.router)
# app.include_router(dashboard.router)
# app.include_router(backup.router)

@app.get("/")
def inicio():
    return {"status": "Sistema EBD Ativo e Pronto!"}