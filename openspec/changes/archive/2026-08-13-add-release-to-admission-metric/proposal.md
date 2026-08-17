## Why

Atualmente, o painel de indicadores apresenta métricas para medir o tempo do fim da cirurgia até a liberação do encaminhamento e do fim da cirurgia até a admissão física no leito de UTI. No entanto, não há um indicador direto que mensure o tempo decorrido especificamente durante a etapa de transporte/transferência do paciente (do momento em que o encaminhamento é liberado até o paciente ser admitido de fato no leito). 

A adição desta métrica ("Tempo de Encaminhamento até Admissão") preenche esta lacuna, permitindo que a coordenação hospitalar identifique gargalos logísticos específicos na fase de transporte e recepção do paciente na UTI.

## What Changes

- **Backend (API de Indicadores):**
  - No `IndicadoresProvider` (arquivo `src/providers/implementations/indicadores_provider.py`), adicionar o cálculo de um novo indicador: `tempo_medio_encaminhamento_admissao_minutos`.
  - Este cálculo medirá a diferença de tempo (em minutos) entre a liberação do encaminhamento (data/hora gravada em `encaminhamento_liberado_em` da solicitação ou evento correspondente no histórico) e a admissão definitiva do paciente no leito (evento `conclusao` ou conclusão da solicitação correspondente).
  - Expor a nova métrica no payload JSON retornado pelo endpoint `/api/indicadores/resumo`.
- **Frontend (Painel de Indicadores):**
  - No dashboard de Indicadores (`frontend/src/views/Indicadores.vue`), adicionar um card/gráfico para exibir este novo tempo médio ("Encaminhamento até Admissão") posicionado estrategicamente ao lado dos indicadores existentes de fluxo cirúrgico.

## Capabilities

### New Capabilities

*(Nenhuma nova capacidade necessária, pois trata-se de uma extensão do cálculo de indicadores).*

### Modified Capabilities

- `indicadores-calculos`: Adicionado o cálculo do tempo médio de encaminhamento até admissão (tempo de transporte/transferência física pós-liberação do bloco).

## Impact

- **Backend:** Atualização da API de resumo de indicadores.
- **Frontend:** Atualização na tela de Indicadores para renderizar o novo card lado a lado com os tempos do Bloco Cirúrgico.
- **Banco de Dados (SQLite):** Nenhuma alteração de esquema é necessária, pois utilizaremos os campos já existentes de histórico de ações e campos da tabela `solicitacoes_leito`.
