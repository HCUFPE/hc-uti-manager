## Context

O usuário deseja manter o comportamento implementado onde novas alterações de destino geram históricos com "Alterou destino de alta" e alertas com o título "Alterou o Destino de Alta". No entanto, para a base de dados histórica (registros antigos):
- Devemos rodar um script retroativo para corrigir os registros da tabela `historico_acoes` (histórico antigo).
- NÃO é necessário fazer nenhum ajuste ou migração para os alertas antigos salvos no banco.

## Goals / Non-Goals

**Goals:**
- Manter a diferenciação semântica tanto no histórico quanto nos alertas para novos eventos.
- Escrever um script em `scratch/fix_historical_actions.py` que execute a correção retroativa dos históricos antigos na base SQLite da VM.

**Non-Goals:**
- Não alterar registros de alertas antigos já persistidos na base de dados.

## Decisions

### Manutenção da Engine de Alertas
Decidido manter as alterações na `AlertaController` e `AltasController` de forma que os novos alertas e novos históricos sigam a regra de diferenciação de leito de destino definida vs leito de destino alterado.

### Script de Correção Retroativa
Criar um script em `scratch/fix_historical_actions.py` utilizando SQLAlchemy para buscar todos os registros com `tipo = 'alteracao_destino'` agrupados por prontuário e ordenados por data. Para cada prontuário, a partir do segundo registro cronológico em diante, atualizamos `acao = 'Alterou destino de alta'` e salvamos.
Este script é executado dentro do container na VM de produção para atuar diretamente na base local SQLite real.

## Risks / Trade-offs

Nenhum risco.
