from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
import random 
from fastapi import FastAPI, Depends, HTTPException

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="RPG Engine API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/herois/", response_model=schemas.HeroiResponse)
def criar_heroi(heroi: schemas.HeroiCreate, db: Session = Depends(get_db)):
    # Lógica de Classes (Regra de Negócio)
    hp_inicial = 100
    forca_inicial = 10
    
    if heroi.classe.lower() == "guerreiro":
        hp_inicial = 150  
        forca_inicial = 15
    elif heroi.classe.lower() == "mago":
        hp_inicial = 80   
        forca_inicial = 8 
    
    db_heroi = models.Heroi(
        nome=heroi.nome,
        classe=heroi.classe,
        hp_max=hp_inicial,
        hp_atual=hp_inicial,
        forca=forca_inicial
    )
    
    db.add(db_heroi)
    db.commit()
    db.refresh(db_heroi)
    return db_heroi

@app.get("/herois/", response_model=list[schemas.HeroiResponse])
def listar_herois(db: Session = Depends(get_db)):
    return db.query(models.Heroi).all()


@app.post("/monstros/", response_model=schemas.MonstroResponse)
def criar_monstro(monstro: schemas.MonstroCreate, db: Session = Depends(get_db)):
    db_monstro = models.Monstro(**monstro.dict())
    db.add(db_monstro)
    db.commit()
    db.refresh(db_monstro)
    return db_monstro

@app.get("/monstros/", response_model=list[schemas.MonstroResponse])
def listar_monstros(db: Session = Depends(get_db)):
    return db.query(models.Monstro).all()


@app.post("/batalha/iniciar/{heroi_id}/{monstro_id}", response_model=schemas.LogBatalha)
def iniciar_batalha(heroi_id: int, monstro_id: int, db: Session = Depends(get_db)):

    heroi = db.query(models.Heroi).get(heroi_id)
    monstro = db.query(models.Monstro).get(monstro_id)

    if not heroi or not monstro:
        raise HTTPException(status_code=404, detail="Heroi ou Monstro não encontrado")

    nova_batalha = models.Batalha(
        heroi_id=heroi.id,
        monstro_id=monstro.id,
        monstro_hp_atual=monstro.hp, 
        ativa=True,
        log="Batalha iniciada!"
    )
    
    db.add(nova_batalha)
    db.commit()
    db.refresh(nova_batalha)

    return {
        "batalha_id": nova_batalha.id,
        "mensagem": f"Luta iniciada! {heroi.nome} VS {monstro.nome}",
        "heroi_hp": heroi.hp_atual,
        "monstro_hp": nova_batalha.monstro_hp_atual,
        "ativa": True
    }

@app.post("/batalha/atacar/{batalha_id}", response_model=schemas.LogBatalha)
def realizar_ataque(batalha_id: int, db: Session = Depends(get_db)):
    batalha = db.query(models.Batalha).get(batalha_id)
    
    if not batalha or not batalha.ativa:
        raise HTTPException(status_code=400, detail="Batalha não encontrada ou já encerrada")

    heroi = db.query(models.Heroi).get(batalha.heroi_id)
    monstro_ref = db.query(models.Monstro).get(batalha.monstro_id) #pegar dados fixos (xp, força)

    log_turno = []

    # HERÓI 
    # Dano aleatório entre 50% e 100% da força
    dano_heroi = random.randint(heroi.forca // 2, heroi.forca)
    batalha.monstro_hp_atual -= dano_heroi
    log_turno.append(f"Você causou {dano_heroi} de dano.")

    # Verifica se Monstro Morreu
    if batalha.monstro_hp_atual <= 0:
        batalha.ativa = False
        batalha.monstro_hp_atual = 0
        
        heroi.xp += monstro_ref.xp_recompensa
        log_turno.append(f"VITORIA! O monstro morreu. Você ganhou {monstro_ref.xp_recompensa} XP.")
        
        # Cura um pouco o herói pela vitória
        heroi.hp_atual = min(heroi.hp_atual + 10, heroi.hp_max) 
        
        db.commit()
        return {
            "batalha_id": batalha.id,
            "mensagem": " ".join(log_turno),
            "heroi_hp": heroi.hp_atual,
            "monstro_hp": 0,
            "ativa": False
        }

    # MONSTRO 
    dano_monstro = random.randint(monstro_ref.forca // 2, monstro_ref.forca)
    heroi.hp_atual -= dano_monstro
    log_turno.append(f"O monstro revidou com {dano_monstro} de dano!")

    # Verifica se Herói Morreu
    if heroi.hp_atual <= 0:
        batalha.ativa = False
        heroi.hp_atual = 0
        log_turno.append("DERROTA! Você caiu em combate...")

    batalha.log = " | ".join(log_turno)
    db.commit()

    return {
        "batalha_id": batalha.id,
        "mensagem": " ".join(log_turno),
        "heroi_hp": heroi.hp_atual,
        "monstro_hp": batalha.monstro_hp_atual,
        "ativa": batalha.ativa
    }