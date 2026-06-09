## 1. Ajustar Lógica de Indicadores

- [x] 1.1 Injetar leitos mockados em `IndicadoresProvider.get_indicadores_gerais` quando `MOCK_BEDS=true`
- [x] 1.2 Corrigir o filtro de leitos ocupados para ser insensível a maiúsculas/minúsculas no provedor de indicadores

## 2. Corrigir Vulnerabilidades e Validação

- [x] 2.1 Executar `npm audit fix` no frontend e certificar que o build do frontend compila sem erros
- [x] 2.2 Verificar o cálculo da taxa de ocupação localmente
- [x] 2.3 Submeter alterações, enviar ao repositório remoto e implantar na máquina virtual (VM)
