import sqlite3

def main():
    conn = sqlite3.connect('/app/data/app.db')
    cursor = conn.cursor()
    
    # 0. Atualizar o histórico ID 367 e 392
    cursor.execute("UPDATE historico_acoes SET acao = 'Definiu destino de alta' WHERE id IN (367, 392);")
    print("Históricos ID 367 e 392 atualizados para 'Definiu destino de alta'.")
    
    # 1. Obter todos os alertas
    cursor.execute("SELECT id, tipo, categoria, titulo, mensagem, criado_em, prontuario FROM alertas;")
    rows = cursor.fetchall()
    
    to_delete = []
    
    # Vamos agrupar os alertas por (prontuario, criado_em, titulo)
    # E identificar se há um com "(Prontuário" e outro sem.
    groups = {}
    for r in rows:
        id_val, tipo, cat, tit, msg, date, pront = r
        # Usamos uma chave aproximada (prontuario, criado_em, titulo)
        # Nota: criado_em pode ser string com milissegundos, agrupamos por segundos
        date_sec = str(date)[:19] # YYYY-MM-DD HH:MM:SS
        key = (pront, date_sec, tit)
        groups.setdefault(key, []).append(r)
        
    for key, items in groups.items():
        if len(items) > 1:
            # Tem duplicados. Vamos ver se um tem "(Prontuário" e o outro não
            has_pront = [it for it in items if "(Prontuário" in it[4]]
            no_pront = [it for it in items if "(Prontuário" not in it[4]]
            
            if has_pront and no_pront:
                # Deletamos os que não tem o prontuário na mensagem
                for it in no_pront:
                    to_delete.append(it[0])
            else:
                # Se forem idênticos, deletamos o de maior ID (ou menor) mantendo apenas um
                sorted_items = sorted(items, key=lambda x: x[0])
                for it in sorted_items[1:]:
                    to_delete.append(it[0])
                    
    # Além disso, o ID 272 é um "Alterou o Destino de Alta" que virou "Definiu" no histórico, então deve ser deletado
    # ID 272: (272, 'info', 'Gargalo', 'Alterou o Destino de Alta', 'Leito 0502F: Destino 807A (Prontuário 22341010)', '2026-07-27 10:44:33.257460')
    if 272 not in to_delete:
        to_delete.append(272)
        
    # Remover duplicatas da lista de exclusão
    to_delete = list(set(to_delete))
    
    print("IDs de alertas duplicados identificados para deleção:", to_delete)
    
    for d_id in to_delete:
        cursor.execute("DELETE FROM alertas WHERE id = ?;", (d_id,))
        print(f"Alerta ID {d_id} deletado.")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
