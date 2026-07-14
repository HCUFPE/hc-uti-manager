## Why

Atualmente, o resumo volumétrico mistura contagens de ações (ex: cliques operacionais em reservar/cancelar) com contagens de solicitações de pacientes. Isso faz com que as somas pareçam não fechar, gerando confusão no usuário. 

A proposta é dividir o resumo em dois quadros bem definidos:
1. **Ciclo de Vida das Solicitações:** Onde cada uma das solicitações criadas no período se encontra atualmente (uma divisão estrita de estados: Concluídas, Canceladas, Reservadas Ativas, Pendentes na Fila). A soma dessas partes dará exatamente o total de solicitações criadas.
2. **Resumo de Ações da UTI e Altas:** Contagem histórica das ações operacionais tomadas (Cliques em Reservar, Cliques em Cancelar Reserva, Solicitações de Alta e Altas Concluídas).

## What Changes

- **Backend (`indicadores_provider.py`):**
  - Ajustar o retorno de `/api/indicadores/resumo` para incluir no dicionário `detalhado.volumes` as novas chaves correspondentes aos estados das solicitações criadas no período:
    - `concluidas` (solicitações criadas no período com status "Concluída")
    - `canceladas` (solicitações criadas no período com status "Cancelada")
    - `reservadas_ativas` (solicitações criadas no período com status "Reservado")
    - `pendentes_fila` (solicitações criadas no período com status "Pendente")
  - Manter as contagens de ações históricas para a segunda tabela.

- **Frontend (`Indicadores.vue`):**
  - Redesenhar a tabela de "Resumo Volumétrico do Período" dividindo-a em dois quadros separados:
    1. **Ciclo de Vida das Solicitações**
    2. **Ações Operacionais da UTI/Regulação**

## Capabilities

### Modified Capabilities
- `indicadores`: Redesenho do resumo volumétrico.
