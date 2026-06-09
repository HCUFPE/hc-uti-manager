## 1. Implementar Mudança no Backend

- [x] 1.1 Remover a lógica de fallback mockada do tempo médio de liberação de encaminhamento em `src/providers/implementations/indicadores_provider.py`
- [x] 1.2 Verificar se existem testes unitários/integração que dependem do valor mockado `45.2` e corrigi-los para esperar `0.0` em banco de dados limpo

## 2. Validação e Homologação

- [x] 2.1 Criar e executar um script de validação local para atestar que o indicador retorna `0.0` com o banco vazio
- [x] 2.2 Submeter as mudanças ao Git, realizar push para o repositório remoto e atualizar a máquina virtual (VM)
