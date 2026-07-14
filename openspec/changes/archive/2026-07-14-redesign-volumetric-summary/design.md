## Context

A separação lógica entre o ciclo de vida da solicitação (estado atual) e ações operacionais (volume de trabalho) evita confusão matemática.

## Decisions

### 1. Backend: `src/providers/implementations/indicadores_provider.py`
Adicionar os seguintes cálculos sob `volume_solicitacoes`:
```python
sols_criadas_periodo = [s for s in solicitacoes_todas if in_period(s.criado_em)]
volume_solicitacoes = len(sols_criadas_periodo)

volume_concluidas = len([s for s in sols_criadas_periodo if s.status == "Concluída"])
volume_canceladas = len([s for s in sols_criadas_periodo if s.status == "Cancelada"])
volume_reservas_ativas = len([s for s in sols_criadas_periodo if s.status == "Reservado"])
volume_pendentes_fila = len([s for s in sols_criadas_periodo if s.status == "Pendente"])
```

Retornar no dicionário `"volumes"`:
```python
"volumes": {
    "solicitacoes": volume_solicitacoes,
    "concluidas": volume_concluidas,
    "canceladas": volume_canceladas,
    "reservas_ativas": volume_reservas_ativas,
    "pendentes_fila": volume_pendentes_fila,
    "percentual_concluidas": round(volume_concluidas / volume_solicitacoes * 100, 1) if volume_solicitacoes > 0 else 0.0,
    "percentual_canceladas": round(volume_canceladas / volume_solicitacoes * 100, 1) if volume_solicitacoes > 0 else 0.0,
    "percentual_reservas_ativas": round(volume_reservas_ativas / volume_solicitacoes * 100, 1) if volume_solicitacoes > 0 else 0.0,
    "percentual_pendentes_fila": round(volume_pendentes_fila / volume_solicitacoes * 100, 1) if volume_solicitacoes > 0 else 0.0,
    
    # Ações Operacionais históricas
    "reservas_efetuadas": volume_reservas,
    "cancelamento_reservas": volume_cancelamentos_res,
    "altas": volume_altas,
    "altas_concluidas": volume_altas_concluidas,
}
```

### 2. Frontend: `frontend/src/views/Indicadores.vue`
Substituir a tabela única por duas tabelas consecutivas dentro do mesmo grid/área.
- **Tabela 1: Resumo Volumétrico das Solicitações (Ciclo de Vida)**
- **Tabela 2: Resumo de Ações da UTI e Altas (Volume de Trabalho)**
