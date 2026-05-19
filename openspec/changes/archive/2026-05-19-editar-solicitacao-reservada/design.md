## Context

O fluxo atual de solicitações de leito impede a edição de uma solicitação após a reserva de um leito, o que protege o status e os dados já avaliados. No entanto, solicitantes com papéis de gestão e controle (BC, BC-ADMIN, COB, COB-ADMIN, HEM e HEM-ADMIN) necessitam editar esses dados caso haja alguma atualização clínica ou de cadastro, mesmo com o leito reservado. Isso exige uma mudança no bloqueio de interface (frontend) e nas regras de negócio da API (backend).

## Goals / Non-Goals

**Goals:**
- Habilitar o botão e a ação de "Editar" no frontend (como em `Solicitacoes.vue`) em solicitações de status "reservado", somente se o usuário ativo pertencer aos grupos AD/Role correspondentes (`BC`, `BC-ADMIN`, `COB`, `COB-ADMIN`, `HEM` ou `HEM-ADMIN`).
- Adaptar o endpoint de atualização (`PUT/PATCH` para solicitações) no backend para verificar as *roles* do solicitante antes de rejeitar atualizações de solicitações reservadas, permitindo a operação para os referidos grupos.
- Garantir que o histórico de ações registre essa alteração devidamente.

**Non-Goals:**
- Mudar o status do leito ao editar a solicitação.
- Permitir edição de solicitações reservadas para médicos assistentes comuns (não inclusos nestes grupos).
- Reformular todo o sistema de controle de acesso baseado em role (apenas estender a regra já existente de edição).

## Decisions

**Validação de Grupos (Frontend)**
- Iremos injetar a verificação dos grupos do usuário logado diretamente nas regras que determinam o estado `disabled` ou a renderização do botão "Editar" de uma solicitação.
- A checagem será algo como: `isReserved && userHasSpecialRole(user.groups)` para liberar a interface.

**Validação de Grupos (Backend)**
- No arquivo responsável pela atualização da solicitação (provavelmente em `src/controllers/solicitacao_controller.py` ou roteador correspondente), ao recuperar a solicitação atual para update, checaremos se ela está reservada.
- Se estiver reservada, validaremos `current_user.groups` contra a lista permitida: `['BC', 'BC-ADMIN', 'COB', 'COB-ADMIN', 'HEM', 'HEM-ADMIN']`. Se nenhuma role bater, levantaremos um erro `HTTPException(403, "Não autorizado a editar solicitações reservadas")`.
- A checagem será case-insensitive para evitar bugs com o mapeamento AD.

## Risks / Trade-offs

- **[Risk]** Possibilidade de conflito de dados se o leito estiver sendo atualizado (movimentação de paciente) simultaneamente com a edição da solicitação.
  - *Mitigação*: A edição é limitada aos dados da solicitação em si. O sistema mantém trilha de auditoria/histórico para registrar quem fez a edição.
- **[Risk]** Divergência entre os nomes das roles na especificação e como estão no Active Directory ou banco de dados local.
  - *Mitigação*: As roles devem ser tratadas de forma flexível ou ser configuradas com nomes idênticos aos mapeados no payload JWT / Mock do usuário.
