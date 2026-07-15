-- src/providers/sql/leito/tempo_higienizacao.sql
-- Calcula o tempo de higienização histórico de leitos da UTI no AGHU
WITH ExtratosOrdenados AS (
    SELECT
        e.lto_lto_id,
        e.criado_em AS data_status,
        mv.descricao AS status_nome,
        -- Busca o timestamp do próximo status/movimentação do mesmo leito
        LEAD(e.criado_em) OVER (PARTITION BY e.lto_lto_id ORDER BY e.criado_em ASC) AS data_proximo_status
    FROM
        agh.ain_extrato_leitos e
    JOIN 
        agh.ain_tipos_mvto_leito mv ON e.tml_codigo = mv.codigo
    JOIN
        agh.ain_leitos le ON e.lto_lto_id = le.lto_id
    WHERE
        le.ind_situacao = 'A'
        AND le.unf_seq = 115 -- Restringe aos leitos da UTI
)
SELECT
    data_status AS inicio_higienizacao,
    data_proximo_status AS fim_higienizacao
FROM
    ExtratosOrdenados
WHERE
    status_nome ILIKE '%LIMPEZA%' 
    AND data_proximo_status IS NOT NULL;
