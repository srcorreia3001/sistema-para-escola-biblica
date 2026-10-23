from pathlib import Path
from fastapi import APIRouter, Depends, Request, Form, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..database import get_db
from ..models import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticação"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_hash_senha(senha_plana: str) -> str:
    return pwd_context.hash(senha_plana)

@router.get("/login", response_class=HTMLResponse)
def tela_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@router.post("/login")
def processar_login(
    request: Request,
    response: Response,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return templates.TemplateResponse(
            request=request,
            name="login.html", 
            context={"erro": "E-mail ou senha incorretos."},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Redireciona para a tela de Alunos após o login com sucesso
    res = RedirectResponse(url="/alunos", status_code=status.HTTP_302_FOUND)
    res.set_cookie(key="usuario_id", value=str(usuario.id), httponly=True)
    res.set_cookie(key="usuario_perfil", value=usuario.perfil, httponly=True)
    return res

@router.get("/logout")
def logout():
    res = RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    res.delete_cookie("usuario_id")
    res.delete_cookie("usuario_perfil")
    return res