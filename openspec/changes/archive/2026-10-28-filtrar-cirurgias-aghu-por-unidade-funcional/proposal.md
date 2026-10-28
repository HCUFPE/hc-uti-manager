# Proposal: Filtrar Cirurgias do AGHU por Unidade Funcional Cirúrgica

## Why

Atualmente, a rotina de busca de cirurgias no AGHU (`obter_cirurgia_aghu.sql`) consulta a tabela `agh.mbc_cirurgias` sem restringir a Unidade Funcional (`cir.unf_seq`). No AGHU/Ebserh, essa tabela é compartilhada tanto para cirurgias em centros cirúrgicos quanto para exames e procedimentos diagnósticos ambulatoriais sob sedação (como Endoscopia na Unidade Funcional `155`). Como a ordenação atual prioriza a proximidade de hoje (`CURRENT_DATE`), um exame diagnóstico de 10 minutos realizado pela manhã em uma unidade ambulatorial/endoscópica (ex: Duodenoscopia na Unidade 155) sobrepõe cirurgias de grande porte programadas para os próximos dias no Bloco Cirúrgico (Unidade 28), preenchendo incorretamente o formulário de reserva de leito de UTI.

## What Changes

- **Filtro de Unidade Funcional por Setor Solicitante**:
  - Restringir as cirurgias recuperadas do AGHU para considerar exclusivamente as Unidades Funcionais autorizadas:
    - **Bloco Cirúrgico (BC)**: Unidade Funcional `28` (`BLOCO CIRURGICO`);
    - **Centro Obstétrico (COB)**: Unidade Funcional `20` (`CENTRO OBSTETRICO`);
    - **Hemodinâmica (HEM)**: Unidade Funcional `47` (`HEMODINAMICA - PDT`) e `233` (`HEMODINAMICA (AMBULATORIO)`);
    - **Consulta Geral (Admin / UTI)**: Apenas o conjunto das unidades cirúrgicas válidas (`unf_seq IN (28, 20, 47, 233)`), excluindo unidades diagnósticas e ambulatoriais puras (como a Unidade `155` - Endoscopia).
- **Priorização de Cirurgias Agendadas (`situacao = 'AGND'`)**:
  - Ajustar o `ORDER BY` da consulta SQL para priorizar registros com situação `AGND` (Agendada) à frente de registros já finalizados (`RZDA`), evitando que procedimentos concluídos no mesmo dia sufoquem cirurgias agendadas.
- **Passagem de Parâmetro do Tipo/Perfil no Endpoint**:
  - O endpoint `GET /api/solicitacoes/consultar-aghu/{prontuario}` passará a aceitar o query parameter opcional `tipo` (ex: `Cirurgico`, `Obstetrico`, `HEM`), utilizando adicionalmente o perfil do usuário logado (`current_user`) para aplicar o filtro de `unf_seq` correspondente.
- **Atualização na Interface**:
  - Em `frontend/src/views/Solicitacoes.vue`, enviar o `tipo` selecionado durante a busca de dados do paciente no AGHU.

## Capabilities

### New Capabilities
*(Nenhuma nova capacidade introduzida)*

### Modified Capabilities
- `solicitacao-leitos`: Atualizar o requisito "Criação de Solicitação de Leito" para especificar que a importação de dados cirúrgicos do AGHU deve filtrar obrigatoriamente as unidades funcionais cirúrgicas permitidas (BC: 28, COB: 20, HEM: 47/233) e priorizar agendamentos ativos.

## Impact

- **SQL Backend**: `src/providers/sql/solicitacao/obter_cirurgia_aghu.sql`.
- **Provedor e Controller**: `src/providers/implementations/aghu_cirurgia_provider.py` e `src/controllers/solicitacao_leito_controller.py`.
- **API Roteador**: `src/routers/solicitacoes_leito.py` (aceitar `tipo: Optional[str] = Query(None)`).
- **Frontend**: `frontend/src/views/Solicitacoes.vue` (passar parâmetro `tipo` na chamada `api.get('/api/solicitacoes/consultar-aghu/...')`).
- **Documentação e Governança**: `docs/projeto_inicial/02-requisitos.md` e `CHANGELOG.md`.
