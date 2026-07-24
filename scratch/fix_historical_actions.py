import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Configura sys.path para conseguir importar os modelos da pasta src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from models.historico_acao import HistoricoAcao

def main():
    load_dotenv()
    dsn = os.getenv("SQLITE_DSN", "sqlite+aiosqlite:///./data/app.db")
    # Para o script síncrono, removemos a biblioteca aiosqlite
    sync_dsn = dsn.replace("+aiosqlite", "")
    
    print(f"Conectando ao banco de dados: {sync_dsn}")
    engine = create_engine(sync_dsn)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Busca todas as ações de histórico de tipo 'alteracao_destino'
        historicos = session.query(HistoricoAcao).filter(HistoricoAcao.tipo == 'alteracao_destino').order_by(HistoricoAcao.criado_em.asc()).all()
        print(f"Total de registros de alteracao_destino encontrados: {len(historicos)}")
        
        # Agrupa por prontuário
        by_prontuario = {}
        for h in historicos:
            if not h.prontuario:
                continue
            by_prontuario.setdefault(h.prontuario, []).append(h)
            
        corrigidos = 0
        for prontuario, logs in by_prontuario.items():
            # logs já estão ordenados de forma crescente por data de criação
            # O primeiro log (índice 0) é a definição inicial ("Definiu destino de alta")
            # Do segundo log (índice 1) em diante, todos devem ser atualizados para "Alterou destino de alta"
            if len(logs) > 1:
                for h_edit in logs[1:]:
                    if h_edit.acao != "Alterou destino de alta":
                        h_edit.acao = "Alterou destino de alta"
                        corrigidos += 1
                        
        if corrigidos > 0:
            session.commit()
            print(f"Sucesso! {corrigidos} registros de histórico foram atualizados de 'Definiu...' para 'Alterou destino de alta'.")
        else:
            print("Nenhum registro antigo precisou de correção.")
            
    except Exception as e:
        session.rollback()
        print(f"Erro durante a execução da correção: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    main()
