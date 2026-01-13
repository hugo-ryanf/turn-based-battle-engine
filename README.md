# ⚔️ Turn-Based RPG Battle Engine

> API Backend robusta que simula a lógica complexa de um jogo de RPG em turnos, com cálculos de dano, sistema de XP e persistência de dados.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-green)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)

## 🧠 Sobre o Projeto

Este projeto não é apenas um CRUD. É uma **Game Engine** via API. O objetivo foi desenvolver algoritmos que gerenciam o ciclo de vida de uma batalha (Game Loop), garantindo que as regras do jogo sejam aplicadas corretamente no servidor.

### Diferenciais Técnicos:
* **Gestão de Estado:** O backend controla de quem é a vez (Player vs CPU).
* **Fator RNG:** Cálculos de dano incluem variação aleatória (sorte/crítico) baseada em atributos.
* **Lógica de Negócio:** Validações impedem ações ilegais (ex: atacar um monstro morto ou atacar fora de turno).

## 🛠 Tech Stack

* **[FastAPI](https://fastapi.tiangolo.com/):** Framework moderno para APIs assíncronas.
* **[SQLAlchemy](https://www.sqlalchemy.org/):** ORM para persistência de heróis e histórico de batalhas.
* **[Pydantic](https://docs.pydantic.dev/):** Schemas rigorosos para entrada/saída de dados.
* **SQLite:** Banco de dados leve para simulação local.

## 🚀 Como Rodar o Jogo (Localmente)

### 1. Clone o repositório
```bash
git clone [https://github.com/hugo-ryanf/turn-based-battle-engine.git](https://github.com/hugo-ryanf/turn-based-battle-engine.git)
cd turn-based-battle-engine
```
2. Configure o Ambiente

```
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as Dependências
```
pip install -r requirements.txt
```
4. Inicie o Servidor
```
python -m uvicorn app.main:app --reload
```
O jogo estará disponível em: http://127.0.0.1:8000

🎮 Documentação (Endpoints)
Para testar a engine visualmente, acesse o Swagger UI: 👉 http://127.0.0.1:8000/docs

Fluxo Principal de Batalha:

### Fluxo Principal de Batalha

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/herois` | Cria um personagem (Guerreiro/Mago) com atributos base. |
| `POST` | `/batalhas/iniciar` | Sorteia um monstro e inicia uma sessão de combate. |
| `POST` | `/batalhas/{id}/atacar` | **Core:** Executa o turno, calcula dano e contra-ataque. |
| `GET` | `/herois/{id}` | Verifica HP atual, XP acumulado e Nível. |
| `GET` | `/batalhas/{id}` | Consulta o log/histórico do que aconteceu na luta. |


👨‍💻 Autor: 
Desenvolvido por Hugo Ryan.
