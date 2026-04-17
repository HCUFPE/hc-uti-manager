SELECT prontuario, nome, dt_nascimento, sexo, cor, nome_mae, nome_pai
FROM agh.aip_pacientes
WHERE prontuario = :prontuario;
