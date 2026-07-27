import sqlite3

def main():
    conn = sqlite3.connect('/app/data/app.db')
    cursor = conn.cursor()
    
    # 1. Atualizar o histórico ID 367
    cursor.execute("UPDATE historico_acoes SET acao = 'Definiu destino de alta' WHERE id = 367;")
    print("Histórico ID 367 atualizado para 'Definiu destino de alta'.")
    
    # 2. Deletar os alertas duplicados ID 196 e 260
    cursor.execute("DELETE FROM alertas WHERE id IN (196, 260);")
    print("Alertas duplicados ID 196 e 260 deletados.")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
