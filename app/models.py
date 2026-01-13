from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base

class Heroi(Base):
    __tablename__ = "herois"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    classe = Column(String)  # Ex: "Guerreiro", "Mago"
    
    nivel = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    
    hp_max = Column(Integer, default=100)
    hp_atual = Column(Integer, default=100)
    
    forca = Column(Integer, default=10)
    defesa = Column(Integer, default=5)

class Monstro(Base):
    __tablename__ = "monstros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True)
    
    nivel = Column(Integer)
    hp = Column(Integer)
    forca = Column(Integer)
    xp_recompensa = Column(Integer) # Quanto XP ele dá se morrer

class Batalha(Base):
    __tablename__ = "batalhas"

    id = Column(Integer, primary_key=True, index=True)
    heroi_id = Column(Integer, ForeignKey("herois.id"))
    monstro_id = Column(Integer, ForeignKey("monstros.id"))
    
    monstro_hp_atual = Column(Integer)
    
    ativa = Column(Boolean, default=True) 
    log = Column(String, default="Batalha iniciada!") 