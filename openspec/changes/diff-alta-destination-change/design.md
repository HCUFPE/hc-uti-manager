## Context

Atualmente, `AltasController.atualizar_destino` registra a mesma ação no histórico ("Definiu destino de alta") em ambos os casos.
E em `AlertaController._gerar_alerta_por_tipo`, o evento com `tipo == "alteracao_destino"` gera um título de alerta fixo "Destino de Alta Definido".

## Goals / Non-Goals

**Goals:**
- Registrar "Alterou destino de alta" quando já houver leito de destino cadastrado na solicitação de alta.
- Exibir o alerta "Alterou o Destino de Alta" na tela da UTI quando houver essa alteração.

**Non-Goals:**
- Não criar novas tabelas no banco de dados.

## Decisions

### Detecção de Destino Anterior
Em `AltasController.atualizar_destino`, verificaremos se `alvo.leito_destino` (o valor atual no banco) não é nulo/vazio antes de aplicar o novo leito de destino vindo de `payload['leitoDestino']`.
- Se `alvo.leito_destino` já continha um valor diferente do novo valor, registra no histórico a ação: `"Alterou destino de alta"`.
- Caso contrário, registra: `"Definiu destino de alta"`.

### Detecção no Gerador de Alertas
Em `AlertaController._gerar_alerta_por_tipo`, quando `tipo == "alteracao_destino"`, verificaremos os `detalhes` ou a `acao` do evento histórico.
Como `_gerar_alerta_por_tipo` recebe `detalhes` (e o histórico registra os detalhes como `f"Leito {alvo.lto_id}: Destino {payload['leitoDestino']}"`), podemos alterar a assinatura do método ou a forma de buscar a ação, OU passar `ev` inteiro para o gerador de alertas!
Espere, vamos analisar a assinatura de `_gerar_alerta_por_tipo` em `alerta_controller.py`:
```python
207:     def _gerar_alerta_por_tipo(self, tipo, detalhes, operador, criado_em_evento, pront_alerta, perfil_vaga, match_hoje, novos_alertas):
```
Espera! Podemos passar a `acao` do evento para `_gerar_alerta_por_tipo`!
No loop de `_analisar_historico`:
```python
140:         tipo = ev.get("tipo")
141:         detalhes = ev.get("detalhes", "")
142:         operador = ev.get("operador", "Sistema")
143:         criado_em_evento = ev.get("criado_em")
144:         prontuario_evento = ev.get("prontuario")
```
Se passarmos também `acao = ev.get("acao", "")` para `_processar_evento_historico` e `_gerar_alerta_por_tipo`, podemos fazer a distinção limpa:
```python
        # 4. NIR -> UTI (Destino)
        elif tipo in ["alteracao_destino", "destino_disponivel", "destino_pendente"]:
            titulo = "Destino de Alta Definido"
            if tipo == "alteracao_destino" and acao == "Alterou destino de alta":
                titulo = "Alterou o Destino de Alta"
```
Isso é muito limpo e direto!

## Risks / Trade-offs

Nenhum risco.
