## 1. Scripts de Limpeza de Dados

- [x] 1.1 Criar o script Python `scratch/production_cleanup.py` para purgar a base local de simulações e remover os usuários padrão (`admin`, `bloco`, `nir`, `uti`).

## 2. Configurações na VM e Deploy

- [ ] 2.1 Atualizar as variáveis de ambiente no arquivo `.env` da VM definindo `MOCK_BEDS=false`.
- [ ] 2.2 Executar o script `production_cleanup.py` dentro do container da aplicação na VM.
- [ ] 2.3 Reiniciar os serviços da aplicação para aplicar o censo real do AGHU e as novas restrições de login.
