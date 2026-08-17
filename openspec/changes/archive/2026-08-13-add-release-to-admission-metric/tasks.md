## 1. Backend Implementation

- [x] 1.1 Calcular tempo_medio_encaminhamento_admissao_minutos no provedor de indicadores (src/providers/implementations/indicadores_provider.py)
- [x] 1.2 Incluir a nova métrica no payload JSON retornado pela API get_indicadores_gerais

## 2. Frontend Implementation

- [x] 2.1 Adicionar card de tempo de 'Encaminhamento até Admissão' no painel de indicadores (frontend/src/views/Indicadores.vue)
- [x] 2.2 Ajustar o grid de cards de tempos médios de processo para comportar 6 cards de forma elegante

## 3. Verification & Deploy

- [x] 3.1 Verificar localmente o correto carregamento do JSON de indicadores e o layout responsivo do painel
- [x] 3.2 Realizar o commit e deploy automático na VM e testar o funcionamento em produção
