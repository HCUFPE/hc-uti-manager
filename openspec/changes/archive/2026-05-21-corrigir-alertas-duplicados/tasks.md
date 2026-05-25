## 1. Backend Implementation

- [ ] 1.1 In `src/controllers/alerta_controller.py`, update `_analisar_altas` to populate `"criado_em"` with `alta.criado_em` for "Solicitação de Alta" and `alta.atualizado_em` for "Acomodação Definida".
- [ ] 1.2 In `src/controllers/alerta_controller.py`, update the `_sincronizar_alertas` logic to perform robust datetime comparison using a tolerance window (e.g. difference < 2 seconds) when checking for `existente`.
- [ ] 1.3 Verify that the cleanup code in `_sincronizar_alertas` remains unchanged, only deleting `["Infeccioso", "Permanencia", "Limpeza"]` alerts, thereby preserving "Gargalo" alerts history.

## 2. Verification and Testing

- [ ] 2.1 Write and run a python verification script in `scratch` that triggers `gerar_alertas` multiple times to verify no duplicate alerts are created.
- [ ] 2.2 Verify that already resolved or older alerts are not deleted by the sync cleanup routine, preserving history.
