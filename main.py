import uvicorn
import pandas as pd
import os
import re
from meus_dados.cadastro import Sistema
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
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

@app.get('/delete', response_class=HTMLResponse)
async def del_cad(request:Request):
    return templates.TemplateResponse('del_cad.html', {'request': request})


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
        



if __name__ == '__main__':
    uvicorn.run(app)
