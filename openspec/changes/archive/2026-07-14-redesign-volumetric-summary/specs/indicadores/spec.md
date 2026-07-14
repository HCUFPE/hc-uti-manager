## ADDED Requirements

### Requirement: Detalhamento do Ciclo de Vida da Solicitação
O endpoint de indicadores operacionais MUST retornar um detalhamento completo dos estados das solicitações criadas no período, de forma a fechar o balanço exato:
$$\text{Criadas} = \text{Concluídas} + \text{Canceladas} + \text{Reservas Ativas} + \text{Pendentes na Fila}$$

### Requirement: Separação Visual de Resumos de Volumes
A tela de Indicadores Operacionais MUST renderizar dois quadros separados no layout:
1. Ciclo de Vida das Solicitações (Concluídas, Canceladas, Reservas Ativas, Pendentes na Fila)
2. Resumo de Ações da UTI e Altas (Reservas Efetuadas, Reservas Canceladas, Altas Solicitadas, Altas Concluídas)
