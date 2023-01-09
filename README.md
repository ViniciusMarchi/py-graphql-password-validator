
<details>
<summary>Tabela de Conteúdos</summary>

<!-- # Tabela de conteúdos -->
* [O projeto](#o-projeto)
    * [Fluxo de dados](#fluxo-dos-dados)
* [Executando o projeto](#executando-o-projeto) 
    * [Com Docker](#com-docker)
    * [Sem Docker](#sem-docker)
* [Consumindo a API](#consumindo-a-api)
    * [Formato da Query](#formato-da-query)
    * [Formato das Regras](#formato-das-regras)
* [Testes de unidade e integração](#testes-de-unidade-e-de-integração)
* [Estrutura de diretórios](#estrutura-de-diretórios-do-projeto)
</details>

# O projeto
API GraphQL que realiza a validação de senha se baseando em um conjunto de regras de validação de senha escolhidas pelo usuário.

Principais tecnologias utilizadas:
* Python 3.10
* [Strayberry](https://strawberry.rocks/)
* Docker
* FastAPI

## Fluxo dos dados
![Diagrama do fluxo de dados da API](./assets/api-flow-diagram.png)

O fluxo de dados (demonstrado pela figura acima), de maneira simplificada, é definido da seguinte maneira: o usuário realiza uma `query` informando uma senha e um conjunto de regras de validação de senha. As regras escolhidas pelo usuário serão utilizadas para validar a senha informada.

A `query` é recebida pelo `resolver`, o qual extrai os dados da query e os representa dentro da API, posteriormente repassa os dados para o `input check`, módulo responsável por validar se o formato dos dados estão corretos. Por exemplo, no caso das regras, elas podem ser uma lista vazia `[]` (nesse cenário toda senha será válida), entretanto, quando definidas, devem respeitar o formato `{ rule: <NOME_DA_REGRA>, value: <VALOR_DA_REGRA> }`. Como exemplo, uma regra sem campo `<value>` (ex: `{ rule: <regra> }`) não respeita o formato esperado, logo é inválida. Outro ponto observado é o campo `<value>`. Esse campo não aceita valores negativos por definição, por exemplo, imagine que a regra escolhida é que a senha possua um número minímo de digitos, logo, não faz sentido que uma senha tenha no mínimo -1 dígito, por isso números negativos como valores de regras não são aceitos.

Se o formato do input não for respeitado um erro descritivo do problema é informado ao usuário. Se os dados estiverem no formato correto o fluxo continua e eles serão repassados para o módulo que valida a senha de fato, o `password validator`, que verifica se a senha cumpre as regras stabelecidas pelo usuário, o resultado desse processo é enviado ao usuário como resposta.

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

# Consumindo a API
## Formato da query

Para consumir a API basta constrir uma query GraphQL no formato demonstrado abaixo. A query é usada para validar uma senha com base em um conjunto de regras.

```graphql
{
  verify(
    password:"<PASSWORD>",
    rules: [{rule:"<RULE_NAME>", value: <RULE_VALUE>}]
  ) {
    verify
    noMatch
  }
}
```
### Argumentos
Ela consiste em um único campo chamado `verify`, que recebe dois argumentos: `password` e `rules`.

* `password (string)`: representa a senha a ser verificada.
* `rules (list[object])`: contém uma lista de objetos especificando as regras a serem aplicadas à senha. Cada objeto possui dois campos:
    * `rule (string)`: representa o nome da regra.
    * `value (int)`: representa o valor da regra.

### Fields
Para usar essa query basta substituir os placeholders `<PASSWORD>`, `<RULE_NAME>` e `<RULE_VALUE>` pelos valores desejados. O formato das regras é descrito abaixo [Formato da Regra](#Formato-da-regra)

O resultado retornado é um objeto com dois campos: `verify` e `noMatch`.

* `verify (boolean)`: resultado da validação da senha. `True` se a senha for válida, `False` se for inválida.
* `noMatch (list[string])`: lista de regras que não foram satisfeitas pela senha. Se a senha for válida essa lista estará vazia.

## Formato das regras
As regras para validar as senhas possuem o seguinte formato:

`{rule:<RULE_NAME>, value: <RULE_VALUE>}`

Rule é uma `string` e representa o nome da regra. Os valores são inteiros positivos.

A tabela abaixo exibe as regras disponíveis para a validação de senha.

| nome da regra          | valores aceitos                        | descrição |
| ------------- | ---------------------------- | ---------------------------- |
`minSize`         | inteiro positivo (ex: 1,2,3,4...) | define um tamanho mínimo
`minUppercase`    | inteiro positivo | define uma quantidade mínima de letras maíusculas
`minLowercase`    | inteiro positivo | define uma quantidade mínima de letras minúsculas
`minDigit`        | inteiro positivo | define uma quantidade mínima de digitos (0-9)
`minSpecialChars` | inteiro positivo | define uma quantiade mínima de caracteres especiais (ex: `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `(`, `)`, `-`,`+`,`/`,`{`,`}`,`[`,`]`)
`noRepeted`       | inteiro positivo (esse valor será ignorado) | define que dois ou mais caracteres sequencias não devem se repetir (ex: senha é válido, mas seenha não, pois o caractere `e` se repetiu de maneira sequencial)

# Testes de unidade e de integração
O projeto é coberto por testes de unidade e de integração. Para executar os testes basta rodar o script contido na raiz do projeto, com o seguinte comando
```bash
python3 run_tests.py
```

# Estrutura de diretórios do projeto
```
.
├─ model                          // modelos graphql
│ └── password_info.py
│
├─ password
│ └── valid_pass.py               // verifica se a senha cumpre as regras estipuladas
│
├─ resolver                       // implementação dos resolvers para o schema
│ └── verify.py
│
├─ schema
│ └── schema.py                   // schema graphql que define a api
│
├─ tests                          // testes unitários e de integração
│ ├── test_check_input_password.py
│ ├── test_check_input_rules.py
│ ├── test_integration.py
| └── test_validpass.py
│
├─ utils
│ ├── check_input_password.py      // valida o formato do input da senha
| └── check_input_rules.py         // valida o formato do input das regras
│
├─ api.py                          // entry point da API
├─ docker-compose.yml              // define a construção do container
├─ Dockerfile                      // define a construção da imagem docker
├─ README.md
├─ requirements.txt                // pacotes utilizados no projeto
└─ run_tests.py                    // script que executa os testes
```