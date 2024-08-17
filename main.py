from unittest.mock import Base
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from ulid import ulid


app = FastAPI()


class Corrida(BaseModel):
    id: str | None
    origem : str
    destino : str
    distancia : int
    valor : float
    estado : str


def calcular(distancia: int) -> float:
    return distancia * 2 + 6.65

corridas: list[Corrida] = [
    Corrida(id=str(ulid()),
            origem= 'the',
            destino='sp',
            distancia= 6,
            valor = calcular(distancia=6),
            estado = 'requisitada'),
    Corrida(id=str(ulid()),
            origem = 'timon',
            destino = 'parnaiba',
            distancia = 12,
            valor = calcular(distancia=12),
            estado= 'requisitada'))
]


@app.get("/corridas")
def esportes_lista() -> list[Corrida]:
    return corridas



@app.post('/corridas')
def corrida_criar(corr: Corrida):
    corr = Corrida(id=str(ulid()),
                   origem= corr.origem,
                   destino = corr.destino,
                   distancia = corr.distancia,
                   valor = corr.valor,
                   estado = corr.estado)

    corridas.append(corr)

    return corr

@app.get('/corridas/{id}')
def corrida_detalhes(id: str) -> Corrida:
    # buscar na lista e retornar
    for co in corridas:
        if co.id == id:
            return co

    raise HTTPException(status_code=404, detail='Corrida não localizado!')

@app.put('/corridas/{id}')
def corrida_alterar(id: str, corrida : Corrida):
    for co in corridas:
        if id == co.id and ('requisitada' == co.estado.lower().split() or 'andamento' == co.estado.lower().split()):
            co.origem = corrida.origem
            co.destino = corrida.destino
            co.distancia = corrida.distancia
            co.valor = corrida.valor
            co.estado = corrida.estado
                
            return co
        else:
            return HTTPException(status_code=400, detail='O status da corrida tende a ser requisitada ou em andamento!')
        
    raise HTTPException(status_code=404, detail='Corrida não localizado!')

@app.post('/corridas/{id}')
def corrida_iniciar(corrida: Corrida):
    if corrida.estado.lower().split() == 'requisitada':
        for e in corridas:
            if e.id == id:
                e.estado = 'andamento'
            return Response(status_code=200)
        

@app.put('/corridas/{id}')
def corrida_finalizar(corrida: Corrida):
    if corrida.estado.lower().split() == 'andamento':
        for a in corridas:
            if id == a.id:
                a.estado = 'finalizada'

                return Response(status_code=200)
            
    raise(HTTPException(status_code=404, detail='Corrida não encontrada!'))

@app.delete('/corridas/{id}')
def corrida_remover(id: str):
    for e in corridas:
        if e.id == id:
            corridas.remove(e)
            return Response(status_code=204)

    raise HTTPException(status_code=404, detail='Corrida não localizado!')
