## Context

Para realizar a limpeza preservando os perfis e fazer a carga retroativa (backfill) das novas colunas de Nome, Lotação e E-mail para os usuários já cadastrados na VM, criaremos uma rotina de execução. 

Como o servidor de Active Directory (`10.34.0.101`) é interno da rede hospitalar e as bibliotecas Python necessárias (`ldap3`, `sqlalchemy`) estão instaladas apenas dentro do container da aplicação (`hc-uti-backend`), executaremos as queries de sincronização diretamente no ambiente do container.

## Goals / Non-Goals

**Goals:**
- Validar se o script `scratch/clean_vm_db.py` preserva a tabela `usuarios_perfis` (sim, já preserva).
- Criar o script utilitário `scratch/backfill_ad_details.py` que inicia a conexão SSH, injeta o script de sincronização dentro do container `hc-uti-backend` e executa a varredura e atualização.
- Atualizar todos os perfis ativos na VM com as novas colunas extraídas do AD.

**Non-Goals:**
- Modificar permissões ou grupos no AD.
- Automatizar o backfill para rodar a cada deploy (deve ser acionado apenas uma vez ou sob demanda).

## Decisions

### 1. Execução do backfill de dados dentro do container
- **Opção A:** Executar o script no host da VM.
- **Opção B (Escolhida):** Enviar o script para o host da VM e executá-lo dentro do container do backend (`podman exec`) conectando ao banco de dados SQLite `/app/data/app.db`.
- **Razoamento:** O host da VM não tem as dependências instaladas (como `ldap3` e `sqlalchemy`), enquanto o container possui todo o ecossistema pronto, além das permissões de rede necessárias para contatar o AD.

## Risks / Trade-offs

- **[Risco]** Algum usuário cadastrado no banco local não existir mais no AD.
  - **Mitigação:** Tratar a exceção de usuário não encontrado individualmente, registrando o log de alerta e continuando a execução do script para os demais usuários.
