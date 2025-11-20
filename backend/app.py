from collections import defaultdict
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .database import SessionLocal, init_db   # <- aqui
from . import models, schemas, security


# cria as tabelas ao subir a API
init_db()   # <- adiciona essa linha ANTES de usar o banco


app = FastAPI(title="Datainsight AVALIA NR01 PRO")

origins = [
    "http://localhost:5500",
    "http://localhost:5173",
    "https://nr01teste.netlify.app",
    "*"  # na demo, pode deixar aberto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    from jose import JWTError, jwt

    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido (sem sub).",
            )
        user_id = int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado.",
        )
    return user


# ==== AUTH =======================================================

@app.post("/api/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Busca usuário pelo e-mail
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    # Se não achou ou senha não bate → 400 (não 500)
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ou senha inválidos",
        )

    # Cria token JWT
    access_token = security.create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    # Aqui eu NÃO uso schemas.UserOut.from_orm para evitar erro 500 com Pydantic v2
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
    }


@app.get("/api/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    # FastAPI/Pydantic convertem o ORM para UserOut
    return current_user


# ==== CAMPANHAS ==================================================

@app.post("/api/campaigns", response_model=schemas.CampaignOut)
def create_campaign(
    body: schemas.CampaignCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    camp = models.Campaign(
        company_name=body.company_name,
        title=body.title,
        description=body.description,
    )
    db.add(camp)
    db.commit()
    db.refresh(camp)
    return camp


@app.get("/api/campaigns", response_model=list[schemas.CampaignOut])
def list_campaigns(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Campaign)
        .order_by(models.Campaign.created_at.desc())
        .all()
    )


@app.get("/api/campaigns/{campaign_id}/summary", response_model=schemas.SummaryOut)
def campaign_summary(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    camp = db.query(models.Campaign).filter(
        models.Campaign.id == campaign_id
    ).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")

    rows = (
        db.query(models.Dimension.name, models.Response.score)
        .join(models.Response, models.Response.dimension_id == models.Dimension.id)
        .filter(models.Response.campaign_id == campaign_id)
        .all()
    )

    soma = defaultdict(int)
    cont = defaultdict(int)

    for dim_name, score in rows:
        soma[dim_name] += score
        cont[dim_name] += 1

    averages = {dim: round(soma[dim] / cont[dim], 2) for dim in soma} if soma else {}

    return schemas.SummaryOut(
        campaign=schemas.CampaignOut.from_orm(camp),
        averages=averages,
    )



