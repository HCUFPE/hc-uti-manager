# Design: Renomeação do Sistema para "Reserva UTI"

## Context

A transição de nome de `HC-UTI Manager` para `Reserva UTI` é uma mudança estritamente visual, de apresentação e de documentação. Nenhuma camada de infraestrutura de servidor, banco de dados ou autenticação deve ser afetada.

## Goals / Non-Goals

**Goals:**
- Atualizar os textos de apresentação da interface (aba do navegador, tela de login, topo da barra lateral).
- Atualizar a constante central `APP_NAME` em `src/version.py` e refletir no `/api/health` e Swagger.
- Atualizar documentação do projeto (`README.md`, `docs/projeto_inicial/*`, `CHANGELOG.md`).

**Non-Goals:**
- **Zero alteração em infraestrutura:** Não alterar o serviço systemd (`hc-uti.service`), caminhos na VM (`/var/app/hc-uti-manager`), nem nomes de containers (`hc-uti-backend`, `hc-uti-nginx`).
- **Zero alteração em imagens neutras:** Manter `logo.png` (ícone da barra lateral) e os favicons/ícones da aba inalterados, pois são símbolos/brasões gráficos sem texto.
- **Zero alteração em regras de permissão ou usuários:** Não há nenhuma mudança em perfis, permissões ou banco de dados.

## Decisions

### 1. Mudança Restrita à Camada de Apresentação e Documentação
- **Decisão:** Todo o backend, banco SQLite, variáveis de ambiente e serviços Linux permanecem intocados. Apenas strings de texto de interface e metadados informativos de versão são atualizados.
- **Justificativa:** Garantia total de segurança, estabilidade e zero downtime.

### 2. Tratamento das Imagens
- **Decisão:** Manter os ícones e favicons intactos. No login, caso desejado, conectar a logo `Logo Reserva UTI.png` que já se encontra na pasta `frontend/public/` ou manter a atual.
