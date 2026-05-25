SELECT
  -- 1. Dados do Paciente
  pac.prontuario AS "Prontuário",
  pac.nome AS "Nome Completo",
  TO_CHAR(pac.dt_nascimento, 'DD-MM-YYYY') AS "Data de Nascimento", -- Formatado: dd-mm-aaaa
  
  -- 2. Dados da Cirurgia e Tempo
  TO_CHAR(cir.dthr_inicio_cirg, 'DD-MM-YYYY') AS "Data da Cirurgia", -- Formatado: dd-mm-aaaa
  TO_CHAR(cir.dthr_inicio_cirg, 'HH24:MI') AS "Hora de Início",
  
  -- 3. Especialidade
  esp.nome_especialidade AS "Especialidade",
  
  -- 4. Procedimento Principal
  psu.phi_descricao AS "Procedimento Principal"

FROM agh.mbc_cirurgias cir
  INNER JOIN agh.aip_pacientes pac ON cir.pac_codigo = pac.codigo
  LEFT JOIN agh.agh_especialidades esp ON cir.esp_seq = esp.seq
  
  -- Rota da Agenda (Garantindo o Procedimento Principal)
  INNER JOIN agh.mbc_agendas agd ON cir.agd_seq = agd.seq
  LEFT JOIN agh.mbc_procedimento_cirurgicos pci ON pci.seq = agd.epr_pci_seq
  LEFT JOIN agh.fat_proced_hosp_internos phi ON phi.pci_seq = pci.seq
  LEFT JOIN public.vw_fat_associacao_procedimentos psu ON phi.seq = psu.phi_seq AND psu.cpg_cph_csp_seq = 1

WHERE 
  pac.prontuario = :prontuario
  AND cir.situacao <> 'CANC'

ORDER BY cir.dthr_inicio_cirg DESC
LIMIT 1;
