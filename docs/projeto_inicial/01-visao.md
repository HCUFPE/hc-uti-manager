# Documento de Visão — HC-UTI Manager

Este documento define a visão, o escopo e as diretrizes principais do projeto **HC-UTI Manager**, servindo como fonte de verdade para o propósito do produto e as necessidades que ele atende.

---

## 1. Introdução e Objetivo do Produto
O **HC-UTI Manager** é uma solução de software desenvolvida para o Hospital das Clínicas da UFPE (HC-UFPE/Ebserh) com o objetivo de centralizar, otimizar e monitorar em tempo real o censo de leitos, o fluxo de internações, as reservas e as solicitações de vagas para a Unidade de Terapia Intensiva (UTI). 

O sistema integra-se de forma inteligente ao sistema de gestão hospitalar oficial (AGHU) e serve como ponte operacional rápida entre três grandes setores: a **UTI**, o **Bloco Cirúrgico (BC)** e o **Núcleo Interno de Regulação (NIR)**.

---

## 2. Declaração do Problema

| Elemento | Descrição |
| --- | --- |
| **O problema de** | Falta de visibilidade em tempo real do status físico dos leitos da UTI, gerando a necessidade de alinhamento manual por canais de comunicação informais e descentralizados para saber se haverá vagas, ausência de previsão consolidada de cirurgias eletivas para a UTI, e dificuldades operacionais para reservar leitos com antecedência e gerar indicadores de acompanhamento confiáveis. |
| **Afeta** | A equipe médica e administrativa da UTI, os cirurgiões e gestores do Bloco Cirúrgico, os reguladores do NIR e, principalmente, os pacientes que aguardam vaga em estado grave ou pós-operatório. |
| **O impacto disso é** | Ociosidade de leitos críticos (longa espera), cancelamento ou suspensão desnecessária de cirurgias eletivas por suposta falta de vagas, falhas de comunicação devido ao uso de ferramentas externas e descentralizadas, e dificuldade na extração de métricas históricas de controle e auditoria. |
| **Uma solução de sucesso seria** | Um painel visual e dinâmico (Bed Card Board) atualizado em tempo real, que integre a previsão de cirurgias do AGHU para a UTI, permita a reserva ágil de leitos com alertas inteligentes automáticos e forneça um dashboard de indicadores para análise de performance. |

---

## 3. Perfis e Atores do Sistema

O sistema atende a perfis específicos, cada um com permissões operacionais distintas:

*   **Equipe da UTI (Médicos e Enfermagem):**
    *   *Objetivo:* Controlar o estado do leito físico (ocupado, higienização, desativado).
    *   *Ação no sistema:* Solicitar alta de pacientes internados, definir a necessidade de higienização ou interdição de leitos.
*   **Bloco Cirúrgico (BC / Solicitantes):**
    *   *Objetivo:* Garantir leito de UTI pós-operatório para as cirurgias eletivas agendadas.
    *   *Ação no sistema:* Cadastrar solicitações de leitos de UTI, gerenciar prioridades de fila (P1 a P4) e reservar leitos vagos específicos para pacientes cirúrgicos.
*   **NIR (Núcleo Interno de Regulação):**
    *   *Objetivo:* Regular a entrada e saída de todos os pacientes do hospital.
    *   *Ação no sistema:* Visualizar solicitações de alta da UTI e definir a enfermaria/leito de destino para onde o paciente será transferido, liberando fisicamente o leito da UTI.
*   **Administrador / Gestão:**
    *   *Objetivo:* Monitorar as métricas de qualidade e gerenciar parametrizações.
    *   *Ação no sistema:* Visualizar indicadores consolidados (KPIs de cancelamentos, tempos de giro de leito) e gerenciar acessos.

---

## 4. Recursos e Funcionalidades Principais

*   **Censo Diário e Painel de Leitos (Bed Cards):** Visualização em tempo real de cada leito da UTI (identificando o paciente ocupante, tempo de internação, previsão de alta e próximas reservas).
*   **Painel de Solicitações e Fila Inteligente:** Fila dinâmica de pacientes cirúrgicos aguardando vaga, ordenada por prioridade clínica (P1 a P4) e integrada aos agendamentos do AGHU.
*   **Mesclagem Inteligente (Troca de Paciente):** Regra de negócio que permite substituir um paciente da fila por outro de forma ágil, cancelando a solicitação antiga, reaproveitando a vaga para o novo paciente e atualizando o censo sem gerar duplicidades.
*   **Módulo de Altas e Destinos (NIR):** Tela de controle para o NIR definir o destino de pacientes que receberam alta clínica da UTI, agilizando o giro do leito.
*   **Motor de Alertas em Tempo Real:** Alertas visuais e sonoros disparados para avisar sobre novas solicitações críticas de hoje, cancelamentos feitos pelo Bloco Cirúrgico, ou altas pendentes.
*   **Indicadores de Performance (KPIs):** Dashboard com contagem de admissões, taxas de ocupação e segmentação exata de cancelamentos de reserva (separando os provocados pela UTI dos provocados por remanejamento do Bloco Cirúrgico).