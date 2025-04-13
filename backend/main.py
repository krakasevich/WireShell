from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, ClientConfig
from wireguard import (
    generate_keypair,
    generate_client_config,
    SERVER_CONFIGS,
    add_peer_to_server,
    get_next_available_ip,
    generate_client_keys,
    get_server_public_key,
    add_peer_to_remote_server
)
import hashlib
import subprocess
from sqlalchemy import and_

# Creating tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Обновляем настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The data model from the client
class UserCreate(BaseModel):
    username: str
    password: str

class ConfigRequest(BaseModel):
    user_id: int
    location: str  # Добавляем поле для локации

# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# The endpoint for registration
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Checking if the user exists
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="The user already exists")

        # Hashing the password
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        
        # Creating a new user
        db_user = User(
            username=user.username,
            password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {
            "message": "The user has been successfully registered",
            "user_id": db_user.id,
            "username": db_user.username
        }
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

# The entry endpoint
@app.post("/login")
async def login(request: UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"Login attempt for user: {request.username}")
        user = db.query(User).filter(User.username == request.username).first()
        
        if not user:
            print(f"User not found: {request.username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Хешируем введенный пароль и сравниваем с хешем в базе
        hashed_password = hashlib.sha256(request.password.encode()).hexdigest()
        if user.password != hashed_password:
            print(f"Invalid password for user: {request.username}")
            raise HTTPException(status_code=401, detail="Invalid username or password")
            
        print(f"Successful login for user: {request.username}")
        return {"message": "Login successful", "user_id": user.id, "username": user.username}
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@app.post("/api/generate-config")
async def generate_wireguard_config(config_request: ConfigRequest, db: Session = Depends(get_db)):
    """Генерирует конфигурацию WireGuard для пользователя"""
    try:
        print(f"Generating keys for user {config_request.user_id} in location {config_request.location}")
        
        # Проверяем существование пользователя
        user = db.query(User).filter(User.id == config_request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Проверяем поддерживаемые локации
        if config_request.location not in SERVER_CONFIGS:
            raise HTTPException(status_code=400, detail=f"Unsupported location. Available locations: {', '.join(SERVER_CONFIGS.keys())}")
            
        # Проверяем существующую конфигурацию
        existing_config = db.query(ClientConfig).filter(
            and_(
                ClientConfig.user_id == config_request.user_id,
                ClientConfig.location == config_request.location
            )
        ).first()
        
        if existing_config:
            return {
                "config": existing_config.config_text,
                "filename": f"wireguard-{config_request.location}-{config_request.user_id}.conf"
            }
            
        # Получаем список использованных IP-адресов для данной локации
        used_ips = db.query(ClientConfig.assigned_ip).filter(
            ClientConfig.location == config_request.location
        ).all()
        used_ips = [ip[0] for ip in used_ips]
        
        # Генерируем новый IP-адрес для выбранной локации
        client_ip = get_next_available_ip(used_ips, config_request.location)
        print(f"Generated IP address: {client_ip}")
        
        # Получаем конфигурацию сервера для выбранной локации
        server_config = SERVER_CONFIGS[config_request.location]
        server_endpoint = server_config["endpoint"]
        server_public_key = server_config["public_key"]
        
        # Генерируем ключи клиента
        client_private_key, client_public_key = generate_client_keys()
        print(f"Generated client keys. Public key: {client_public_key}")
        
        # Добавляем пир на сервер
        try:
            # Если локация - london, отправляем запрос на лондонский сервер
            if config_request.location == "london":
                await add_peer_to_remote_server(client_public_key, client_ip, config_request.location)
            else:
                add_peer_to_server(client_public_key, client_ip)
            print(f"Successfully added peer to server")
        except Exception as e:
            print(f"Failed to add peer to server: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to add peer to server: {str(e)}")
            
        # Генерируем конфигурацию клиента
        config = generate_client_config(
            private_key=client_private_key,
            client_ip=client_ip,
            server_public_key=server_public_key,
            server_endpoint=server_endpoint,
            location=config_request.location
        )
        print(f"Generated client configuration for IP: {client_ip}")
        
        # Сохраняем конфигурацию в базу данных
        client_config = ClientConfig(
            user_id=config_request.user_id,
            location=config_request.location,
            private_key=client_private_key,
            public_key=client_public_key,
            assigned_ip=client_ip,
            config_text=config
        )
        db.add(client_config)
        db.commit()
        print(f"Saved configuration to database")
        
        return {
            "config": config,
            "filename": f"wireguard-{config_request.location}-{config_request.user_id}.conf"
        }
        
    except Exception as e:
        print(f"Error generating config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating config: {str(e)}")