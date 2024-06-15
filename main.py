from fastapi import FastAPI, HTTPException  # Importa o FastAPI para criar a API e HTTPException para lidar com exceções HTTP
from pydantic import BaseModel  # Importa BaseModel do Pydantic para validação de dados
from fastapi.middleware.cors import CORSMiddleware  # Importa CORSMiddleware para permitir requisições de outras origens
import sqlite3  # Importa sqlite3 para interação com banco de dados SQLite (não utilizado no código fornecido)

# Cria uma instância do FastAPI
app = FastAPI()

# Configura o middleware CORS para permitir requisições de origens específicas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Define a origem permitida (ou "*" para permitir de qualquer origem)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permite métodos específicos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Constantes para os fatores de emissão
# Os valores foram fixados e estipulados para uma melhor compreensão do projeto.
# É necessário fazer pesquisas mais aprofundadas para definir com mais precisão cada valor
NUMERO_EMISSAO_AGUA = 130
NUMERO_EMISSAO_CARNE = 255
NUMERO_EMISSAO_ENERGIA = 175
NUMERO_EMISSAO_COMBUSTIVEL_GASOLINA = 280
NUMERO_EMISSAO_COMBUSTIVEL_ETANOL = 210
# Modelo de dados para a requisição
class RequestData(BaseModel):
    numero_consumo_agua: float
    numero_consumo_carne: float
    numero_consumo_energia: float
    numero_consumo_gasolina: float
    numero_consumo_alcool: float

# Modelo de dados para o resultado (não utilizado no código fornecido)
class Resultado(BaseModel):
    id: int
    num1: float
    num2: float
    resultado: float

# Endpoint para calcular os números
@app.post("/calcular/")
async def calcular_numeros(item: RequestData):
    # Validações para os valores de consumo
    if item.numero_consumo_agua <= 0:
        return "Não foi possível realizar a operação. O consumo de água deve ser zero ou positivo."
    if item.numero_consumo_carne < 0:
        return "Não foi possível realizar a operação. O consumo de carne dever ser zero ou positivo."
    if item.numero_consumo_energia < 0:
        return "Não foi possível realizar a operação. O consumo de energia dever ser zero ou positivo."
    if item.numero_consumo_gasolina < 0:
        return "Não foi possível realizar a operação. O consumo de gasolina dever ser zero ou positivo."
    if item.numero_consumo_alcool < 0:
        return "Não foi possível realizar a operação. O consumo de alcool dever ser zero ou positivo."
    
    # Calcula o fator de emissão de água
    fator_emissao_agua = NUMERO_EMISSAO_AGUA / item.numero_consumo_agua
    
    # Calcula o fator de emissão de carne
    fator_emissao_carne = NUMERO_EMISSAO_CARNE / item.numero_consumo_carne
    
    # Calcula o fator de emissão de energia
    fator_emissao_energia = NUMERO_EMISSAO_ENERGIA / item.numero_consumo_energia
    
    # Calcula o fator de emissão de combustível (gasolina), se houver consumo
    if item.numero_consumo_gasolina > 0:
        fator_emissao_combustivel_gasolina = (NUMERO_EMISSAO_COMBUSTIVEL_GASOLINA ** 2) / item.numero_consumo_gasolina
    else:
        fator_emissao_combustivel_gasolina = 0
    
    # Calcula o fator de emissão de combustível (álcool), se houver consumo
    if item.numero_consumo_alcool > 0:
        fator_emissao_combustivel_alcool = (NUMERO_EMISSAO_COMBUSTIVEL_ETANOL ** 2) / item.numero_consumo_alcool
    else:
        fator_emissao_combustivel_alcool = 0
        
    # Calcula o total de emissão somando todos os fatores de emissão
    total_emissao = fator_emissao_agua + fator_emissao_carne + fator_emissao_energia + fator_emissao_combustivel_gasolina + fator_emissao_combustivel_alcool

    # Retorna o resultado como um dicionário
    return {
        "Emissão Água": fator_emissao_agua,
        "Emissão Carne": fator_emissao_carne,
        "Emissão Energia": fator_emissao_energia,
        "Emissão Gasolina": fator_emissao_combustivel_gasolina,
        "Emissão Álcool": fator_emissao_combustivel_alcool,
        "TotalEmissao": total_emissao
    }
