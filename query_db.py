import sqlite3
import pandas as pd

# Caminho para o seu banco de dados
DB_PATH = 'financeflow.db'

def query_with_pandas():
    print("--- Consultando com Pandas ---")
    # O Pandas consegue ler o banco de dados diretamente e transformar o resultado
    # num DataFrame (uma tabela muito fácil de manipular)
    
    # Criamos a conexão
    conn = sqlite3.connect(DB_PATH)
    
    # Escrevemos a nossa consulta (Query)
    # Aqui estamos pedindo para juntar (JOIN) as transações com suas categorias
    query = """
        SELECT 
            t.date as 'Data',
            t.description as 'Descrição',
            t.amount as 'Valor',
            c.name as 'Categoria',
            t.type as 'Tipo'
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        ORDER BY t.date DESC
        LIMIT 5;
    """
    
    # O Pandas faz todo o trabalho pesado
    df = pd.read_sql_query(query, conn)
    
    # Mostra os resultados de forma tabular no terminal
    print(df.to_string())
    print("\n")
    
    # Exemplo: Agrupando para saber o total gasto por categoria
    print("--- Total por Categoria (Usando Pandas) ---")
    query_total = """
        SELECT c.name as Categoria, SUM(t.amount) as Total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.type = 'expense'
        GROUP BY c.id;
    """
    df_totals = pd.read_sql_query(query_total, conn)
    print(df_totals.to_string())
    
    conn.close()

if __name__ == '__main__':
    query_with_pandas()
