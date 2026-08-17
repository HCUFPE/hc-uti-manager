## Why

Atualmente, o sistema de internação da UTI é centrado nas solicitações ativas vindas do Bloco Cirúrgico (BC). No entanto, setores como a Obstetrícia (COB) e a Hemodinâmica (HEM) ainda não estão integrados para criar solicitações eletrônicas diretamente no painel. Isso gera a necessidade de que a equipe da UTI reserve leitos de forma manual/preventiva para garantir vagas para esses setores antes de a cirurgia terminar ou da internação física ocorrer.

Esta nova funcionalidade ("Reserva Prévia de Leito Clínico/COB/HEM") resolverá este problema de forma simplificada, permitindo o bloqueio de leitos de maneira genérica sem exigir dados cadastrais imediatos do paciente. Ela também apoia o remanejamento inteligente dessas reservas, liberando automaticamente a vaga quando o paciente é remanejado ou admitido pelo censo.

Este conjunto de alterações representa a evolução do sistema para a versão **1.5.0**.

## What Changes

- **Backend (Novas APIs e Regras de Negócio):**
  - Adição da flag `bloqueado_clinico` (boolean) na modelagem local de estados dos leitos (`LeitoEstado`).
  - Criação de endpoints HTTP para ativar (`/api/leitos/{lto_id}/bloquear-clinico`) e desativar (`/api/leitos/{lto_id}/desbloquear-clinico`) esse bloqueio genérico.
  - Ajuste na listagem de leitos disponíveis para solicitações do Bloco (BC): leitos bloqueados para Clínico/COB/HEM não serão retornados como opções livres.
  - Implementação do swap/troca de bloqueio no remanejamento: ao mover uma reserva ativa do Leito X para um Leito Y bloqueado para clínica, o Leito Y recebe o paciente e o Leito X herda o bloqueio genérico automaticamente.
- **Frontend (Painel e Solicitações):**
  - Exibição visual destacada dos leitos bloqueados genéricos com a etiqueta "Reservado p/ Clínico/COB/HEM".
  - Adição de botões para bloquear e desbloquear diretamente do card do leito vago (para UTI/Admin).
- **Versão do Sistema:**
  - Bump global da versão para `1.5.0`.

## Capabilities

### New Capabilities

*(Nenhuma nova capacidade no nível macro, apenas extensão das capacidades de internação e solicitação de leitos).*

### Modified Capabilities

- `internacao-leitos`: Adicionado o estado de leito bloqueado para Clínico/COB/HEM e rotina de auto-limpeza de bloqueio na admissão física.
- `solicitacao-leitos`: Ajustada a listagem de leitos elegíveis para o Bloco Cirúrgico e a lógica de swap de bloqueio na rota de remanejamento.

## Impact

- **Banco de Dados (SQLite):** Nova migração do Alembic para adicionar a coluna `bloqueado_clinico` na tabela `leito_estados`.
- **Backend APIs:** Novos endpoints e modificação das controllers de leito e solicitações.
- **Frontend:** Estilização de novos cards, modais de confirmação de bloqueio/liberação e alteração nas listas de leitos elegíveis para mudança de destino.
- **Versionamento:** Bump de versão para `1.5.0` no backend (`src/main.py`) e no frontend (`frontend/src/config/version.ts`).
