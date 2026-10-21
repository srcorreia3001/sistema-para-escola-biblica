from app.database import SessionLocal, engine, Base
from app.models import Usuario
from app.routers.auth import gerar_hash_senha

# Garante que as tabelas existem
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Verifica se o admin já existe
admin_existente = db.query(Usuario).filter(Usuario.email == "admin@ebd.com").first()

if not admin_existente:
    admin = Usuario(
        nome="Administrador EBD",
        email="admin@ebd.com",
        senha_hash=gerar_hash_senha("admin123"),
        perfil="admin"
    )
    db.add(admin)
    db.commit()
    print("Usuário Administrador cadastrado com sucesso! (Email: admin@ebd.com | Senha: admin123)")
else:
    print("Administrador já está cadastrado no banco.")

db.close()