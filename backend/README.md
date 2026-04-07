# UmlAramigo Backend API

API FastAPI para plataforma de doação de pets (cães e gatos).

## Features

- ✅ Autenticação JWT com Pydantic
- ✅ SQLAlchemy + PostgreSQL
- ✅ Alembic para migrações
- ✅ Swagger/OpenAPI documentation
- ✅ Service layer pattern
- ✅ Schemas com Pydantic
- ✅ CORS habilitado

## Funcionalidades

1. **Organizações**: Pessoas podem criar organizações que fazem doação de pets
2. **Pets**: Cadastro de pets para adoção (cachorro, gato)
3. **Formulários de Interesse**: Outras pessoas podem preencher com nome e telefone para expressar interesse

## Setup

### 1. Criar Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e ajuste as configurações:

```bash
cp .env.example .env
```

Atualize as variáveis:

```
SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=postgresql://user:password@localhost:5432/umlaramigo
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Configurar Banco de Dados PostgreSQL

```bash
createdb umlaramigo
```

### 5. Rodar Migrações

```bash
# Gerar uma migração automática
alembic revision --autogenerate -m "Initial migration"

# Aplicar migrações
alembic upgrade head
```

### 6. Iniciar Servidor

```bash
python run.py
```

Acesse a documentação em: http://localhost:8000/docs

## Estrutura do Projeto

```
backend/
├── app/
│   ├── core/           # Configurações, segurança, banco de dados
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Schemas Pydantic
│   ├── services/       # Camada de negócio
│   ├── routes/         # Endpoints FastAPI
│   ├── utils/          # Utilitários (dependências, etc)
│   └── main.py         # FastAPI app
├── alembic/            # Migrações de banco de dados
├── requirements.txt    # Dependências
├── .env.example        # Exemplo de variáveis
└── run.py              # Script para iniciar servidor
```

## API Endpoints

### Autenticação

- `POST /auth/register` - Registrar novo usuário
- `POST /auth/login` - Login (retorna token JWT)

### Organizações

- `POST /organizations/` - Criar organização
- `GET /organizations/` - Listar todas as organizações
- `GET /organizations/my-organizations` - Listar organizações do usuário autenticado
- `GET /organizations/{org_id}` - Obter detalhes da organização
- `PUT /organizations/{org_id}` - Atualizar organização
- `DELETE /organizations/{org_id}` - Deletar organização

### Pets

- `POST /pets/?org_id=1` - Cadastrar novo pet
- `GET /pets/` - Listar todos os pets
- `GET /pets/organization/{org_id}` - Listar pets de uma organização
- `GET /pets/{pet_id}` - Obter detalhes do pet
- `PUT /pets/{pet_id}` - Atualizar pet
- `DELETE /pets/{pet_id}` - Deletar pet

### Formulários de Interesse

- `POST /interests/?pet_id=1` - Criar formulário de interesse
- `GET /interests/` - Listar todos os formulários
- `GET /interests/user/my-interests` - Listar formulários do usuário
- `GET /interests/pet/{pet_id}` - Listar formulários para um pet específico
- `DELETE /interests/{interest_id}` - Deletar formulário

## Autenticação

A API usa JWT (JSON Web Tokens) para autenticação.

### Exemplo de Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

Resposta:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2024-03-22T10:30:00"
  }
}
```

### Usar Token em Requisições

```bash
curl -X GET "http://localhost:8000/organizations/my-organizations" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Esquemas de Dados

### User

- `id`: int
- `email`: str (único)
- `full_name`: str
- `is_active`: bool
- `created_at`: datetime

### Organization

- `id`: int
- `name`: str
- `description`: str (opcional)
- `owner_id`: int (FK)
- `created_at`: datetime

### Pet

- `id`: int
- `name`: str
- `pet_type`: enum (dog, cat)
- `description`: str (opcional)
- `organization_id`: int (FK)
- `created_at`: datetime

### InterestForm

- `id`: int
- `full_name`: str
- `phone`: str
- `user_id`: int (FK)
- `pet_id`: int (FK)
- `created_at`: datetime

## Troubleshooting

### Erro de conexão com banco de dados

- Verifique se PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`
- Verifique se o banco de dados foi criado

### Erro ao rodar migrações

- Confirme que está no diretório backend
- Verifique se o ambiente virtual está ativado
- Tente: `alembic current`

## Desenvolvimento

Para adicionar novos recursos:

1. Crie o modelo em `app/models/`
2. Crie o schema em `app/schemas/`
3. Crie o service em `app/services/`
4. Crie as rotas em `app/routes/`
5. Inclua o router em `app/main.py`
6. Gere uma migração: `alembic revision --autogenerate -m "descrição"`
