# Executando o projeto

## Com Docker
Garanta que dependências necessárias estão instaladas, sendo elas: Docker e Docker Compose (opcional, pois auxilia na construção da imagem e do container, mas essa ação pode ser feita manualmente).

Com o Docker Compose instalado acesse a pasta raiz do projeto e execute:
```bash
docker-compose up
```

Aguarde a construção da imagem e do container, após o processo completo a API estará disponível em http://localhost:8000/graphql

Obs: Se você optou por não utilizar o Docker Compose não há problemas, ainda é possível  construir o container manualmente com os seguintes comandos:

1. Construa a imagem
```bash
docker build -t <image-name> .
```

2. Depois, construa o container
```bash
docker run -p 8000:8000 <image-name>
```
Ao final, também obteremos a API executando em http://localhost:8000/graphql

## Sem docker
Certifique-se de possuir Python na versão 3.10.6 ou superior. Após isso, acesse a pasta raiz do projeto e instale as dependências com o comando:
```bash
pip install -r requirements.txt
```

Aguarde as dependências baixarem e execute:
```bash
uvicorn api:app --reload
```

Após isso, o servidor estará disponível em http://localhost:8000/graphql

# Testes de unidade e de integração
O projeto em é coberto por testes de integração. Para executar os testes basta rodar o script contido na raiz do projeto, com o seguinte comando
```bash
python3 run_tests.py
```