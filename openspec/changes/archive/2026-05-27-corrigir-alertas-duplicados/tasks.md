## 1. Database Cleanup

- [x] 1.1 Delete duplicate and test alerts from the local SQLite database (`data/app.db`)

## 2. Code Modifications

- [x] 2.1 Implement `get_todas_completo()` in `SolicitacaoLeitoProvider` to include cancelled solicitations
- [x] 2.2 Update `AlertaController._analisar_historico` to use `get_todas_completo()`
- [x] 2.3 Correct date validation in `AlertaController._validar_data_hoje` to normalize date formats (`DD-MM-YYYY` vs `YYYY-MM-DD`)
- [x] 2.4 Refine alert deduplication in `AlertaController._sincronizar_alertas` by normalizing and comparing datetime objects

## 3. Verification

- [x] 3.1 Run tests to verify alerts are not duplicated and only triggered for today's surgeries
