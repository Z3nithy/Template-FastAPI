# Template FastAPI

Template reutilizavel para iniciar APIs com **FastAPI**, **SQLAlchemy**, **Alembic** e autenticacao baseada em **JWT**. A estrutura separa configuracoes, acesso ao banco, endpoints e regras de negocio para que o projeto possa crescer sem concentrar tudo em um unico arquivo.

> **Estado atual:** este repositorio e uma base tecnica, nao um sistema pronto. A unica rota incluida e `GET /health`. Ainda nao existem modelos de negocio, CRUD ou um modelo `User`; esses elementos devem ser criados para cada aplicacao.

## Indice

- [O que voce encontra aqui](#o-que-voce-encontra-aqui)
- [Comecando](#comecando)
- [Configuracoes](#configuracoes)
- [Executando e testando](#executando-e-testando)
- [Como a aplicacao esta organizada](#como-a-aplicacao-esta-organizada)
- [Adicionando uma funcionalidade](#adicionando-uma-funcionalidade)
- [Banco de dados e migracoes](#banco-de-dados-e-migracoes)
- [Autenticacao e senhas](#autenticacao-e-senhas)
- [Problemas comuns](#problemas-comuns)
- [Antes de publicar](#antes-de-publicar)

## O que voce encontra aqui

- Aplicacao FastAPI com documentacao OpenAPI automatica.
- Configuracoes validadas por Pydantic Settings.
- Conexao e sessoes SQLAlchemy.
- Migracoes de banco com Alembic.
- Funcoes para criar e validar tokens JWT.
- Funcoes para gerar e verificar hashes de senha.
- Endpoint de verificacao `GET /health`.
- Testes automatizados com pytest.

## Comecando

Os comandos abaixo assumem que voce esta na pasta raiz do repositorio.

### 1. Criar e ativar um ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativacao, permita scripts apenas nesta janela:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

**Linux ou macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependencias

Para desenvolvimento, instale tambem as ferramentas de teste:

```bash
python -m pip install -r requirements-dev.txt
```

O arquivo `requirements-dev.txt` inclui `requirements.txt`; nao e necessario instalar os dois separadamente.

### 3. Criar o arquivo local de configuracao

Copie o exemplo para `.env`.

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**Linux ou macOS:**

```bash
cp .env.example .env
```

Gere uma chave secreta para o seu ambiente:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Substitua o valor de exemplo de `SECRET_KEY` no `.env` pela chave gerada. Nao compartilhe essa chave e nao envie o arquivo `.env` para o Git.

## Configuracoes

O arquivo [`.env.example`](.env.example) mostra as variaveis aceitas. Elas tambem podem ser fornecidas como variaveis de ambiente do sistema.

| Variavel | Obrigatoria | Padrao | Para que serve |
| --- | --- | --- | --- |
| `DATABASE_URL` | Nao | `sqlite:///./database.db` | URL de conexao com o banco SQLAlchemy. |
| `SECRET_KEY` | **Sim** | Nenhum | Chave usada para assinar tokens JWT; precisa ter pelo menos 32 caracteres. |
| `ALGORITHM` | Nao | `HS256` | Algoritmo utilizado pelo JWT. |
| `DEBUG` | Nao | `false` | Ativa o modo debug, o log de SQL e o reload do `python main.py`. |

As configuracoes sao carregadas e validadas em [`core/config.py`](core/config.py). A aplicacao nao inicia se `SECRET_KEY` estiver ausente ou for curta demais. O exemplo do `.env.example` e apenas um marcador: substitua-o antes de usar a aplicacao fora de um ambiente local de teste.

## Executando e testando

### Iniciar em desenvolvimento

```bash
uvicorn main:app --reload
```

O servidor fica disponivel em `http://127.0.0.1:8000`. O parametro `--reload` e uma opcao do comando acima; para iniciar pelo script, use `python main.py` (o reload pelo script depende de `DEBUG=true`).

### Rotas existentes

| Metodo | Caminho | Resultado |
| --- | --- | --- |
| `GET` | `/health` | Retorna `{"status": "ok"}` se a aplicacao respondeu. |

O FastAPI gera a documentacao interativa em:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Executar os testes

```bash
pytest
```

Os testes existentes verificam configuracoes, tokens JWT, hash de senhas e a rota de saude. Os testes usam valores de ambiente proprios definidos em [`tests/conftest.py`](tests/conftest.py), sem exigir uma chave real.

## Como a aplicacao esta organizada

```text
.
├── core/                 Configuracoes, JWT e hash de senhas
├── database/             Engine, Base SQLAlchemy e sessao por requisicao
├── dependencies/         Dependencias reutilizaveis do FastAPI
├── enums/                Enumeracoes do dominio da aplicacao
├── models/               Modelos/tabelas SQLAlchemy
├── routes/               Endpoints HTTP e routers
├── schemas/              Formatos de entrada e saida da API
├── services/             Regras de negocio
├── migrations/           Configuracao e historico de migracoes Alembic
├── tests/                Testes automatizados
├── main.py               Criacao da aplicacao e registro de rotas
├── alembic.ini           Configuracao do Alembic
├── requirements.txt      Dependencias necessarias para executar
└── requirements-dev.txt  Dependencias de execucao e de desenvolvimento
```

### Caminho de uma requisicao

Uma rota recebe a requisicao HTTP, valida os dados com um schema, chama o servico responsavel pela regra de negocio e, quando necessario, usa uma sessao do banco para ler ou gravar modelos. A resposta e convertida para o formato definido pelo schema de saida.

```text
Cliente HTTP -> routes -> schemas / services -> models / database
                    -> resposta HTTP
```

Responsabilidades recomendadas:

- **`routes/`**: caminhos HTTP, codigos de resposta e dependencias FastAPI. Evite colocar regras de negocio extensas aqui.
- **`schemas/`**: validacao e formato dos dados recebidos e devolvidos pela API. Schemas Pydantic nao sao tabelas do banco.
- **`services/`**: regras de negocio e coordenacao de operacoes.
- **`models/`**: estrutura persistida no banco por meio do SQLAlchemy.
- **`database/`**: engine, classe declarativa `Base` e dependencia `get_db`.
- **`dependencies/`**: recursos que o FastAPI injeta em rotas, como usuario autenticado ou sessao do banco.
- **`core/`**: configuracoes e utilitarios transversais, nao especificos de um dominio.

## Adicionando uma funcionalidade

Ao implementar um recurso de negocio, siga esta ordem:

1. **Defina o modelo** em `models/` se os dados precisarem ser persistidos.
2. **Defina os schemas** em `schemas/` para validar a entrada e controlar os campos da resposta.
3. **Implemente a regra** em `services/`; mantenha a rota focada na comunicacao HTTP.
4. **Crie a rota** em `routes/`, usando `Depends(get_db)` quando precisar do banco.
5. **Registre o router** em `main.py` com `app.include_router(...)`.
6. **Crie ou atualize testes** para os casos esperados e os erros importantes.
7. Se adicionou ou alterou modelos, **gere e aplique uma migracao** conforme a proxima secao.

Use nomes que indiquem o recurso e mantenha os arquivos pequenos e focados. Antes de criar um helper novo, veja se a funcionalidade ja existe em `core/`, `database/` ou `dependencies/`.

### Exemplo: registrar um router

Este exemplo mostra apenas como conectar um router novo a aplicacao; ele nao e uma rota de negocio que ja exista no template.

Em `routes/itens.py`:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/itens", tags=["itens"])


@router.get("/")
def listar_itens() -> list[dict[str, str]]:
    return [{"nome": "Exemplo"}]
```

Em `main.py`, importe e registre o router depois de criar `app`:

```python
from routes.itens import router as itens_router

app.include_router(itens_router)
```

Ao reiniciar a aplicacao, a rota de exemplo aparece em `/docs` como `GET /itens/`. Para um recurso real, substitua o dado fixo por schemas, servicos e acesso ao banco conforme necessario.

## Banco de dados e migracoes

[`database/db.py`](database/db.py) cria o `engine`, a classe declarativa `Base`, a fabrica `SessionLocal` e a dependencia `get_db`. O `get_db` fornece uma sessao durante a requisicao e a fecha ao terminar.

**A aplicacao nao cria nem altera tabelas automaticamente ao iniciar.** O historico do schema e controlado pelo Alembic. O diretorio `migrations/versions/` comeca vazio porque ainda nao ha modelos de negocio neste template.

### Depois de adicionar um modelo

1. Garanta que o modelo herde de `Base` e que o modulo seja importado durante o carregamento das migracoes. Uma opcao e exportar os modelos em `models/__init__.py` e importar `models` em `migrations/env.py`; outra e importar explicitamente cada modulo de modelo em `env.py`.
2. Gere uma migracao:

   ```bash
   alembic revision --autogenerate -m "create item table"
   ```

3. **Abra e revise o arquivo gerado** em `migrations/versions/`. O autogenerate compara o metadata carregado com o banco e pode nao reconhecer toda mudanca desejada.
4. Aplique a migracao:

   ```bash
   alembic upgrade head
   ```

Comandos uteis:

```bash
alembic current          # revisao aplicada no banco atual
alembic history          # historico de revisoes
alembic downgrade -1     # desfaz a ultima revisao
```

Nao edite uma migracao que ja foi aplicada em ambientes compartilhados. Crie uma nova revisao para mudancas futuras. Antes de executar `downgrade`, confira o que a migracao remove; desfazer uma migracao pode causar perda de dados.

## Autenticacao e senhas

- [`core/senha_hash.py`](core/senha_hash.py) expoe `criar_hash_senha` e `verificar_senha`. Persista o hash, nunca a senha original.
- [`core/jwt.py`](core/jwt.py) expoe `criar_token_acesso` e `verificar_token_acesso`. O token atual guarda o identificador do usuario em `sub` e expira apos 60 minutos.
- [`dependencies/autenticacao.py`](dependencies/autenticacao.py) contem a dependencia `get_usuario_atual`, que valida o token e procura o usuario no banco.

**A dependencia de autenticacao ainda precisa de um modelo de usuario:** ela espera que `models` disponibilize `User` com um campo `id`. Como este template nao inclui esse modelo, crie e exporte `User` em `models/__init__.py` antes de importar ou usar `get_usuario_atual` nas rotas. Tambem crie a migracao correspondente.

As funcoes JWT usam `SECRET_KEY` e `ALGORITHM` das configuracoes. Mantenha a chave privada, longa e diferente entre ambientes; se ela for exposta, substitua-a e considere os tokens existentes comprometidos.

## Problemas comuns

| Sintoma | O que verificar |
| --- | --- |
| Erro de validacao mencionando `SECRET_KEY` | Crie o `.env`, substitua o valor de exemplo por uma chave com pelo menos 32 caracteres e confirme que o comando esta sendo executado na raiz do projeto. |
| `alembic revision --autogenerate` nao encontra uma tabela | Confirme que o modelo herda de `Base` e que seu modulo foi importado antes de `target_metadata` em `migrations/env.py`. |
| A tabela nao aparece depois de criar um modelo | Gere e aplique a migracao com `alembic upgrade head`; iniciar a API nao cria tabelas automaticamente. |
| Erro `cannot import name 'User'` ao usar autenticacao | Crie o modelo `User` e exporte-o em `models/__init__.py`, conforme descrito em [Autenticacao e senhas](#autenticacao-e-senhas). |
| `/docs` nao abre | Confirme que o servidor iniciou sem erros e que esta usando o endereco e a porta mostrados no terminal. |

## Antes de publicar

- Configure `SECRET_KEY` segura fora do repositorio; nunca use a chave de exemplo.
- Defina `DEBUG=false` e nao exponha logs detalhados em producao.
- Configure o `DATABASE_URL` do ambiente e aplique as migracoes antes de iniciar as novas versoes.
- Revise autenticacao, autorizacao, validacao de entrada, CORS e tratamento de erros de acordo com a aplicacao.
- Execute `pytest` e revise as migracoes antes de implantar.
- Configure logs, monitoramento, backups e politica de rotacao de segredos conforme o ambiente.
