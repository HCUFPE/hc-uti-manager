## Context

No ambiente de desenvolvimento local (`MOCK_BEDS=true`), os dados de cirurgia mockados retornam sempre com a data do dia atual ("hoje"). Para testar o cálculo de indicadores de fila futuros e ordenação por data de cirurgia, é necessário que alguns prontuários mockados representem cirurgias futuras (amanhã e depois). No frontend, a hora da cirurgia está disponível no objeto de solicitação (`hora_cirurgia`), mas não é exibida visualmente na listagem de solicitações.

## Goals / Non-Goals

**Goals:**
- Adicionar os prontuários `6` (cirurgia para amanhã) e `7` (cirurgia para depois de amanhã) ao mock de desenvolvimento.
- Exibir a hora de início da cirurgia nos cards de solicitação de leito (seção de pendentes e seção de reservados).

**Non-Goals:**
- Alterar as consultas SQL de produção que acessam o banco do AGHU.
- Adicionar ou alterar as rotas da API.

## Decisions

### 1. Ajuste dos Mocks no Backend
- **Abordagem**: Em `SolicitacaoLeitoController.consultar_dados_aghu`, adicionaremos entradas específicas no dicionário `mocks` para as chaves `"6"` e `"7"`. As datas das cirurgias serão calculadas dinamicamente:
  - Prontuário `6`: `(datetime.today() + timedelta(days=1)).strftime("%d-%m-%Y")`
  - Prontuário `7`: `(datetime.today() + timedelta(days=2)).strftime("%d-%m-%Y")`
- **Raciocínio**: Essa técnica garante que as cirurgias mockadas sempre fiquem em datas relativas dinâmicas ao dia em que o teste está sendo executado, evitando que mocks de data fiquem defasados ou no passado.

### 2. Exibição da Hora da Cirurgia no Frontend
- **Abordagem**:
  - No grid de detalhes do card de solicitações **Aguardando Reserva** (`Solicitacoes.vue`), incluiremos um novo bloco de detalhe entre a "Data Prevista da Cirurgia" e o "Turno":
    ```html
    <div class="space-y-0.5">
      <p class="text-[10px] font-medium uppercase tracking-wider text-slate-400">Horário</p>
      <p class="text-sm font-semibold text-slate-700">{{ sol.hora_cirurgia || '--:--' }}</p>
    </div>
    ```
  - No grid de detalhes das solicitações **Reservadas** (`Solicitacoes.vue`), incluiremos a hora de início junto à data ou em um bloco próprio:
    ```html
    <div class="space-y-1">
      <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Horário</p>
      <p class="text-base font-bold text-slate-700">{{ sol.hora_cirurgia || '--:--' }}</p>
    </div>
    ```
- **Raciocínio**: Isso fornece informações exatas aos coordenadores para que possam priorizar pacientes com base no horário exato da cirurgia, e não apenas no turno.

## Risks / Trade-offs

- **[Risco]** A ordenação da fila de prioridade pode ser afetada localmente por datas futuras.
  - **[Mitigação]** A ordenação do backend já prioriza a data da cirurgia de forma crescente. Portanto, os prontuários 6 (amanhã) e 7 (depois) ficarão no final da fila de prioridades, o que é o comportamento esperado.
