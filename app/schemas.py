from pydantic import BaseModel

class HeroiCreate(BaseModel):
    nome: str
    classe: str  

class HeroiResponse(BaseModel):
    id: int
    nome: str
    classe: str
    nivel: int
    hp_atual: int
    forca: int
    xp: int

    class Config:
        from_attributes = True

class MonstroCreate(BaseModel):
    nome: str
    nivel: int
    hp: int
    forca: int
    xp_recompensa: int

class MonstroResponse(MonstroCreate):
    id: int
    
    class Config:
        from_attributes = True

class LogBatalha(BaseModel):
    batalha_id: int
    mensagem: str
    heroi_hp: int
    monstro_hp: int
    ativa: bool # Se False, a luta acabou