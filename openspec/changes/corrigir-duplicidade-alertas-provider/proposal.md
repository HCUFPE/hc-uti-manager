# Proposta de Mudança: Corrigir Duplicidade de Alertas no AlertaProvider

## Por que

Durante o diagnóstico de duplicidades no banco de dados de produção (`10.34.0.192`), foi identificado um único par de alertas duplicados (`#1017` e `#1018`) gerados no dia `02/09/2026 às 11:22:41`.

A investigação da causa raiz revelou que o método `criar()` em `src/providers/implementations/alerta_provider.py` executava uma consulta com igualdade estrita do campo de data/hora (`Alerta.criado_em == data.get("criado_em")`). Devido à divergência de tipos (string ISO v v. objeto datetime nativo do SQLite), a busca por duplicatas retornava falso e permitia a gravação de um segundo alerta idêntico.

## O que

1. **Ajuste na Query de Desduplicação (`AlertaProvider.criar`):**
   * Modificar a consulta SQL para buscar alertas com o mesmo `titulo`, `prontuario` e `mensagem` (e `perfil_alvo`, quando informado), dispensando a igualdade estrita de milissegundos de string no campo `criado_em`.
   * Caso já exista um alerta correspondente na base, o método `criar` retornará o alerta existente em vez de criar um novo registro.

2. **Limpeza da Duplicidade Existente em Produção:**
   * Executar uma rotina pontual de limpeza na base de Produção para remover a linha duplicada (`#1018`), preservando a de menor ID (`#1017`).

## Impacto

- Elimina 100% dos riscos de criação de alertas duplicados no banco de dados em execuções assíncronas paralelas.
- Não altera contratos de APIs nem estruturas de tabelas.
