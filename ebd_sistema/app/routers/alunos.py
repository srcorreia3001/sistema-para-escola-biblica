from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Aluno

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.get("/", response_class=HTMLResponse)
def listar_alunos(request: Request, db: Session = Depends(get_db)):
    lista_alunos = db.query(Aluno).filter(Aluno.ativo == True).all()
    # Retorna para o HTML dinâmico
    return f"Alunos cadastrados: {len(lista_alunos)}"

@router.post("/novo")
def cadastrar_aluno(
    nome: str = Form(...),
    telefone: str = Form(None),
    sala_id: int = Form(...),
    db: Session = Depends(get_db)
):
    novo_aluno = Aluno(nome=nome, telefone=telefone, sala_id=sala_id)
    db.add(novo_aluno)
    db.commit()
    return {"mensagem": "Aluno cadastrado com sucesso!"}