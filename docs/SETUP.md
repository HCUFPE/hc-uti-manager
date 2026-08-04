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

### 1. Sistema Operacional e Utilitários de Base
A VM roda Debian/Ubuntu-like Linux. Instale os utilitarios essenciais de rede e administracao no host:
```bash
sudo apt update && sudo apt install -y git curl ufw systemd openssh-server python3
```

### 2. Runtime de Containers (Podman)
Este projeto utiliza o Podman para gerenciar a execucao dos containers de producao (Backend + Nginx):
```bash
sudo apt install -y podman podman-compose
```

### 3. Estruturacao de Pastas e Clone do Codigo
No host da VM, a aplicacao deve ser implantada no diretorio `/var/app/`:

1. Crie o diretorio de destino e ajuste as permissoes para o usuario local:
   ```bash
   sudo mkdir -p /var/app/hc-uti-manager
   sudo chown -R $USER:$USER /var/app/hc-uti-manager
   ```
2. Clone o repositorio do Git na pasta criada:
   ```bash
   git clone <URL_DO_REPOSITORIO> /var/app/hc-uti-manager
   ```
3. Crie a pasta de dados persistentes utilizada pelo SQLite (para manter os logs locais e reservas de leito):
   ```bash
   mkdir -p /var/app/hc-uti-manager/data
   ```

### 4. Configuracao das Variaveis de Ambiente (.env)
Crie e preencha o arquivo `/var/app/hc-uti-manager/.env` com as configuracoes corporativas da VM:
```bash
cp /var/app/hc-uti-manager/.env.example /var/app/hc-uti-manager/.env
nano /var/app/hc-uti-manager/.env
```

**Principais variaveis a configurar:**
* `SQLITE_DSN=sqlite+aiosqlite:///./data/app.db` (Banco local do sistema de UTI)
* `POSTGRES_DSN=postgresql+asyncpg://usuario:senha@ip_do_banco:5432/aghu` (Conexao com o banco de dados do AGHU)
* `AD_URL=ldap://ip_do_ad:389` e `AD_BASEDN=dc=ebserh,dc=gov,dc=br` (Integracao com o Active Directory para autenticacao)
* `JWT_SECRET=sua_chave_secreta` (Seguranca do token de sessao)

### 5. Configuracao do Servidor Web (Nginx e SSL)
O container do Nginx atua como proxy reverso para o backend FastAPI e gerencia as conexoes seguras (HTTPS). Para que ele funcione corretamente, os certificados SSL devem ser configurados no host da VM:

1. Crie o diretorio para armazenar as chaves de seguranca SSL:
   ```bash
   mkdir -p /var/app/hc-uti-manager/nginx/ssl
   ```
2. Insira os arquivos de certificado corporativo do hospital na pasta criada com os nomes exatos esperados pela configuracao do Nginx:
   * Certificado público: `/var/app/hc-uti-manager/nginx/ssl/server.crt`
   * Chave privada: `/var/app/hc-uti-manager/nginx/ssl/server.key`

*(Nota: O arquivo `/var/app/hc-uti-manager/nginx/default.conf` ja vem configurado no repositorio para fazer o redirecionamento automatico da porta 80 para a 443 com HTTPS).*

### 6. Persistencia do Servico (Systemd)
Para garantir que a aplicacao inicialize automaticamente junto com o sistema operacional e reinicie em caso de falhas:

1. Copie o arquivo de servico fornecido no repositorio para a VM:
   ```bash
   sudo cp /var/app/hc-uti-manager/hc-uti.service /etc/systemd/system/
   ```
2. Recarregue os daemon do systemd:
   ```bash
   sudo systemctl daemon-reload
   ```
3. Habilite e inicie o servico:
   ```bash
   sudo systemctl enable hc-uti.service
   sudo systemctl start hc-uti.service
   ```
4. **Executar as Migrações do Banco de Dados (Primeira Inicialização):**
   Logo após o container subir pela primeira vez, execute o comando do Alembic para criar a estrutura inicial de tabelas no banco de dados SQLite:
   ```bash
   podman exec hc-uti-backend alembic upgrade head
   ```
5. Acompanhe os logs da aplicacao em tempo real:
   ```bash
   journalctl -u hc-uti.service -f
   ```

### 7. Rotina de Backup Automatico (Cron)
Um script de backup diario do banco de dados SQLite local com rotacao automatica e executado no cron da VM:

1. Dê permissao de execucao no script:
   ```bash
   chmod +x /var/app/hc-uti-manager/scratch/backup_db.sh
   ```
2. Agende o script no Cron para rodar diariamente as 02:00:
   ```bash
   (crontab -l 2>/dev/null; echo "0 2 * * * /var/app/hc-uti-manager/scratch/backup_db.sh > /dev/null 2>&1") | crontab -
   ```

### 8. Rotina de Atualizacao / Deploy na VM
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
   sudo systemctl restart hc-uti.service
   ```
5. **Rodar Migracoes de Banco (Alembic):**
   ```bash
   podman exec hc-uti-backend alembic upgrade head
   ```

*(Nota: O utilitario local `.venv/bin/python scratch/git_pull_and_rebuild.py` pode ser executado para rodar todos esses comandos na VM de forma remota via SSH).*

### 9. Manutencao de Logs e Limpeza de Disco
Para evitar quedas do container ou falhas de deploy por falta de espaco em disco, execute a limpeza periodica na VM:
```bash
# Limpa cache do gerenciador de pacotes do host
sudo apt-get clean

# Reduz o tamanho de logs acumulados no journald
sudo journalctl --vacuum-size=50M

# Limpa caches e containers antigos orfaos do Podman
export XDG_RUNTIME_DIR=/run/user/$(id -u)
podman system prune -a -f
```
