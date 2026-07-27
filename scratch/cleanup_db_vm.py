import sqlite3

def main():
    conn = sqlite3.connect('/app/data/app.db')
    cursor = conn.cursor()
    
    # 1. Atualizar o histórico ID 367 e 392
    cursor.execute("UPDATE historico_acoes SET acao = 'Definiu destino de alta' WHERE id IN (367, 392);")
    print("Históricos ID 367 e 392 atualizados para 'Definiu destino de alta'.")
    
    # 2. Deletar os alertas duplicados ID 196, 260 e 259
    cursor.execute("DELETE FROM alertas WHERE id IN (196, 260, 259);")
    print("Alertas duplicados ID 196, 260 e 259 deletados.")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
