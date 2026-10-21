from fastapi import APIRouter, Depends, Request, Form, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticação"])
templates = Jinja2Templates(directory="app/templates")

# Utilitário de Criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_hash_senha(senha_plana: str) -> str:
    return pwd_context.hash(senha_plana)

# Tela de Login (GET)
@router.get("/login", response_class=HTMLResponse)
def tela_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Processamento do Form de Login (POST)
@router.post("/login")
def processar_login(
    request: Request,
    response: Response,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    # Validação de credenciais
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "erro": "E-mail ou senha incorretos."},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Criação da resposta e definição do Cookie de Sessão
    res = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    res.set_cookie(key="usuario_id", value=str(usuario.id), httponly=True)
    res.set_cookie(key="usuario_perfil", value=usuario.perfil, httponly=True)
    return res

# Logout (Sair do Sistema)
@router.get("/logout")
def logout():
    res = RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    res.delete_cookie("usuario_id")
    res.delete_cookie("usuario_perfil")
    return res