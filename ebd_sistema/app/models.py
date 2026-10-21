from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    perfil = Column(String, default="professor")  # 'admin' ou 'professor'

class Sala(Base):
    __tablename__ = "salas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)         # Ex: "Mocidade", "Primários"
    faixa_etaria = Column(String, nullable=True)

    alunos = relationship("Aluno", back_populates="sala")
    chamadas = relationship("Chamada", back_populates="sala")

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    ativo = Column(Boolean, default=True)
    sala_id = Column(Integer, ForeignKey("salas.id"))

    sala = relationship("Sala", back_populates="alunos")

class Chamada(Base):
    __tablename__ = "chamadas"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False)         # AAAA-MM-DD
    sala_id = Column(Integer, ForeignKey("salas.id"))
    
    # Métricas de acompanhamento
    total_presentes = Column(Integer, default=0)
    total_ausentes = Column(Integer, default=0)
    qtd_biblias = Column(Integer, default=0)
    qtd_revistas = Column(Integer, default=0)
    valor_oferta = Column(Float, default=0.0)
    sugestoes = Column(Text, nullable=True)

    sala = relationship("Sala", back_populates="chamadas")