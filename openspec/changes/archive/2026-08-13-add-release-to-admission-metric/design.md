## Context

Atualmente, o UTI Manager apresenta os seguintes tempos operacionais do fluxo cirúrgico:
1. **Recepção Pós-Cirúrgico (BC):** Fim da Cirurgia até a Admissão na UTI.
2. **Liberação Encaminhamento:** Fim da Cirurgia até a Liberação de Encaminhamento pela UTI.

Para ter uma visão completa da logística de transferência do paciente, a coordenação solicitou a adição de um terceiro tempo:
3. **Encaminhamento até Admissão:** Medição específica da etapa de transporte físico (da Liberação do Encaminhamento pela UTI até a Admissão definitiva na UTI).

## Goals / Non-Goals

**Goals:**
- Calcular o tempo médio de encaminhamento até admissão (em minutos) para solicitações concluídas no período de filtragem.
- Exibir este tempo no payload JSON da API e em um novo card no painel de indicadores (frontend).

**Non-Goals:**
- Alterar o fluxo de transição de status das solicitações.
- Criar novos endpoints de API (vamos usar o endpoint `/api/indicadores/resumo` existente).

## Decisions

### 1. Fórmula de Cálculo no Backend
Usaremos a diferença entre o evento de admissão final (`conclusao`) e a data de liberação do encaminhamento registrada na solicitação (`encaminhamento_liberado_em`).

**Alternativa considerada:** Buscar o evento de histórico do tipo `encaminhamento_liberado`.
*   *Decisão:* Usar o campo `sol.encaminhamento_liberado_em` da tabela de solicitações (`solicitacoes_leito`) se disponível, pois é mais direto. Se não estiver populado, podemos cruzar com o evento `encaminhamento_liberado` do histórico para o prontuário.
*   *Abordagem final:* 
    ```python
    tempos_encaminhamento_admissao = []
    for ev in novas_internacoes_periodo:
        sol = find_solicitacao(ev)
        if sol and sol.encaminhamento_liberado_em:
            diff = (ev.criado_em - sol.encaminhamento_liberado_em).total_seconds() / 60.0 # minutos
            if diff >= 0:
                tempos_encaminhamento_admissao.append(diff)
    ```
    Isso calcula o tempo de transporte em minutos de forma precisa e eficiente.

### 2. Layout do Frontend
No arquivo `frontend/src/views/Indicadores.vue`, adicionaremos o novo card na seção de tempos médios (gargalos).
*   A classe do grid da seção será ajustada de `xl:grid-cols-5` para `xl:grid-cols-3 2xl:grid-cols-6` para acomodar o sexto card de forma elegante em telas grandes e responsivas.
*   Utilizaremos a função de formatação `formatarTempoLiberacao` existente para formatar o resultado em minutos ou horas/minutos conforme necessário.

## Risks / Trade-offs

- **[Risco]** Solicitações antigas ou importadas que não tenham o campo `encaminhamento_liberado_em` preenchido.
  - *Mitigação:* O cálculo ignora solicitações que não possuam ambas as datas preenchidas (retornando `0` como fallback), evitando divisões por zero ou erros no carregamento.
