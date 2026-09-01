## 1. Implementação no Backend

- [x] 1.1 Atualizar `AlertaController._gerar_alerta_por_tipo` em `src/controllers/alerta_controller.py` para tratar o tipo de evento de histórico `conclusao` e gerar alertas com `tipo="admissao_concluida"`, `categoria="Gargalo"`, `perfil_alvo="NIR"` e os textos/títulos customizados de admissão concluída no censo.

## 2. Implementação do Som e Lógica no Frontend

- [x] 2.1 Atualizar `useUiStore` em `frontend/src/stores/ui.ts` para implementar o novo som sintetizado `tocarAlertaAdmissao` utilizando a Web Audio API com oscilador do tipo `sine` e notas C-E-G ascendentes.
- [x] 2.2 Atualizar `verificarETocarSomGlobal` em `frontend/src/layouts/DefaultLayout.vue` para verificar se há alertas não lidos. Caso haja alertas padrão pendentes (urgentes), reproduzir o som de bipe padrão; se não houver alertas padrão, mas houver alertas do tipo `admissao_concluida`, reproduzir o novo som de admissão (`tocarAlertaAdmissao()`).

## 3. Estilização Visual no Frontend

- [x] 2.3 Importar o ícone `CheckCircleIcon` de `@heroicons/vue/24/outline` no arquivo `frontend/src/views/Alertas.vue`.
- [x] 2.4 Estender a definição do tipo `AlertType` em `frontend/src/views/Alertas.vue` para incluir `'admissao_concluida'`.
- [x] 2.5 Atualizar o mapeamento do objeto `alertConfig` em `frontend/src/views/Alertas.vue` definindo a cor verde/esmeralda para o background, bordas e ícone `CheckCircleIcon` para os alertas de tipo `admissao_concluida`.
- [x] 2.6 Atualizar a função `formatTipo` em `frontend/src/views/Alertas.vue` para retornar `'Admissão'` quando o tipo do alerta for `admissao_concluida`.
- [x] 2.7 Exibir a especialidade do paciente como uma badge antes da data de criação no cabeçalho das solicitações de alta na tela `Altas.vue`.

## 4. Verificação e Deploy em Homologação

- [x] 3.1 Verificar localmente o funcionamento simulando um evento de histórico de `conclusao` no banco SQLite local.
- [x] 3.2 Realizar o deploy do código para o servidor de homologação utilizando o script correspondente na pasta scratch.
