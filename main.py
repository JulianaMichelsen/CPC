from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

numero_EmissaoAgua = 175
numero_EmissaoCarne = 175
numero_EmissaoEnergia = 175

class RequestData(BaseModel):
    numero_vAgua: float
    numero_cCarne: float
    numero_cEnergia: float

class Resultado(BaseModel):
    id: int
    num1: float
    num2: float
    resultado: float


@app.post("/calcular/")
async def calcular_numeros(item: RequestData):
    fator_EmissaoAgua = numero_EmissaoAgua / item.numero_vAgua
    
    fator_EmissaoCarne = numero_EmissaoCarne / item.numero_cCarne
    
    fator_EmissaoEnergia = numero_EmissaoEnergia / item.numero_cEnergia

    return "Emissão Água:" + str(fator_EmissaoAgua) + " Emissão Carne:" + str(fator_EmissaoCarne) + " Emissão Energia:" + str(fator_EmissaoEnergia)
