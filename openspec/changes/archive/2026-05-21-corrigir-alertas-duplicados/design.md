## Context

Durante os testes do sistema, foram reportados alertas duplicados para perfis como a UTI e NIR. A investigação do código em [alerta_controller.py](file:///c:/Users/daniel.turmina/Documents/HC-UTI-Manager/src/controllers/alerta_controller.py) revelou que o problema principal está na sincronização de alertas:
1. **Comparação Inexata de Datetime:** O método `_sincronizar_alertas` compara as datas de criação dos alertas usando `a.criado_em == data.get("criado_em")`. Como os valores salvos no banco de dados SQLite podem sofrer pequenas variações de precisão (subsegundos/milissegundos) ou formatação em relação aos objetos datetime em memória, a busca por alertas existentes falha. Isso faz com que alertas de histórico sejam recriados em toda execução da rotina.
2. **Alertas de Estado Sem Timestamp Real:** Os alertas do tipo "Gargalo" gerados no método `_analisar_altas` (como "Solicitação de Alta" e "Acomodação Definida") não possuem um campo `criado_em` no dicionário gerador, o que resulta em `data.get("criado_em")` sendo `None`. Consequentemente, a rotina de detecção de duplicados pode erroneamente agrupar ou deixar de diferenciar eventos separados no tempo se usarem a mesma mensagem.

O usuário manifestou explicitamente que **não deseja** a remoção ou limpeza automática de nenhum alerta do tipo "Gargalo" (ou baseado em histórico), mesmo que a condição que os gerou não seja mais ativa, pois a preservação desse histórico no banco de dados local é de suma importância.

## Goals / Non-Goals

**Goals:**
- Ajustar a comparação de datas na sincronização para tolerar variações de precisão (limite de 2 segundos de diferença), garantindo a detecção confiável de alertas existentes e evitando duplicações indesejadas.
- Atribuir o timestamp real do objeto `alta` (`alta.criado_em` ou `alta.atualizado_em`) aos alertas gerados dinamicamente em `_analisar_altas`.
- **Preservar todo o histórico de alertas "Gargalo"**: Garantir que a lógica de limpeza de alertas obsoletos continue ignorando os alertas do tipo "Gargalo" (mantendo a regra que apenas limpa `Infeccioso`, `Permanencia` e `Limpeza`).

**Non-Goals:**
- Implementar limpeza de alertas "Gargalo" obsoletos ou antigos.
- Alterar o comportamento no frontend.

## Decisions

### 1. Robustez na Comparação de Datetime na Sincronização
Para evitar falsos negativos na busca por alertas existentes decorrentes de diferenças de milissegundos do SQLite:
- **Decisão:** Usar a diferença absoluta de tempo: `abs((a.criado_em - data.get("criado_em")).total_seconds()) < 2` no método de verificação de alertas existentes. Se a diferença for menor que 2 segundos, consideramos as datas equivalentes.

### 2. Atribuição de Timestamps Reais para Alertas de Alta
- **Decisão:** Em `_analisar_altas`, passar o campo `"criado_em": alta.criado_em` para alertas de "Solicitação de Alta" e `"criado_em": alta.atualizado_em` para alertas de "Acomodação Definida". Isso garante que alertas de solicitações diferentes (que ocorrem em momentos distintos) tenham timestamps distintos e não sejam incorretamente fundidos ou sobrescritos.

### 3. Preservação de Histórico de Alertas
- **Decisão:** Manter a rotina de limpeza de obsoletos exatamente como está, sem deletar alertas "Gargalo" expirados ou solucionados:
  ```python
  if a_antigo.categoria in ["Infeccioso", "Permanencia", "Limpeza"]:
      await self.alerta_provider.deletar(a_antigo.id)
  ```

## Risks / Trade-offs

- **[Risco]** Caso o banco SQLite armazene datas sem segundos (apenas minutos), a tolerância de 2 segundos pode não ser suficiente se a data for truncada no minuto.
  - **Mitigação:** Os testes prévios confirmam que o SQLite armazena com precisão de microsegundos (`%Y-%m-%d %H:%M:%S.%f`), então a tolerância de 2 segundos é ideal e segura.
