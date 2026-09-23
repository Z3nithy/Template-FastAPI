# Template FastAPI

Template base para a construção de APIs utilizando **FastAPI**, **SQLAlchemy** e autenticação baseada em **JWT**.

O projeto reúne uma estrutura inicial reutilizável para novos sistemas. A configuração da aplicação, a conexão com o banco de dados, o controle de sessões, o hash de senhas e a autenticação já estão organizados em módulos separados, permitindo que cada novo projeto evolua a partir desta base.

## Objetivo

Este repositório não representa uma aplicação de negócio específica. Ele funciona como um ponto de partida para APIs que precisem de:

- aplicação web com FastAPI;
- persistência de dados com SQLAlchemy;
- gerenciamento de configurações por variáveis de ambiente;
- criação e validação de tokens JWT;
- armazenamento seguro de senhas;
- dependências para identificar o usuário autenticado;
- separação entre modelos, schemas, rotas, serviços e enums.

As pastas de domínio estão preparadas para receber as entidades e regras específicas de cada sistema construído a partir deste template.

## Estrutura do projeto

```text
Template-FastAPI/
├── core/
│   ├── config.py       # Configurações carregadas do ambiente
│   ├── jwt.py          # Criação e validação de tokens JWT
│   └── senha_hash.py   # Hash e verificação de senhas
├── database/
│   ├── db.py           # Engine, sessão, Base e dependência do banco
│   └── __init__.py
├── dependencies/
│   ├── autenticacao.py # Recuperação do usuário autenticado
│   └── __init__.py
├── enums/              # Enumerações do domínio
├── models/             # Modelos SQLAlchemy
├── routes/             # Rotas e routers da API
├── schemas/            # Schemas Pydantic de entrada e saída
├── services/           # Regras de negócio e serviços da aplicação
├── main.py             # Ponto de entrada da aplicação
├── requirements.txt    # Dependências do projeto
└── .env                # Configurações locais, não versionadas
```

## Tecnologias utilizadas

- [FastAPI](https://fastapi.tiangolo.com/): criação da API e documentação automática;
- [Uvicorn](https://www.uvicorn.org/): servidor ASGI;
- [SQLAlchemy](https://www.sqlalchemy.org/): comunicação com o banco de dados;
- [python-jose](https://python-jose.readthedocs.io/): geração e validação de JWT;
- [pwdlib](https://frankie567.github.io/pwdlib/): hash seguro de senhas;
- [python-dotenv](https://github.com/theskumar/python-dotenv): carregamento das variáveis do arquivo `.env`.

## Configuração do ambiente

### 1. Criar e ativar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite:///./database.db
SECRET_KEY=altere-esta-chave-por-um-valor-seguro
ALGORITHM=HS256
```

Em ambientes reais, utilize uma chave longa, aleatória e exclusiva para cada ambiente. O arquivo `.env` já está listado no `.gitignore` e não deve ser enviado ao controle de versão.

## Executando a aplicação

Com o ambiente virtual ativado, execute:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs` para a documentação Swagger;
- `http://127.0.0.1:8000/redoc` para a documentação ReDoc.

Também é possível iniciar pelo próprio arquivo principal:

```bash
python main.py
```

## Componentes principais

### Configuração

O módulo `core/config.py` carrega as configurações do arquivo `.env` por meio de variáveis de ambiente. Dessa forma, informações específicas de cada ambiente não ficam fixas no código.

### Banco de dados

O módulo `database/db.py` centraliza:

- a criação do `engine` do SQLAlchemy;
- a classe declarativa `Base` usada pelos modelos;
- a fábrica de sessões `SessionLocal`;
- a dependência `get_db`, que abre e fecha a sessão por requisição.

Ao iniciar a aplicação, `main.py` executa `Base.metadata.create_all` para criar as tabelas registradas nos modelos.

### Segurança

O módulo `core/senha_hash.py` disponibiliza funções para criar e verificar hashes de senha. A senha original não deve ser armazenada no banco.

O módulo `core/jwt.py` cria tokens de acesso com identificação do usuário no campo `sub` e prazo de expiração. A dependência `get_usuario_atual`, em `dependencies/autenticacao.py`, lê o token enviado no header `Authorization`, valida suas informações e recupera o usuário correspondente.

## Como evoluir o template

Para iniciar um novo domínio de negócio a partir desta base, a organização recomendada é:

1. Criar os modelos SQLAlchemy em `models/`.
2. Criar os schemas de entrada e saída em `schemas/`.
3. Implementar as regras de negócio em `services/`.
4. Criar os endpoints em `routes/`.
5. Registrar os routers em `main.py`.
6. Adicionar enums específicos em `enums/`, quando necessário.
7. Criar testes para os serviços e endpoints adicionados.

Essa separação mantém as rotas focadas no protocolo HTTP e concentra as regras da aplicação nos serviços, facilitando manutenção e expansão.

## Observações

- O template fornece a fundação técnica; modelos, endpoints e regras de negócio devem ser definidos conforme o sistema que será construído.
- As chaves e credenciais do ambiente devem permanecer fora do código-fonte.
- Em projetos maiores, recomenda-se adicionar migrations, como Alembic, em vez de depender apenas de `Base.metadata.create_all`.
- Antes de publicar a API, configure CORS, logs, tratamento de erros, validações e testes de acordo com os requisitos do projeto.
