
# Minha API

Este projeto faz parte do material didático das disciplinas do curso **Desenvolvimento Full Stack**.  
O objetivo é ilustrar os conceitos apresentados ao longo das aulas do módulo **Sprint I**.

# Estrutura do Projeto
  ```bash


backend_api/
|-- app.py
|-- clientes.db
|-- README.md
|-- requiriments.txt
|-- /static
    |-- swagger.json
frontend/
|-- /imagens
|-- cadastro.html
|-- home.html
|-- veiculos.html
|-- script.js
|-- style.css
|-- README.md
```

# Como executar
Será necessário ter todas as bibliotecas Python listadas no `requirements.txt` instaladas.  
Após clonar o repositório, acesse o diretório raiz pelo terminal para executar os comandos descritos abaixo.

É fortemente recomendado o uso de ambientes virtuais como [virtualenv] (https://virtualenv.pypa.io/en/latest/installation.html) para isolar as dependências do projeto.


# Configurando o Ambiente Virtual
```bash
(env)$ python -m venv venv # cria ambiente virtual
(env)$ source venv/bin/activate  # No Linux/macOS
venv\Scripts\activate  # No Windows
``` 

# Instalando Dependências
``` 
Para instalar as dependências listadas no arquivo requirements.txt, utilize o seguinte comando:
```
```bash
pip install -r requirements.txt
```


# Executando a API
A API cria automaticamente um banco de dados caso não exista. No entanto, um banco de dados com aproximadamente 20 clientes pré-cadastrados foi incluído para facilitar os testes das rotas (GET, POST, PUT, DELETE).

Para executar a API, utilize o comando:
```bash
flask run --host 0.0.0.0 --port 5000
```


# Modo de Desenvolvimento
Durante o desenvolvimento, é recomendado utilizar o parâmetro --reload. Isso permite que o servidor reinicie automaticamente ao detectar alterações no código:
```bash
flask run --host 0.0.0.0 --port 5000 --reload
```


# Acessando a API
Após iniciar o servidor, acesse http://localhost:5000 no navegador para verificar o status da API em execução.


# Documentação da API via Swagger

Para acessar a documentação Swagger da API, acesse http://localhost:5000/swagger.


# Exemplos de Uso da API

```
```bash


Listar Clientes
GET /clientes
Exemplo de Resposta:
[
    {
        "id": 1,
        "nome": "João Silva",
        "cpf": "12345678901",
        "dt_nasc": "1990-01-01",
        "logradouro": "Rua A",
        "cep": "12345678",
        "cidade": "Cidade A",
        "uf": "SP"
    }
]
```
```bash


Cadastrar Cliente
POST /clientes
Corpo da Solicitação:
{
    "nome": "Maria Souza",
    "cpf": "98765432100",
    "dt_nasc": "1995-05-15",
    "logradouro": "Rua B",
    "cep": "87654321",
    "cidade": "Cidade B",
    "uf": "RJ"
}

```
```bash


Exemplo de Resposta:
{
    "message": "Cliente cadastrado com sucesso!"
}

```
```bash


Atualizar Cliente
PUT /clientes/{id}
Corpo da Solicitação:
{
    "nome": "Maria Souza Atualizada",
    "cpf": "98765432100",
    "dt_nasc": "1995-05-15",
    "logradouro": "Rua B",
    "cep": "87654321",
    "cidade": "Cidade B",
    "uf": "RJ"
}

```
```bash


Deletar Cliente
DELETE /clientes/{id}
Exemplo de Resposta:
{
    "message": "Cliente removido com sucesso!"
}
