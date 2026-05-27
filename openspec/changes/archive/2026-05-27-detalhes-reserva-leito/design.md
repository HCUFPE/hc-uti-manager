## Context

Atualmente, a visão de leitos (`Home.vue` e `BedCard.vue`) recebe dados do backend que descrevem o próximo paciente (reserva ativa). Entretanto, essa informação está limitada ao prontuário, idade, especialidade, data da cirurgia e turno. O nome do paciente e a hora da cirurgia não são expostos pelo controller de leitos, embora estejam salvos na tabela `solicitacoes_leito` (que origina a reserva).

## Goals / Non-Goals

**Goals:**
- Estender o retorno da listagem de leitos no backend para incluir `nome_proximo` e `hora_cirurgia_proximo`.
- Exibir o nome do próximo paciente nos cards de leito com reserva em fonte pequena (ex: `text-xs`).
- Concatenar a data da cirurgia e a hora da cirurgia no formato `DD/MM/AAAA - HH:MM` no card de leito.

**Non-Goals:**
- Não iremos alterar a estrutura do banco de dados (SQLite/Prisma). As informações necessárias já estão presentes na tabela `solicitacoes_leito`.
- Não alteraremos a listagem de pacientes atuais de leitos ocupados, visto que essas informações vêm diretamente do AGHU de forma demográfica em tempo real.

## Decisions

### Decision 1: Lookup no Controller de Leitos (Backend)
- **Opção A:** Modificar o model `LeitoEstado` para duplicar o nome e a hora da cirurgia.
- **Opção B:** No método `listar_leitos` do `LeitosController`, quando houver uma solicitação de leito associada à reserva (`sol_id`), carregar as informações diretamente do objeto `SolicitacaoLeito` retornado pelo `solicitacao_provider`.
- **Escolha:** Opção B. Evita duplicação de dados nas tabelas locais e mantém a consistência relacional. A consulta por `sol_id` já é executada para extrair data e turno da cirurgia, logo incluir o nome e a hora tem custo desprezível.

### Decision 2: Formatação de Data e Hora no Frontend
- **Opção A:** Criar um helper inline no template.
- **Opção B:** Definir um método utilitário `formatarDataHoraCirurgia(data, hora)` dentro do script setup do componente `BedCard.vue`.
- **Escolha:** Opção B. Oferece melhor legibilidade do código de visualização e encapsula a lógica de formatação de forma robusta.

## Risks / Trade-offs

- **[Risco] Mocks no ambiente de desenvolvimento sem nome de paciente ou horário** → Mocks locais podem não apresentar o nome e hora, quebrando a interface ou exibindo dados incompletos.
  - **Mitigação:** Tratar fallbacks adequadamente: se `nome` não existir, omitir o campo ou usar `'Paciente AGHU'`, e se `hora_cirurgia` não existir, exibir apenas a data formatada.
