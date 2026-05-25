## Context

Atualmente, pacientes com leito de UTI reservado via solicitações cirúrgicas eletivas (dos setores BC, COB, HEM) não têm um fluxo estruturado no sistema para comunicar o término do procedimento cirúrgico (prontidão para transporte) e a autorização de recebimento pela UTI.

## Goals / Non-Goals

**Goals:**
- Adicionar campos `cirurgia_finalizada` e `encaminhamento_liberado` na tabela de solicitações de leito.
- Criar endpoints de atualização desses campos com validações de papel/perfil do usuário.
- Habilitar botão "Cirurgia Finalizada" em `Solicitacoes.vue` para setores solicitantes.
- Atualizar a coloração visual dos cards de leitos reservados no painel da UTI (`Home.vue` / `BedCard.vue`) para amarelo (Cirurgia Finalizada) e verde (Encaminhamento Liberado).
- Exibir botão "Liberar Encaminhamento" para a UTI nos leitos em estado amarelo.
- Disparar alertas recíprocos e automáticos entre a UTI e os solicitantes.

**Non-Goals:**
- Modificar o fluxo de cancelamento de reservas ou altas já existentes.

## Decisions

- **Modelo de Dados (Extensão SQLite)**:
  - Adicionar as colunas `cirurgia_finalizada` (boolean) e `encaminhamento_liberado` (boolean) à tabela `solicitacoes_leito` no modelo `SolicitacaoLeito`.
  - Atualizar o método `to_dict()` para serializar estes campos no JSON de resposta.
- **Endpoints de Ação no Backend**:
  - `POST /api/solicitacoes/{sol_id}/cirurgia-finalizada`:
    - Permissão: `[ADMIN, BC, BC_ADMIN, COB, COB_ADMIN, HEM, HEM_ADMIN]`.
    - Lógica: Define `cirurgia_finalizada = True`, registra log no histórico (`tipo="cirurgia_finalizada"`, `acao="Cirurgia Finalizada"`, `detalhes=f"Solicitação #{sol_id}: Paciente prontuário {prontuario} com cirurgia finalizada"`).
  - `POST /api/solicitacoes/{sol_id}/liberar-encaminhamento`:
    - Permissão: `[ADMIN, UTI, UTI_ADMIN]`.
    - Lógica: Define `encaminhamento_liberado = True`, registra log no histórico (`tipo="encaminhamento_liberado"`, `acao="Encaminhamento Liberado"`, `detalhes=f"Solicitação #{sol_id}: Encaminhamento autorizado"`).
  - `POST /api/solicitacoes/{sol_id}/cancelar-liberacao`:
    - Permissão: `[ADMIN, UTI, UTI_ADMIN]`.
    - Lógica: Define `encaminhamento_liberado = False`, registra log no histórico (`tipo="encaminhamento_cancelado"`, `acao="Liberação Cancelada"`, `detalhes=f"Solicitação #{sol_id}: Liberação de encaminhamento cancelada"`).
- **Repasse de Propriedades na Listagem de Leitos**:
  - Em `leitos_controller.py` -> `listar_leitos()`, ao recuperar os dados da solicitação vinculada à reserva via `solicitacao_id`, incluir no dicionário do leito:
    - `"cirurgia_finalizada"`: `sol.cirurgia_finalizada`
    - `"encaminhamento_liberado"`: `sol.encaminhamento_liberado`
    - `"solicitacao_id"`: `sol.id`
- **Adaptação dos Alertas**:
  - Em `alerta_controller.py` -> `_gerar_alerta_por_tipo`:
    - Tratar `tipo == "cirurgia_finalizada"`: Criar alerta `"Cirurgia Finalizada"`, tipo `"aviso"`, `perfil_alvo = None` (UTI).
    - Tratar `tipo == "encaminhamento_liberado"`: Identificar o solicitante original `perfil_vaga` e criar alerta `"Encaminhamento Autorizado"`, tipo `"info"`, `perfil_alvo = perfil_vaga`.
    - Tratar `tipo == "encaminhamento_cancelado"`: Identificar o solicitante original `perfil_vaga` e criar alerta `"Liberação Cancelada"`, tipo `"critico"`, `perfil_alvo = perfil_vaga`.
- **Modificações Visuais e Botões no Frontend**:
  - Em `Solicitacoes.vue`: Exibir o botão "Cirurgia Finalizada" quando a solicitação estiver com status "Reservado" e `cirurgia_finalizada == false`. Exibir badges informativas sobre o status do encaminhamento.
  - Em `BedCard.vue`:
    - Adaptar classe dinâmica `:class` para colorir a borda/fundo em amarelo quando `cirurgia_finalizada && !encaminhamento_liberado`, e em verde quando `encaminhamento_liberado`.
    - Exibir o botão "Liberar Encaminhamento" para perfis UTI/Admin se `cirurgia_finalizada && !encaminhamento_liberado`.
    - Exibir o botão "Cancelar Liberação" para perfis UTI/Admin se `encaminhamento_liberado == true`.
  - Em `Home.vue`: Mapear o evento `@liberar-encaminhamento` e realizar chamada ao endpoint correspondente.

## Risks / Trade-offs

- **Carga de Queries na Listagem de Leitos**:
  - *Risco*: A listagem de leitos passa a ler as solicitações associadas para preencher os dados de encaminhamento.
  - *Mitigação*: O banco SQLite local possui índices adequados e a lista de leitos ativos é pequena (escala de dezenas), minimizando qualquer impacto de performance.
