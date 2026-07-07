## 1. Limpeza do Banco de Dados

- [x] 1.1 Revisar o arquivo `scratch/clean_vm_db.py` para garantir que a tabela `usuarios_perfis` não seja afetada pela exclusão de dados transacionais
- [x] 1.2 Executar a limpeza do banco na VM rodando o script `scratch/clean_vm_db.py`

## 2. Script e Execução de Backfill (Carga Retroativa)

- [x] 2.1 Criar o script utilitário `scratch/backfill_ad_details.py` no repositório local
- [x] 2.2 Implementar a lógica no script para transferir e executar o comando de sincronização em lote dentro do container `hc-uti-backend` na VM
- [x] 2.3 Executar o script `scratch/backfill_ad_details.py` para carregar as informações do AD para todos os perfis existentes na base de dados da VM
