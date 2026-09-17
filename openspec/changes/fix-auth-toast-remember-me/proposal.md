## Why

Ao acessar o sistema ou quando a sessão do usuário expira, o componente `Home.vue` tenta carregar os leitos (`GET /api/leitos`) antes/durante o processo de navegação e autenticação. Quando o servidor retorna `401 Unauthorized`, o frontend redireciona para a rota `/login`, mas dispara indevidamente um toast de erro em vermelho ("Falha ao carregar leitos. Verifique a conexao."), criando uma mensagem falsa de erro de rede. Além disso, a opção "Lembrar de mim" no login estava configurada para apenas 15 minutos em vez de estender a sessão.

## What Changes

- **Tratamento de Toast no Login/Home**: Silenciar notificações de erro de carregamento de leitos quando o erro for `401 Unauthorized` ou quando o usuário não estiver autenticado.
- **Ajuste no Tempo do Token (Lembrar de mim)**: Ajustar a regra do backend em `src/routers/auth.py` para que ao marcar "Lembrar de mim", o token de acesso seja emitido com validade de 7 dias (168 horas), mantendo o login padrão com validade de 24 horas.
- **Sincronização de Especificação e Changelog**: Atualização dos documentos de requisitos e histórico de versões do projeto.

## Capabilities

### New Capabilities
- Nenhuma nova funcionalidade requerida.

### Modified Capabilities
- Nenhuma alteração em capacidades core de especificação do OpenSpec.

## Impact

- `frontend/src/views/Home.vue`: Filtro no tratamento do `catch` em `loadLeitos()`.
- `src/routers/auth.py`: Validade da expiração do token JWT na rota de login.
- `docs/projeto_inicial/02-requisitos.md` e `CHANGELOG.md`: Sincronização da documentação.
