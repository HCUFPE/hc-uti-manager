# Proposal: Permitir Seleção do Motivo "Falta de vaga de UTI" por Setores Solicitantes

## Why

Atualmente, o motivo de cancelamento de solicitação "Falta de vaga de UTI" é exibido e permitido exclusivamente para usuários com perfil da UTI (e Administradores). Na rotina hospitalar, contudo, os setores solicitantes (Bloco Cirúrgico - BC, Centro Obstétrico - COB e Hemodinâmica - HEM) frequentemente suspendem cirurgias ou cancelam suas solicitações ao serem previamente informados da ausência de leitos na UTI. Sem essa opção no menu de seleção, os solicitantes eram forçados a selecionar justificativas genéricas (como "Cirurgia suspensa por outros motivos") ou depender da própria UTI para cancelar o registro, o que gerava atrito operacional e comprometia a fidelidade dos indicadores de cancelamento. Esta mudança inclui a opção diretamente para os solicitantes na versão em construção 1.8.0.

## What Changes

- **Inclusão do Motivo para Solicitantes**: Disponibilizar o motivo "Falta de vaga de UTI" no dropdown de cancelamento de solicitações para os perfis solicitantes (`BC`, `COB`, `HEM` e seus subperfis `-Admin`).
- **Ajuste de Seleção no Frontend**: Atualizar a constante `MOTIVOS_CANCELAMENTO` e a computed property `motivosAtuais` em `Solicitacoes.vue` para contemplar essa opção universalmente para cancelamentos de solicitações pendentes/reservadas.
- **Transparência de Indicadores e Histórico**: Garantir que o cancelamento registrado com este motivo seja atribuído ao usuário solicitante no log de histórico e refletido nas métricas do BI/Indicadores de forma agregada.
- **Documentação e Changelog**: Atualizar o `CHANGELOG.md` na versão em construção `1.8.0`, bem como os cadernos de requisitos e casos de uso do projeto.

## Capabilities

### New Capabilities
*(Nenhuma nova capacidade introduzida)*

### Modified Capabilities
- `solicitacao-leitos`: Atualizar a regra de negócio do requisito "Controle de Permissões na Edição", permitindo que setores solicitantes criadores (`BC`, `COB`, `HEM`) também selecionem o motivo "Falta de vaga de UTI" ao cancelar suas solicitações.

## Impact

- **Frontend**: `frontend/src/views/Solicitacoes.vue` (atualização da lista de motivos de cancelamento e computed property).
- **Backend / APIs**: `src/routers/solicitacoes_leito.py` (garantir que a autorização por perfil de origem aceite "Falta de vaga de UTI" sem restrições colaterais).
- **Documentação e Governança**: `CHANGELOG.md`, `docs/projeto_inicial/02-requisitos.md` e `docs/projeto_inicial/03-casos-uso.md`.
