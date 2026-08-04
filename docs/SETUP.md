# Guia de Instalacao e Execucao

Este guia contem os passos detalhados para configurar o ambiente de desenvolvimento local e implantar a aplicacao em producao na VM.

## Pre-requisitos
- Git
- Python 3.10 ou superior
- Node.js 18 ou superior

---

## Opcao A: Ambiente de Desenvolvimento Local (Manual)

Utilize esta opcao para programar e testar alteracoes no seu computador pessoal de forma nativa.

### 1. Configuracao do Backend
Execute estes comandos na raiz do projeto:

```bash
# 1. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# 2. Instale as dependencias
pip install -r requirements.txt

# 3. Configure as variaveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais e segredos locais
nano .env
```

### 2. Configuracao do Frontend
Execute estes comandos em um novo terminal:

```bash
# 1. Navegue ate a pasta do frontend e instale as dependencias
cd frontend
npm install
```

### 3. Executando em Desenvolvimento

- **Iniciar o Backend:**
  ```bash
  # Na raiz do projeto, com o .venv ativo
  uvicorn src.main:app --reload
  ```
  O backend ficara acessivel em `http://127.0.0.1:8000`. A documentacao interativa (Swagger UI) estara em `/docs`.

- **Iniciar o Frontend:**
  ```bash
  # Na pasta frontend/
  npm run dev
  ```
  O frontend ficara acessivel em `http://127.0.0.1:5173`. O Vite redirecionara todas as chamadas de `/api` automaticamente para o backend local.

### 4. Build de Producao do Frontend
Para gerar os arquivos estaticos finais a serem servidos pelo backend:
```bash
# Na pasta frontend/
npm run build
```

---

## Opcao B: Ambiente de Producao com Podman (VM de Producao)

Esta opcao descreve a arquitetura utilizada no servidor de producao, onde a aplicacao roda empacotada em containers gerenciados via **Podman** e monitorados pelo **systemd**.

### 1. Servico no Systemd
Para que a aplicacao inicialize automaticamente junto com o sistema operacional e reinicie em caso de falhas, configuramos o servico systemd:

1. Copie o arquivo de servico fornecido no repositorio para a VM:
   ```bash
   cp /var/app/hc-uti-manager/hc-uti.service /etc/systemd/system/
   ```
2. Recarregue os daemon do systemd:
   ```bash
   systemctl daemon-reload
   ```
3. Habilite e inicie o servico:
   ```bash
   systemctl enable hc-uti.service
   systemctl start hc-uti.service
   ```
4. Acompanhe os logs da aplicacao em tempo real:
   ```bash
   journalctl -u hc-uti.service -f
   ```

### 2. Rotina de Backup Automatico (Cron)
Um script de backup diario do banco de dados SQLite local com rotacao automatica e executado no cron da VM:

1. Dê permissao de execucao no script:
   ```bash
   chmod +x /var/app/hc-uti-manager/scratch/backup_db.sh
   ```
2. Agende o script no Cron para rodar diariamente as 02:00:
   ```bash
   (crontab -l 2>/dev/null; echo "0 2 * * * /var/app/hc-uti-manager/scratch/backup_db.sh > /dev/null 2>&1") | crontab -
   ```

### 3. Rotina de Atualizacao / Deploy na VM
Para atualizar a aplicacao na VM quando novos commits forem enviados para a branch `master`:

1. **Fazer Backup do Banco Local:**
   ```bash
   podman exec hc-uti-backend sqlite3 /app/data/app.db ".backup '/app/data/backup_pre_deploy.db'"
   ```
2. **Atualizar o Codigo Fonte:**
   ```bash
   git pull origin master
   ```
3. **Recompilar a Imagem do Podman:**
   ```bash
   podman build --no-cache -t localhost/hc-uti-manager_backend:latest .
   ```
4. **Reiniciar o Servico no Systemd:**
   ```bash
   systemctl restart hc-uti.service
   ```
5. **Rodar Migracoes de Banco (Alembic):**
   ```bash
   podman exec hc-uti-backend alembic upgrade head
   ```

*(Nota: O utilitario local `.venv/bin/python scratch/git_pull_and_rebuild.py` pode ser executado para rodar todos esses comandos na VM de forma remota via SSH).*

### 4. Manutencao de Logs e Limpeza de Disco
Para evitar quedas do container ou falhas de deploy por falta de espaco em disco, execute a limpeza periodica na VM:
```bash
# Limpa cache do gerenciador de pacotes do host
apt-get clean

# Reduz o tamanho de logs acumulados no journald
journalctl --vacuum-size=50M

# Limpa caches e containers antigos orfaos do Podman
export XDG_RUNTIME_DIR=/run/user/$(id -u)
podman system prune -a -f
```
