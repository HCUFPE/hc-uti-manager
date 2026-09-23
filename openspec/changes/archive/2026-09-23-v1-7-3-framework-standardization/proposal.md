# Proposal: v1.7.3 - Padronização com Framework SETISD (Proteção de Rotas, Auditoria e Central de Segredos)

## Why

Para elevar o nível de segurança, conformidade e maturidade da aplicação `HC UTI Manager` seguindo os padrões arquiteturais do **Framework SETISD**, a versão **v1.7.3** introduz:
1. **Default-Private Router Pattern**: Garantir proteção rigorosa contra acessos não autenticados no backend FastAPI (corrigindo a vulnerabilidade/falta de dependência no router `alta.py`).
2. **Tabela Unificada de Auditoria e Logs**: Histórico imutável de alterações (gravando estado anterior e novo em JSON) categorizado em `SEGURANCA`, `NEGOCIO_CLINICO` ou `CONFIGURACAO`.
3. **Central de Configurações e Validação de Segredos**: Validação rigorosa no boot do servidor (`src/config.py` e documentação `docs/SECRETS_E_CONFIGURACOES.md`) que impede a inicialização do sistema se existirem variáveis faltando no `.env` ou se segredos fracos forem utilizados em produção.

## What Changes

- **Proteção de Rotas (Default-Private Router Pattern)**:
  - Atualização do router `src/routers/alta.py` para injetar a dependência de autenticação JWT em nível de router (`dependencies=[Depends(get_current_user)]`), alinhando-o aos demais routers da aplicação.
- **Sistema de Auditoria Unificada (`audit_log.py` e `audit_helper.py`)**:
  - Nova tabela/entidade `audit_logs` no SQLite local e PostgreSQL via SQLAlchemy.
  - Função auxiliar `registrar_auditoria()` que grava logs estruturados imutáveis com `categoria` (`SEGURANCA`, `NEGOCIO_CLINICO`, `CONFIGURACAO`), `acao`, `usuario_id`, `detalhes` e payloads JSON `estado_anterior` e `estado_novo`.
  - Integração automática no `HistoricoProvider.registrar()` para que **todas as ações operacionais da UTI, Bloco Cirúrgico e NIR** (solicitação de alta, reservas, cancelamentos, swaps, bloqueio clínico e passagens de caso) gravem cópias imutáveis em `audit_logs` sob a categoria `NEGOCIO_CLINICO`.
  - Inclusão de auditoria de `SEGURANCA` para login, atribuição (`ATRIBUIR_PERFIL_USUARIO`) e exclusão (`EXCLUIR_PERFIL_USUARIO`) de perfis em `AdminConfig.vue`.
- **Central de Configurações e Validação de Segredos**:
  - Módulo centralizado `src/config.py` utilizando Pydantic / pydantic-settings para carregamento e validação estrita de variáveis de ambiente.
  - Validação de boot: se `ENVIRONMENT=production`, bloqueia a subida da aplicação se `SECRET_KEY` for fraca/default ou se variáveis obrigatórias estiverem ausentes.
  - Documentação detalhada em `docs/SECRETS_E_CONFIGURACOES.md`.
- **Atualização de Documentação de Especificação (Spec-Driven Development)**:
  - Atualização dos arquivos `02-requisitos.md`, `05-interfaces.md`, `data-model.md`, `ARCHITECTURE.md` e `CHANGELOG.md` conforme regras em `.agents/AGENTS.md`.

## Capabilities

### New Capabilities
- `audit-logging`: Sistema de auditoria unificada e imutável para ações de segurança, negócio clínico e configurações.
- `secret-config-validation`: Central de configurações e validação estrita de segredos e variáveis no boot da aplicação.

### Modified Capabilities
- `route-protection`: Aplicação do padrão Default-Private Router na rota `alta.py` garantindo que todos os endpoints de alta exijam autenticação.

## Impact

- **Backend (`src/routers/alta.py`, `src/config.py`, `src/models/audit_log.py`, `src/utils/audit_helper.py`)**: Alterações e inclusão de novos módulos.
- **Banco de Dados (PostgreSQL)**: Criação da tabela `audit_logs`.
- **Configuração (`.env`, `.env.example`, `docs/SECRETS_E_CONFIGURACOES.md`)**: Definição clara e estrita de variáveis de ambiente.
- **Documentação do Projeto (`docs/projeto_inicial/02-requisitos.md`, `docs/projeto_inicial/05-interfaces.md`, `docs/data-model.md`, `docs/ARCHITECTURE.md`, `CHANGELOG.md`)**: Atualização completa e detalhada para a v1.7.3.
