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
                    
    # Além disso, se houver um alerta com título "Alterou o Destino de Alta" e outro com "Destino de Alta Definido"
    # para o mesmo prontuário e data, nós deletamos o de "Alterou..." (pois o histórico foi corrigido para "Definiu...")
    alt_alerts = [r for r in rows if r[3] == "Alterou o Destino de Alta"]
    def_alerts = [r for r in rows if r[3] == "Destino de Alta Definido"]
    
    for alt in alt_alerts:
        alt_id, _, _, _, _, alt_date, alt_pront = alt
        alt_date_sec = str(alt_date)[:19]
        
        # Procura se há um "Definiu" correspondente
        for defe in def_alerts:
            def_id, _, _, _, _, def_date, def_pront = defe
            def_date_sec = str(def_date)[:19]
            
            if alt_pront == def_pront and alt_date_sec == def_date_sec:
                to_delete.append(alt_id)
                print(f"Marcado para deletar alerta de alteração sobressalente: ID {alt_id} (Data: {alt_date})")
        
    # Remover duplicatas da lista de exclusão
    to_delete = list(set(to_delete))
    
    print("IDs de alertas duplicados identificados para deleção:", to_delete)
    
    for d_id in to_delete:
        cursor.execute("DELETE FROM alertas WHERE id = ?;", (d_id,))
        print(f"Alerta ID {d_id} deletado.")
        
    # 3. Atualizar mensagens antigas que não contêm o prontuário
    titulos_alvo = ["Destino de Alta Definido", "Alterou o Destino de Alta", "Leito de Destino LIBERADO", "Liberação de Destino CANCELADA"]
    for r in rows:
        id_val, tipo, cat, tit, msg, date, pront = r
        if id_val not in to_delete: # Se não foi deletado
            if tit in titulos_alvo and pront and pront != "Desconhecido" and "(Prontuário" not in msg:
                nova_msg = f"{msg} (Prontuário {pront})"
                cursor.execute("UPDATE alertas SET mensagem = ? WHERE id = ?;", (nova_msg, id_val))
                print(f"Alerta ID {id_val} atualizado para incluir prontuário: '{nova_msg}'")
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
