## 1. Proteção de Rotas (Default-Private Router Pattern)

- [x] 1.1 Injetar `dependencies=[Depends(get_current_user)]` na declaração do router `src/routers/alta.py` garantindo autenticação padrão em todas as rotas de alta.

## 2. Tabela Unificada de Auditoria e Logs

- [x] 2.1 Criar o modelo SQLAlchemy `AuditLog` em `src/models/audit_log.py` com suporte aos campos imutáveis, categorias (`SEGURANCA`, `NEGOCIO_CLINICO`, `CONFIGURACAO`) e JSON (`estado_anterior` e `estado_novo`).
- [x] 2.2 Criar o helper `registrar_auditoria()` em `src/utils/audit_helper.py` para gravação simplificada de logs de auditoria.
- [x] 2.3 Importar e integrar o registro de auditoria nos fluxos de negócio em `src/routers/alta.py`, `src/controllers/leitos_controller.py` e `src/routers/auth.py`.

## 3. Central de Configurações e Validação de Segredos

- [x] 3.1 Implementar a Central de Configurações `src/config.py` com Pydantic / pydantic-settings para ler e validar variáveis de ambiente.
- [x] 3.2 Adicionar validação no boot para rejeitar inicialização em ambiente de produção com segredos fracos ou ausentes.
- [x] 3.3 Criar o documento `docs/SECRETS_E_CONFIGURACOES.md` detalhando todas as variáveis de ambiente do sistema e atualizar o `.env.example`.

## 4. Atualização da Especificação (Spec-Driven Development)

- [x] 4.1 Atualizar `docs/projeto_inicial/02-requisitos.md` com os novos requisitos funcionais e não-funcionais (RF de auditoria e RNF de segredos/proteção de rotas).
- [x] 4.2 Atualizar `docs/projeto_inicial/05-interfaces.md` e `docs/data-model.md` especificando a tabela `audit_logs`.
- [x] 4.3 Atualizar `docs/ARCHITECTURE.md` registrando o padrão Default-Private Router e o subsistema de Auditoria/Configurações.
- [x] 4.4 Atualizar o `CHANGELOG.md` documentando a versão v1.7.3.
