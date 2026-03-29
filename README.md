# Quitanda Backend

## Requisitos

1. Python 3.14
2. uv
3. docker

## Seed do banco para testes

1. Suba o banco e aplique as migrations.
2. Execute o seed:

```bash
source .venv/bin/activate
python -m app.seed
```

Opcional: manter dados existentes e apenas inserir (sem truncate):

```bash
python -m app.seed --no-reset
```

Usuarios de teste criados (senha `123456`):

- `admin@quitanda.local` (ADMIN)
- `cliente1@quitanda.local` (CLIENTE)
- `cliente2@quitanda.local` (CLIENTE)
- `vendedor1@quitanda.local` (VENDEDOR ativo)
- `vendedor2@quitanda.local` (VENDEDOR ativo)
- `vendedor3@quitanda.local` (VENDEDOR inativo)

## CI/CD com GitHub Actions

Workflow criado em `.github/workflows/ci-cd.yml`.

### Fluxo

1. CI em pull request para `main`:

   - instala dependencias com `uv`
   - valida sintaxe Python
   - valida os dois arquivos compose
   - builda a imagem Docker

1. CD em push para `main`:

   - builda e publica imagem em `ghcr.io/<owner>/quitanda-backend`
   - conecta no servidor via SSH
   - faz `git pull` no diretorio de deploy
   - faz pull da nova imagem e sobe stack com `docker compose -f docker-compose.prod.yml up -d`

### Secrets obrigatorios no repositorio

- `DEPLOY_HOST`: host/IP do servidor
- `DEPLOY_USER`: usuario SSH
- `DEPLOY_SSH_KEY`: chave privada SSH (conteudo completo)
- `DEPLOY_PORT`: porta SSH (opcional, default 22)
- `DEPLOY_PATH`: caminho do projeto no servidor (ex: `/opt/quitanda-backend`)
- `GHCR_USERNAME`: usuario com permissao de leitura no GHCR
- `GHCR_READ_TOKEN`: token com `read:packages` para pull no servidor

### Variaveis no servidor (`.env`)

Garanta que o `.env` de producao tenha, no minimo:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- demais variaveis usadas por `app/settings.py`

O workflow injeta automaticamente:

- `API_IMAGE=ghcr.io/<owner>/quitanda-backend`
- `IMAGE_TAG=<commit_sha>`

Essas variaveis sao usadas em `docker-compose.prod.yml` para versionar o deploy por commit, sem build local no servidor.

## HTTPS automatico em producao (Nginx + Let's Encrypt)

O compose de producao inclui:

- `nginx` como reverse proxy (portas 80 e 443)
- `certbot` para emissao e renovacao automatica de certificados

### Variaveis necessarias no `.env` de producao

- `DOMAIN_NAME`: dominio publico apontando para o servidor (ex: `api.seudominio.com`)
- `LETSENCRYPT_EMAIL`: email para registro no Let's Encrypt
- `NGINX_HTTP_PORT` (opcional, default `80`)
- `NGINX_HTTPS_PORT` (opcional, default `443`)

### Como funciona

1. `cert_init` cria um certificado temporario local para o Nginx subir sem erro.
2. `certbot` solicita certificado valido do Let's Encrypt via desafio HTTP (`/.well-known/acme-challenge/`).
3. Nginx recarrega periodicamente e passa a servir o certificado valido quando disponivel.

Para o certificado ser emitido, o dominio precisa apontar para o IP do servidor e a porta 80 precisa estar aberta.
