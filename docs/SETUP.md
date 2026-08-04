# Guia de Instalacao e Execucao

Este guia contem os passos detalhados para configurar e executar os ambientes de desenvolvimento do backend e do frontend.

## Pre-requisitos

- Python 3.10 ou superior
- Node.js 18 ou superior
- Git

## Opcao A: Executar com Podman (rapido)

1. Na raiz do repositorio, copie e ajuste suas variaveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env conforme seu ambiente (AD, banco, JWT, etc.)
   ```
2. Ainda na raiz, suba os servicos:
   ```bash
   podman-compose up --build
   ```

- Backend em `http://127.0.0.1:8000` e frontend em `http://127.0.0.1:5173`.
- Use esta opcao se quiser um ambiente pronto rapidamente utilizando o Podman; lembre-se de revisar `.env` para conectar ao seu AD ou banco real.

## Opcao B: Ambiente local manual

### 1. Configuracao do Backend

Siga estes passos a partir da raiz do repositorio.

```bash
# 1. Clone o repositorio (se ainda nao o fez)
# git clone <url-do-repositorio>
# cd <nome-do-repositorio>

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# 3. Instale as dependencias do Python
pip install -r requirements.txt

# 4. Configure as variaveis de ambiente
# Copie o arquivo de exemplo para criar seu arquivo de configuracao local
cp .env.example .env

# Edite o arquivo .env com suas configuracoes (banco de dados, segredos, etc.)
# Dica: Para desenvolvimento offline, voce pode deixar as variaveis de AD e POSTGRES comentadas.
nano .env
```

### 2. Configuracao do Frontend

Estes passos devem ser executados em um novo terminal.

```bash
# 1. Navegue ate a pasta do frontend
cd frontend

# 2. Instale as dependencias do Node.js
npm install
```

### 3. Executando a Aplicacao

#### Servidor de Backend

Com o ambiente virtual (`.venv`) ativado, execute o servidor FastAPI a partir da raiz do projeto.

```bash
uvicorn src.main:app --reload
```

- O backend estara disponivel em `http://127.0.0.1:8000`.
- A documentacao interativa da API (Swagger UI) estara em `http://127.0.0.1:8000/docs`.
- A documentacao alternativa (ReDoc) estara em `http://127.0.0.1:8000/redoc`.

#### Servidor de Frontend

Na pasta `frontend/`, execute o servidor de desenvolvimento do Vite.

```bash
npm run dev
```

- O frontend estara disponivel em `http://127.0.0.1:5173` (ou outra porta indicada pelo Vite). O servidor de desenvolvimento do Vite ja vem configurado com um proxy para o backend, entao todas as chamadas de API para `/api` serao redirecionadas automaticamente para `http://127.0.0.1:8000`.

### 4. Build de Producao do Frontend

Para gerar a versao de producao do frontend, que e servida diretamente pelo FastAPI:

```bash
# Na pasta frontend/
npm run build
```

Os arquivos gerados em `frontend/dist/` serao servidos pela aplicacao FastAPI quando ela nao estiver em modo de desenvolvimento, na rota raiz (`/`).

---

## Opcao C: Executar em Producao com Podman (VM de Producao)

Para o ambiente de producao corporativo na VM, o sistema e executado utilizando o **Podman** e gerenciado via **systemd**.

### 1. Pre-requisitos na VM
- Podman e Podman-Compose instalados.
- Diretorio do projeto localizado em `/var/app/hc-uti-manager`.
- Arquivo `.env` configurado na raiz com as variaveis corretas (especialmente `POSTGRES_DSN` e segredos JWT).

### 2. Configurar o Servico no Systemd
Para garantir que a aplicacao inicialize automaticamente com o sistema operacional e seja reiniciada em caso de falhas, utilizamos o arquivo de servico fornecido no repositorio:

1. Copie o arquivo de servico para a pasta do systemd:
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
4. Veja os logs do servico em tempo real:
   ```bash
   journalctl -u hc-uti.service -f
   ```

### 3. Rotina de Backup Automatico do SQLite (Cron)
Para evitar perda de dados nas reservas locais e configuracoes extras, configuramos um script de backup diario com rotacao automatica:

1. Garanta permissao de execucao no script:
   ```bash
   chmod +x /var/app/hc-uti-manager/scratch/backup_db.sh
   ```
2. Agende o script no Cron para rodar diariamente as 02:00 da manha:
   ```bash
   (crontab -l 2>/dev/null; echo "0 2 * * * /var/app/hc-uti-manager/scratch/backup_db.sh > /dev/null 2>&1") | crontab -
   ```

### 4. Pipeline de Deploy / Atualizacao Manual (Script de Rebuild)
Sempre que uma atualizacao for enviada para a branch `master`, execute a rotina abaixo para atualizar a VM de producao sem perder dados:

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
5. **Rodar Migracoes Pendentes de Banco (Alembic):**
   ```bash
   podman exec hc-uti-backend alembic upgrade head
   ```

*(Nota: Voce pode automatizar esse processo rodando diretamente o utilitario `.venv/bin/python scratch/git_pull_and_rebuild.py` a partir do host local do desenvolvedor).*

### 5. Manutencao e Limpeza de Disco na VM
Se o disco da VM ficar cheio, impedindo o deploy ou fazendo o container cair, execute a rotina de limpeza de logs e cache:
```bash
# Limpa cache do gerenciador de pacotes
apt-get clean

# Reduz o tamanho de logs acumulados no journald
journalctl --vacuum-size=50M

# Limpa caches e containers antigos orfaos do Podman
export XDG_RUNTIME_DIR=/run/user/$(id -u)
podman system prune -a -f
```

