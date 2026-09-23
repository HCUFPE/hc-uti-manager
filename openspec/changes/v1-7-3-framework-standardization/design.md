# Design: v1.7.3 - Padronização com Framework SETISD (Proteção de Rotas, Auditoria e Central de Segredos)

## Context

O sistema `HC UTI Manager` precisa adotar o padrão de qualidade e segurança do **Framework SETISD**. Recentemente, a rota `alta.py` executava sem a injeção global de dependência de autenticação do router (`Default-Private Router Pattern`), necessitando regularização. Além disso, ações críticas no sistema de internação e alta médica necessitam de um registro auditável imutável com rastreabilidade de estado (JSON `estado_anterior` e `estado_novo`), categorizado em `SEGURANCA`, `NEGOCIO_CLINICO` ou `CONFIGURACAO`. Por fim, a inicialização do servidor backend deve validar rigorosamente o arquivo `.env` para evitar subidas em produção com chaves fracas ou inconsistentes.

## Goals / Non-Goals

**Goals:**
- Implementar o padrão **Default-Private Router** no router `src/routers/alta.py`.
- Criar o modelo SQLAlchemy `AuditLog` (`src/models/audit_log.py`) e o helper `registrar_auditoria()` (`src/utils/audit_helper.py`).
- Integrar a gravação de auditoria imutável nos fluxos de alta médica, movimentação de leito e login/segurança.
- Criar a Central de Configurações `src/config.py` com validações no boot (Pydantic Settings) e criar a documentação `docs/SECRETS_E_CONFIGURACOES.md`.
- Atualizar todas as documentações de especificação (`02-requisitos.md`, `05-interfaces.md`, `data-model.md`, `ARCHITECTURE.md`, `CHANGELOG.md`).

**Non-Goals:**
- Alterações visuais complexas no frontend (nesta release o foco é a infraestrutura, segurança e auditoria no backend).
- Realizar deploy em produção nesta fase de proposta (o deploy em produção será feito posteriormente via script oficial).

## Decisions

### 1. Default-Private Router Pattern no FastAPI (`alta.py`)
- **Decisão**: Adicionar `dependencies=[Depends(get_current_user)]` na declaração do `APIRouter` em `src/routers/alta.py`.
- **Alternativas consideradas**: Proteger cada endpoint individualmente. *Rejeitado* porque abre margem para esquecimentos em novos endpoints.

### 2. Tabela Unificada de Auditoria Imutável (`audit_logs`)
- **Decisão**: Modelo `AuditLog` contendo `id`, `timestamp`, `categoria` (`SEGURANCA`, `NEGOCIO_CLINICO`, `CONFIGURACAO`), `acao`, `usuario_id`, `detalhes`, `estado_anterior` (JSON) e `estado_novo` (JSON).
- **Alternativas consideradas**: Logs apenas em arquivo de texto. *Rejeitado* pois impede consultas SQL estruturadas de auditoria.

### 3. Central de Configurações com Pydantic BaseSettings (`src/config.py`)
- **Decisão**: Criar classe `Settings` estendendo `BaseSettings` do `pydantic-settings`. No método `@model_validator` ou no boot da aplicação, validar se `ENVIRONMENT == "production"` e rejeitar `SECRET_KEY` padrão/fraca ou variáveis nulas.
- **Alternativas consideradas**: Uso simples de `os.getenv()`. *Rejeitado* pois não garante tipagem nem validação no boot do servidor.

## Risks / Trade-offs

- **[Risco] Falha de boot se `.env` de produção estiver sem variáveis obrigatórias** → *Mitigação*: Criar documentação clara em `docs/SECRETS_E_CONFIGURACOES.md` e atualizar `.env.example`.
- **[Risco] Overhead de IO na gravação de logs de auditoria** → *Mitigação*: A gravação de auditoria é realizada em transação otimizada no PostgreSQL via SQLAlchemy.

## Migration Plan

1. Executar as migrações do banco (ou criação das tabelas via SQLAlchemy `Base.metadata.create_all`).
2. Atualizar variáveis no arquivo `.env`.
3. Reiniciar a aplicação backend (`hc-uti.service`).
