import uvicorn
import subprocess
import pandas as pd
import os
import re
from meus_dados.cadastro import Sistema
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse

app = FastAPI()

# Configurar as origens permitidas (ajuste conforme suas necessidades)
origins = [
    "http://localhost:5173",
    "http://localhost:8000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

sistema = Sistema()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/cadastro", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})


@app.get('/consulta', response_class=HTMLResponse)
async def my_query(request: Request):
    return templates.TemplateResponse('consulta.html', {'request': request})

security = HTTPBasic()


from fastapi.responses import JSONResponse

@app.get('/delete')
async def delete(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == "admin" and credentials.password == "password"):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    meus_dados = "meus_dados"
    dir_csv = os.path.join(meus_dados, 'dados.csv')
    
    df = pd.read_csv(dir_csv)
    df_dict = df.to_dict(orient='records')

    # Verifica o cabeçalho 'Accept' para decidir o tipo de resposta
    accept_header = request.headers.get('accept', '').lower()
    if 'application/json' in accept_header:
        # Retorna os dados como resposta JSON
        return JSONResponse(content=df_dict)
    else:
        # Renderiza o template HTML e passa os dados para serem exibidos no frontend
        return templates.TemplateResponse('delete.html', {"request": request, "data": df_dict}, media_type='text/html')





@app.post("/cadastro")
async def cadastrar(nome: str = Form(...), cpf: str = Form(...), nasc: str = Form(...)):
    errors = {}

    while True:
        nome_ok, error_msg = sistema.verifica_nome_ok(nome)
        if not nome_ok:
            errors['nome_label'] = error_msg
            return {'error': errors}


        cpf_ok, error_msg = sistema.ver_cpf_ok(cpf)
        if not cpf_ok:
            errors['cpf_label'] = error_msg
            return {'error': errors}

        nasc_ok, error_msg = sistema.ver_nasc_ok(nasc)
        if nasc_ok:
            break
        errors['nasc_label'] = error_msg
        return {'error': errors}

    # caminho
    meus_dados = "meus_dados"
    dir_csv = os.path.join(meus_dados, 'dados.csv')
    # gerando id
    try:
        # Ler o arquivo CSV existente
        df = pd.read_csv(dir_csv)

        # Obter o valor máximo do ID atual
        max_id = df['id'].max()

        # Calcular o próximo ID disponível
        next_id = max_id + 1
    except FileNotFoundError:
        # Se o arquivo CSV não existir, definir o próximo ID como 1
        next_id = 1
    except pd.errors.EmptyDataError:
        # Se o arquivo CSV estiver vazio, definir o próximo ID como 1
        next_id = 1
    # criando dicionario
    dados = {
        "id": next_id,
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": nasc
    }

    # Criar um DataFrame com os dados
    df = pd.DataFrame([dados])

    # Salvar o DataFrame em um arquivo CSV
    header = not (os.path.isfile(dir_csv) and os.stat(dir_csv).st_size > 0)
    df.to_csv(dir_csv, mode='a', header=header, index=False)
    return

@app.post("/consulta")
#async def consulta_nome(nome: str = Form(...)):
async def consulta(nome: str = Form(None), codigo: str = Form(None)):
    # caminho
    meus_dados = "meus_dados"
    dir_csv = os.path.join(meus_dados, 'dados.csv')

    if not nome and not codigo:
        return {'invalid_name': True, 'not_integer': True}

    elif nome and not codigo:
        if re.match(r'^[a-zA-Z\s]+$', nome):
            try:
                # Ler o arquivo CSV existente
                df = pd.read_csv(dir_csv)

                # Consultar se contem o valor da variavel no csv
                consulta = df[df['nome'].str.contains(nome, case=False)].to_dict(orient='records')
                print(consulta)
                return {'myquery': consulta}
            except FileNotFoundError:
                pass
            except pd.errors.EmptyDataError:
                pass
        else:
            return {'invalid_name': True}
    

    elif codigo and not nome:
        try:
            codigo = int(codigo)
            busca_id = True
        except ValueError:
            busca_id = False
            return {'not_integer': True}
        
        if busca_id:
            try:
                # Ler o arquivo CSV existente
                df = pd.read_csv(dir_csv)

                # Consultar se contem o valor da variavel no csv
                consulta = df[df['id'] == codigo].to_dict(orient='records')
                print(consulta)
                return {'myquery': consulta}
            except FileNotFoundError:
                pass
            except pd.errors.EmptyDataError:
                pass

class DeleteItemsRequest(BaseModel):
    selectedItems: list[int]

# Rota para excluir os itens selecionados
@app.post("/delete")
async def delete_items(request: DeleteItemsRequest):
    selected_items = request.selectedItems
    # Execute a lógica de exclusão dos itens selecionados aqui
    # Você pode usar o pandas para manipular o arquivo CSV e excluir os itens correspondentes
    
    # Exemplo de lógica de exclusão: removendo os itens selecionados do DataFrame
    meus_dados = "meus_dados"
    dir_csv = os.path.join(meus_dados, 'dados.csv')
    df = pd.read_csv(dir_csv)
    df = df[~df["id"].isin(selected_items)]
    df["id"] = range(1, len(df) + 1)
    df.to_csv(dir_csv, index=False)

    # Retorne uma resposta adequada após a exclusão
    return {"message": "Itens excluídos com sucesso"}


def start_servers():
    # Comando para iniciar o servidor FastAPI
    #fastapi_command = ["uvicorn", "main:app", "--reload"]
    fastapi_command = uvicorn.run("main:app", host="0.0.0.0", port=8000)

    # Caminho para a pasta do projeto React
    #react_dir = os.path.join(os.path.dirname(__file__), "fast_react")

    # Comando para iniciar o servidor React
    #react_command = ["npm", "run", "dev"]
    
    # Executar o comando do React no diretório do projeto React
    #react_process = subprocess.Popen(react_command, cwd=react_dir)

    # Executar o comando do FastAPI
    fastapi_process = subprocess.Popen(fastapi_command)

    # Aguardar o encerramento dos subprocessos
    fastapi_process.wait()
    #react_process.wait()

if __name__ == '__main__':
    start_servers()



