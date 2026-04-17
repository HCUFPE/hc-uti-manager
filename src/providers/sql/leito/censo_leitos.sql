-- src/providers/sql/leito/censo_leitos.sql
-- Busca o censo de leitos em tempo real diretamente do AGHU
-- src/providers/sql/leito/censo_leitos.sql
-- Busca o censo de leitos em tempo real diretamente do AGHU com lógica avançada de extrato e internação
WITH LatestLeito AS (
    SELECT
        lto_lto_id,
        MAX(criado_em) AS max_criado_em
    FROM
        agh.ain_extrato_leitos
    GROUP BY
        lto_lto_id
),
cte_status AS (
    SELECT
        e.lto_lto_id AS numero_leito,
        e.criado_em,
        e.tml_codigo,
        mv.descricao AS status_desc,
        CASE 
            WHEN mv.descricao ILIKE '%DESOCUPADO%' THEN 'DISPONIVEL'
            WHEN mv.descricao ILIKE '%OCUPADO%' THEN 'OCUPADO'
            WHEN mv.descricao ILIKE '%LIMPEZA%' THEN 'LIMPEZA'
            WHEN mv.descricao ILIKE '%INTERDITADO%' THEN 'INTERDITADO'
            WHEN mv.descricao ILIKE '%RESERVADO%' THEN 'OCUPADO'
            ELSE 'DISPONIVEL'
        END as status_simplificado
    FROM
        agh.ain_extrato_leitos e
    JOIN LatestLeito l ON e.lto_lto_id = l.lto_lto_id AND e.criado_em = l.max_criado_em
    JOIN agh.ain_leitos le ON e.lto_lto_id = le.lto_id
    JOIN agh.ain_tipos_mvto_leito mv ON e.tml_codigo = mv.codigo
    WHERE
        le.ind_situacao = 'A'
        AND le.unf_seq = 115 -- Filtro específico para a UTI em questão
),
cte_paciente AS (
    SELECT 
        i.seq as int_seq,
        i.lto_lto_id as numero_leito,
        p.prontuario as prontuario_atual,
        p.nome as nome_paciente,
        p.dt_nascimento as data_nascimento,
        e.nome_especialidade as clinica,
        i.dthr_internacao,
        obs.descricao as observacao,
        CASE 
            WHEN le.ind_acompanhamento_ccih is null then 'S' 
            ELSE le.ind_acompanhamento_ccih 
        END as ccih,
        (CURRENT_DATE - i.dthr_internacao::date) as tempo_ocupacao,
        ROW_NUMBER() OVER (PARTITION BY i.lto_lto_id ORDER BY i.dthr_internacao DESC) as rn
    FROM 
        agh.ain_internacoes i
    LEFT JOIN agh.aip_pacientes p ON i.pac_codigo = p.codigo
    LEFT JOIN agh.agh_especialidades e ON i.esp_seq = e.seq
    LEFT JOIN agh.ain_leitos le ON i.lto_lto_id = le.lto_id
    LEFT JOIN agh.ain_observacoes_censo obs ON obs.int_seq = i.seq
    WHERE 
        i.ind_saida_pac = 'N'
        AND i.lto_lto_id IS NOT NULL
)
SELECT
    st.numero_leito as lto_lto_id,
    st.status_simplificado as status,
    st.status_desc as status_detalhado,
    'UTI' as tipo,
    pa.prontuario_atual,
    pa.nome_paciente,
    pa.data_nascimento,
    pa.clinica as especialidade_atual,
    pa.dthr_internacao as atualizado_em,
    pa.tempo_ocupacao,
    pa.ccih,
    pa.observacao
FROM
    cte_status st
LEFT JOIN
    cte_paciente pa ON st.numero_leito = pa.numero_leito AND pa.rn = 1
ORDER BY
    st.numero_leito;
