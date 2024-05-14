from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # ou "*" para permitir de qualquer origem
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

NUMERO_EMISSAO_AGUA = 175
NUMERO_EMISSAO_CARNE = 175
NUMERO_EMISSAO_ENERGIA = 175
NUMERO_EMISSAO_COMBUSTIVEL = 175

class RequestData(BaseModel):
    numero_consumo_agua: float
    numero_consumo_carne: float
    numero_consumo_energia: float
    numero_consumo_gasolina: float
    numero_consumo_alcool: float

class Resultado(BaseModel):
    id: int
    num1: float
    num2: float
    resultado: float

@app.post("/calcular/")
async def calcular_numeros(item: RequestData):
    if item.numero_consumo_agua <=0:
        return "Não foi possível realizar a operação. O consumo de água deve ser zero ou positivo."
    if item.numero_consumo_carne <0:
        return "Não foi possível realizar a operação. O consumo de carne dever ser zero ou positivo."
    if item.numero_consumo_energia <0:
        return "Não foi possível realizar a operação. O consumo de energia dever ser zero ou positivo."
    if item.numero_consumo_gasolina <0:
        return "Não foi possível realizar a operação. O consumo de gasolina dever ser zero ou positivo."
    if item.numero_consumo_alcool <0:
        return "Não foi possível realizar a operação. O consumo de alcool dever ser zero ou positivo."
    
    fator_emissao_agua = NUMERO_EMISSAO_AGUA / item.numero_consumo_agua
    
    fator_emissao_carne = NUMERO_EMISSAO_CARNE / item.numero_consumo_carne
    
    fator_emissao_energia = NUMERO_EMISSAO_ENERGIA / item.numero_consumo_energia
    
    if item.numero_consumo_gasolina > 0:
        fator_emissao_combustivel_gasolina = (NUMERO_EMISSAO_COMBUSTIVEL ** 2) / item.numero_consumo_gasolina
    else:
        fator_emissao_combustivel_gasolina = 0
    
    if item.numero_consumo_alcool > 0:
        fator_emissao_combustivel_alcool = (NUMERO_EMISSAO_COMBUSTIVEL ** 2) / item.numero_consumo_alcool
    else:
        fator_emissao_combustivel_alcool = 0
        
    total_emissao = fator_emissao_agua + fator_emissao_carne + fator_emissao_energia + fator_emissao_combustivel_gasolina + fator_emissao_combustivel_alcool

    return {"Emissão Água" :  fator_emissao_agua, "Emissão Carne" :  fator_emissao_carne, "Emissão Energia" : fator_emissao_energia, "Emissão Gasolina" : fator_emissao_combustivel_gasolina, "Emissão Álcool" : fator_emissao_combustivel_alcool, "TotalEmissao" : total_emissao}
