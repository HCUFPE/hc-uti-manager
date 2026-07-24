## Context

O usuário quer manter a alteração visual e semântica no histórico de ações ("Alterou destino de alta" vs "Definiu destino de alta"), mas deseja manter os alertas da UTI com o título padrão "Destino de Alta Definido" para evitar ruído.
Também é necessário corrigir a base de dados SQLite histórica na VM.

## Goals / Non-Goals

**Goals:**
- Reverter o mapeamento customizado de títulos na engine de alertas (mantendo "Destino de Alta Definido" para todos).
- Escrever um script em `scratch/fix_historical_actions.py` que execute a correção retroativa e possa ser rodado na VM via SSH.

**Non-Goals:**
- Não reverter a lógica em `AltasController` (a diferenciação de escrita de novas ações no histórico de ações continua ativa).

## Decisions

### Reversão do Título no Alerta Controller
Em `AlertaController._gerar_alerta_por_tipo`, removeremos o bloco condicional que verificava `acao == "Alterou destino de alta"` para alterar o título, fazendo com que a chave `alteracao_destino` sempre aponte para `"Destino de Alta Definido"`.

### Script de Correção Retroativa
Criar um script em `scratch/fix_historical_actions.py` utilizando SQLAlchemy para buscar todos os registros com `tipo = 'alteracao_destino'` agrupados por prontuário e ordenados por data. Para cada prontuário, a partir do segundo registro cronológico em diante, atualizamos `acao = 'Alterou destino de alta'` e salvamos.
Este script lerá as variáveis do `.env` local para saber qual banco conectar (na VM, conectará no SQLite local).

## Risks / Trade-offs

Nenhum risco.
