from pathlib import Path
from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Aluno, Sala

router = APIRouter(prefix="/alunos", tags=["Alunos"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/", response_class=HTMLResponse)
def listar_alunos(request: Request, db: Session = Depends(get_db)):
    usuario_id = request.cookies.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)

    lista_alunos = db.query(Aluno).all()
    lista_salas = db.query(Sala).all()

    return templates.TemplateResponse(
        request=request,
        name="alunos.html",
        context={"alunos": lista_alunos, "salas": lista_salas, "usuario_logado": True}
    )


@router.post("/novo")
def cadastrar_aluno(
    request: Request,
    nome: str = Form(...),
    telefone: str = Form(None),
    data_nascimento: str = Form(None),
    sala_id: int = Form(...),
    db: Session = Depends(get_db)
):
    novo_aluno = Aluno(
        nome=nome,
        telefone=telefone,
        data_nascimento=data_nascimento,
        sala_id=sala_id
    )
    db.add(novo_aluno)
    db.commit()
    return RedirectResponse(url="/alunos", status_code=status.HTTP_302_FOUND)

