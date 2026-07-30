import os
import paramiko
from dotenv import load_dotenv

def main():
    load_dotenv(r"c:\Users\daniel.turmina\Documents\HC-uti-manager\.env")
    host = os.getenv("VM_HOST")
    user = os.getenv("VM_USER")
    secret = os.getenv("VM_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=secret, timeout=15)
        
        # Executar SQL direto no SQLite da aplicação
        sql_commands = """
        -- 1. Deletar alertas de troca antigos
        delete from alertas where titulo = 'Reserva Remanejada (Troca de Paciente)' and prontuario in ('21036074', '22307987', '22064729', '21931076', '13938907');
        
        -- 2. Inserir alertas padronizados como lidos
        insert into alertas (tipo, categoria, titulo, mensagem, prontuario, perfil_alvo, lido, lido_por, lido_em, criado_em) 
        values ('aviso', 'Gargalo', 'Reserva Remanejada (Troca de Paciente)', 
                'Solicitação #92 (HELOISA SIQUEIRA FERNANDES - Prontuário 22307987) foi cancelada. Motivo: Foi substituído por GISELE MARIA DA SILVA (Prontuário 13938907) via troca de paciente.', 
                '13938907', NULL, 1, 'daniel.turmina', '2026-07-29 16:58:00.000000', '2026-07-29 07:59:00.000000');
                
        insert into alertas (tipo, categoria, titulo, mensagem, prontuario, perfil_alvo, lido, lido_por, lido_em, criado_em) 
        values ('aviso', 'Gargalo', 'Reserva Remanejada (Troca de Paciente)', 
                'Solicitação #60 (DAMIAO ALVES PEREIRA - Prontuário 22064729) foi cancelada. Motivo: Foi substituído por JOSE CARLOS DE LUCENA (Prontuário 21931076) via troca de paciente.', 
                '21931076', NULL, 1, 'daniel.turmina', '2026-07-29 16:58:00.000000', '2026-07-29 14:27:00.000000');
                
        -- 3. Ajustar prontuário, data e texto do log de cancelamento da Heloísa (evento 545)
        update historico_acoes 
        set prontuario = '22307987', 
            detalhes = 'Solicitação #92 (HELOISA SIQUEIRA FERNANDES - Prontuário 22307987) foi cancelada. Motivo: Foi substituído por GISELE MARIA DA SILVA (Prontuário 13938907) via troca de paciente.', 
            criado_em = '2026-07-29 10:59:04.951300' 
        where id = 545;
        
        -- 4. Ajustar data e texto do log de cancelamento do Damião (evento 544)
        update historico_acoes 
        set detalhes = 'Solicitação #60 (DAMIAO ALVES PEREIRA - Prontuário 22064729) foi cancelada. Motivo: Foi substituído por JOSE CARLOS DE LUCENA (Prontuário 21931076) via troca de paciente.', 
            criado_em = '2026-07-29 17:27:18.905922' 
        where id = 544;
        """
        
        # Enviar comandos de execução e depois imprimir status e histórico dos pacientes
        cmd = f"export XDG_RUNTIME_DIR=/run/user/$(id -u) && podman exec hc-uti-backend python -c \"import sqlite3; conn = sqlite3.connect('/app/data/app.db'); cursor = conn.cursor(); cursor.executescript(\\\"\\\"\\\"{sql_commands}\\\"\\\"\\\"); conn.commit(); print('=== ALERTA ATIVO/LIDO ==='); [print(row) for row in conn.execute('select id, titulo, mensagem, lido, lido_por, prontuario from alertas where titulo=\\'Reserva Remanejada (Troca de Paciente)\\'').fetchall()]; print('=== HISTÓRICO 21036074 ==='); [print(row) for row in conn.execute('select id, criado_em, tipo, acao, detalhes, prontuario from historico_acoes where prontuario=\\'21036074\\' order by criado_em desc').fetchall()]; print('=== HISTÓRICO 22307987 ==='); [print(row) for row in conn.execute('select id, criado_em, tipo, acao, detalhes, prontuario from historico_acoes where prontuario=\\'22307987\\' order by criado_em desc').fetchall()]; conn.close()\""
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode('utf-8', errors='ignore'))
            
    except Exception as e:
        print("Error:", e)
    finally:
        ssh.close()

if __name__ == '__main__':
    main()
