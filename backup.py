from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class RequestData(BaseModel):
    numero_vAgua: float
    numero_cCarne: float
    numero_cEnergia: float

class Resultado(BaseModel):
    id: int
    num1: float
    num2: float
    resultado: float

# Função para criar a tabela se ela não existir
 def create_table():
    conn = sqlite3.connect("resultados.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS calculos (
            id INTEGER PRIMARY KEY,
            num1 FLOAT,
            num2 FLOAT,
            resultado FLOAT
        )
        """
    )
    conn.commit()
    conn.close() 

@app.post("/calcular/")
async def calcular_numeros(item: RequestData):
    resultado = item.num1 + item.num2
    # Gravando no banco de dados
    conn = sqlite3.connect('resultados.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO calculos (num1, num2, resultado)
        VALUES (?, ?, ?)
    ''', (item.num1, item.num2, resultado))
    conn.commit()
    conn.close()
    return {"resultado": resultado}

@app.get("/resultados/", response_model=list[Resultado])
async def listar_resultados():
    conn = sqlite3.connect("resultados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, num1, num2, resultado FROM calculos")
    resultados = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "num1": r[1], "num2": r[2], "resultado": r[3]} for r in resultados]

@app.delete("/resultados/{resultado_id}")
async def deletar_resultado(resultado_id: int):
    conn = sqlite3.connect("resultados.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calculos WHERE id = ?", (resultado_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Resultado não encontrado")
    conn.commit()
    conn.close()
    return {"mensagem": "Resultado deletado com sucesso"}

@app.put("/resultados/{resultado_id}")
async def atualizar_resultado(resultado_id: int, item: RequestData):
    novo_resultado = item.num1 + item.num2
    conn = sqlite3.connect("resultados.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE calculos SET num1 = ?, num2 = ?, resultado = ? WHERE id = ?",
        (item.num1, item.num2, novo_resultado, resultado_id)
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Resultado não encontrado")
    conn.commit()
    conn.close()
    return {"mensagem": "Resultado atualizado com sucesso"}

# Chama a função create_table() para garantir que a tabela exista
create_table()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

