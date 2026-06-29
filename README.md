# Gestão de Franquias - API
Porjeto Backend (API REST) para gestão de uma rede de franquias de restaurantes, desenvolvida como trabalho acadêmico.

## Swagger produção
O projeto está publicado e pode ser acessado (sem necessidade de rodar localmente):

**Swagger:** https://gestao-franquia-api.onrender.com/docs

## Sobre o projeto
Sistema backend que simula o gerenciamento de franquias, contemplando os módulos:

- **Autenticação** (`/auth`) - login com JWT
- **Usuários** (`/usuarios`) - cadastro e gestão (admin, gerente, atendente)
- **Unidades** (`/unidades`) - filiais da franquia
- **Produtos** (`/produtos`) - catálogo geral
- **Cardápios** (`/cardapios`) - cardápios por período, vinculados às unidades
- **Estoque** (`/estoque`) - controle por unidade
- **Pedidos** (`/pedidos`) - criação e acompanhamento
- **Pagamentos** (`/pagamentos`) - gateway mock (taxa de aprovação configurável)
- **Fidelidade** (`/fidelidade`) - acúmulo e resgate de pontos

## Tecnologias Utilizadas

- **Python 3.12 + FastAPI**
- **SQLAlchemy 2 (ORM) + Alembic (migrations)**
- **PostgreSQL 16**
- **Pydantic v2 (validação)**
- **JWT (autenticação)**
- **Docker + Docker Compose**
- Deploy: **Render** (API) + **Neon** (PostgreSQL) - Plano Free. A 1ª requisição pode demorar 

## Arquitetura
Arquitetura em camadas seguindo Arquitetura Limpa(Clean Architecture)

backend/app/
├── api/v1/             # Endpoints (rotas FastAPI)
├── application/        # Regras de negócio (services)
├── core/               # Configurações e segurança
├── domain/
│   ├── models/         # Entidades SQLAlchemy
│   └── enums.py
├── infrastructure/
│   ├── repositories/   # Acesso a dados
│   └── gateway/        # Integração de pagamento (mock pagamento)
├── schemas/            # Pydantic requests/response (DTOs)
└── main.py             #Ponto de entrada FastAPI


## Como rodar localmente

### Pré-requisitos
- Docker Desktop instalado e em execução

### Passo-a-passo
1. Clone o repositório:
   git clone https://github.com/gpbarreiros/GestaoDeFranquia.git
   
   
2. Crie o arquivo `.env` dentro de `backend/` baseado no `.env.example`:
   cp backend/.env.example backend/.env
   
3. Crie os containers (API + PostgreSQL):
   docker compose up --build   

4. Acesse:
   - **Swagger:** http://localhost:8000/docs
   - **Health check:** http://localhost:8000/health

### Para rodar migrations manualmente (se necessário)
docker compose exec api alembic upgrade head

### Também é possivel acessar Swagger do projeto Publico em:
**Swagger:** https://gestao-franquia-api.onrender.com/docs


## Como testar (passo a passo)
0. Acessra Swagger ou Rodar Projeto localmente

## Para Projeto Local seguir os passos:
http://localhost:8000/docs
1. **Criar usuário** em `POST /usuarios` (role `ADMIN`)
2. **Fazer login** em `POST /auth/login` → copiar o token retornado
3. No Swagger, clicar em **Authorize** e colar o token
4. **Cadastrar uma unidade** em `POST /unidades`
5. **Cadastrar produtos** em `POST /produtos`
6. **Criar um cardápio** em `POST /cardapios` e vincular produtos/unidade
7. **Criar um pedido** em `POST /pedidos`
8. **Processar o pagamento** em `POST /pagamentos` → o mock aprova ~80% das vezes
9. **Consultar pontos de fidelidade** em `GET /fidelidade/me` (creditados automaticamente em pagamentos aprovados)

## Para Projeto Publicado seguir os passos:
https://gestao-franquia-api.onrender.com/docs
1. **Logar com usuário Adminitrador** em `POST /usuarios` 
      ## "email": "avaliador@gestaofranquia.com.br",
      ## "senha": "Avaliador@trabalhofinal2026",
2. **Fazer login** em `POST /auth/login` → copiar o token retornado
3. Na pagina do Swagger, clicar em **Authorize** e colar o token Beare para autenticar
4. **Cadastrar uma ou mais unidades** em `POST /unidades`
5. **Cadastrar produtos por unidade** em `POST /produtos`
6. **Criar um ou mais cardápios** em `POST /cardapios` e vincular produtos/unidade
7. **Criar um ou mais pedidos** em `POST /pedidos`
8. **Processar o pagamento do pedido** em `POST /pagamentos` → mock de pagamento
9. **Consultar pontos de fidelidade** em `GET /fidelidade/me` (Pontos gerado automaticamente após pagamento aprovado)

## Regras de negócio implementadas
- Apenas usuários com role `ADMIN` ou `GERENTE` podem criar/atualizar cardápios e produtos
- Cardápio inativo não pode ter seus itens consultados
- Pedido só aceita pagamento quando está em status `AGUARDANDO_PAGAMENTO`
- Pedido já com pagamento aprovado não pode ser pago novamente
- Pagamento aprovado dispara o crédito de pontos de fidelidade (1 ponto por R$ 1,00 do total)
- Resgate de pontos valida saldo disponível antes de debitar
- Todas as ações sensíveis geram log de auditoria

##Autora
**Gabriella Pereira Barreiros** 

Projeto: Desenvolvimento Back-end.
