## Context

O painel de controle calcula a taxa de ocupação instantânea consultando o AGHU via `census_provider.listar_leitos()`. No entanto, quando `MOCK_BEDS=true` está ativo em desenvolvimento, os leitos retornados pelo AGHU (se houver) não contêm os leitos mockados. Para alinhar os indicadores com a listagem de leitos do painel, o `IndicadoresProvider` precisa injetar os mesmos leitos mockados que o `LeitosController` usa. Além disso, as dependências do frontend (Rollup, PostCSS, Axios) possuem vulnerabilidades de segurança alertadas pelo GitHub que serão corrigidas no arquivo de dependências.

## Goals / Non-Goals

**Goals:**
- Ajustar `IndicadoresProvider.get_indicadores_gerais` para carregar leitos mockados se `MOCK_BEDS == "true"`.
- Modificar o cálculo de ocupação para reconhecer o status de forma case-insensitive.
- Atualizar dependências vulneráveis do frontend para versões seguras usando o npm.

**Non-Goals:**
- Mudar regras de negócio do censo no ambiente de produção.
- Corrigir vulnerabilidades que exijam grandes quebras de compatibilidade em frameworks principais sem validação prévia.

## Decisions

- **Injeção de Mock no IndicadoresProvider**: Seguir o mesmo array de mocks definido no `LeitosController` caso `os.getenv("MOCK_BEDS") == "true"`.
- **Status Case-Insensitive**: Alterar o filtro para `str(l.get("status") or "").upper() == "OCUPADO"`.
- **npm audit fix**: Executar `npm audit fix` no diretório `frontend` para atualizar as vulnerabilidades de forma segura e não destrutiva.

## Risks / Trade-offs

- **Risco**: `npm audit fix` introduzir atualizações que quebrem o build do frontend.
- **Mitigação**: Executar `npm run build` localmente após a atualização para validar a integridade.
