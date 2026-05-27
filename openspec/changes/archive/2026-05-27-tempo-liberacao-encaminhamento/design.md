## Context

Atualmente, o processo de transferência pós-cirúrgica envolve a sinalização do fim da cirurgia pelo setor demandante (cirurgia finalizada) e a autorização de transferência pela UTI (encaminhamento liberado). O intervalo entre esses dois eventos não é medido ou contabilizado para fins analíticos (indicadores), nem monitorado visualmente na tela principal de leitos.

## Goals / Non-Goals

**Goals:**
- Adicionar colunas `cirurgia_finalizada_em` e `encaminhamento_liberado_em` no modelo `SolicitacaoLeito` para controle de fluxo temporal.
- Garantir a migração leve do banco SQLite local em tempo de execução adicionando as colunas caso não existam.
- Calcular e logar o tempo decorrido no histórico de auditoria ao liberar o encaminhamento.
- Exibir um temporizador em execução no card de leito da UTI para leitos no status "Cirurgia Concluída".
- Exibir a média desse tempo no painel de indicadores operacionais.

**Non-Goals:**
- Não utilizaremos bancos de dados externos além de SQLite local e censo AGHU.
- O cálculo do indicador considerará apenas o período selecionado de filtros na tela de Indicadores.

## Decisions

### Decision 1: Atualização Automática do Esquema de SQLite (Migration)
- **Opção A:** Escrever uma migração via Alembic.
- **Opção B:** Executar comandos SQL `ALTER TABLE` protegidos por `TRY/EXCEPT` no lifecycle de inicialização do backend (`main.py`).
- **Escolha:** Opção B. Como as implantações locais e de desenvolvimento utilizam SQLite em múltiplos ambientes, a Opção B garante que as colunas sejam adicionadas automaticamente no startup sem requerer comandos manuais de migração pelo usuário, mantendo a compatibilidade transparente.

### Decision 2: Cálculo do Tempo de Espera em Tempo Real no Card
- **Opção A:** Exibir o tempo calculado estático vindo do backend.
- **Opção B:** Utilizar um timer reativo no frontend (`setInterval` a cada 1 minuto em `BedCard.vue`) para recalcular o tempo decorrido desde o timestamp `cirurgia_finalizada_em` em relação a uma referência `currentTime`.
- **Escolha:** Opção B. Proporciona uma experiência muito mais premium e interativa, com o contador avançando visualmente em tempo real enquanto o profissional monitora a UTI.

## Risks / Trade-offs

- **[Risco] Fuso Horário Diferente entre Servidor e Navegador** → Os timestamps no SQLite são salvos em UTC, enquanto o navegador utiliza a hora local do usuário.
  - **Mitigação:** No backend, ao expor `cirurgia_finalizada_em` na API de leitos, subtrair 3 horas para convertê-lo para o fuso de Brasília (UTC-3), e no frontend fazer o parse desse ISO string na data local do navegador.
