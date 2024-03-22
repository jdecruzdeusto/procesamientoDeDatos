from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import FastAPI, HTTPException, Path, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from models import GeneratorData, AggregatedData  # Asegúrate de tener estos modelos definidos

# Configuración del esquema de seguridad y JWT
SECRET_KEY = "tu_secreto_super_secreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

received_data: List[GeneratorData] = []

# Función para decodificar el JWT
def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Convierte el timestamp a un objeto datetime para la comparación
        exp_timestamp = decoded_token.get("exp")
        if exp_timestamp:
            exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

            if exp >= datetime.now(timezone.utc):
                return decoded_token
            else:
                return None
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e

# Función para crear un token de acceso
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependencia para obtener el usuario actual a partir del token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return {"username": username}

# Endpoint para login y obtención de token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_username = form_data.username
    user_password = form_data.password
    # Verificación de usuario (este es solo un ejemplo, ajusta según tu lógica de autenticación)
    if user_username != "user" or user_password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/generator_data/")
async def receive_data(generator_data: GeneratorData):
    try:
        received_data.append(generator_data)
        return {"message": "Data received successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Rutas protegidas que requieren autenticación
@app.get("/received_data/")
async def get_all_received_data(current_user: dict = Depends(get_current_user)):
    if not received_data:
        raise HTTPException(status_code=404, detail="No data available")
    return received_data

@app.get("/received_data/{generator_id}")
async def get_data_by_generator_id(generator_id: int = Path(..., description="The ID of the generator to retrieve data for"), current_user: dict = Depends(get_current_user)):
    data_for_generator = [data for data in received_data if data.generator_id == generator_id]
    if not data_for_generator:
        raise HTTPException(status_code=404, detail=f"No data found for generator with ID {generator_id}")
    return data_for_generator

@app.get("/average_power_output/")
async def get_average_power_output(current_user: dict = Depends(get_current_user)):
    if not received_data:
        raise HTTPException(status_code=404, detail="No data available")
    total_power = sum(data.power_output for data in received_data)
    average_power = total_power / len(received_data)
    return {"average_power_output": average_power}

@app.get("/average_power_output/{generator_id}")
async def get_average_power_output_by_generator(generator_id: int = Path(..., description="The ID of the generator to retrieve average power output for"), current_user: dict = Depends(get_current_user)):
    data_for_generator = [data for data in received_data if data.generator_id == generator_id]
    if not data_for_generator:
        raise HTTPException(status_code=404, detail=f"No data found for generator with ID {generator_id}")
    total_power = sum(data.power_output for data in data_for_generator)
    average_power = total_power / len(data_for_generator)
    return {"average_power_output": average_power}
