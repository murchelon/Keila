Criar venv:
python -m venv venv-keila

Ativar:
venv-keila\Scripts\activate

deactivate

pip install -r src/requirements.txt

uvicorn main:app --host 0.0.0.0 --reload --port 56789


## Como rodar com Docker

### Build da imagem
docker build -t keila .

### Rodar o container
docker run --rm -p 5000:5000 keila

### Ou com docker-compose
docker-compose up --build

