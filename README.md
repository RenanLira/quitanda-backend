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
