import sys
import json

sys.path.append(r"c:\Users\daniel.turmina\Documents\HC-uti-manager\scratch")
from query_vm_data import run_container_python_query

def main():
    print("--- SOLICITACOES DE LEITO ---")
    res = run_container_python_query(
        "SELECT id, prontuario, perfil_solicitante, tipo, especialidade, status FROM solicitacoes_leito WHERE id IN (18, 24)"
    )
    try:
        data = json.loads(res)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print("Raw response:", res)

if __name__ == '__main__':
    main()
