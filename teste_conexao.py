import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from decouple import config

def testar_e_criar_db():
    print("Tentando conectar ao PostgreSQL...")
    db_name = config('DB_NAME', default='gestao_barcos_beira')
    user = config('DB_USER', default='postgres')
    password = config('DB_PASSWORD', default='postgres')
    host = config('DB_HOST', default='localhost')
    port = config('DB_PORT', default='5432')
    
    # 1. Conectar ao banco padrão 'postgres' para verificar/criar o banco do projeto
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar se o banco já existe
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Banco de dados '{db_name}' não existe. Criando...")
            cursor.execute(f"CREATE DATABASE {db_name};")
            print(f"Banco de dados '{db_name}' criado com sucesso!")
        else:
            print(f"Banco de dados '{db_name}' já existe.")
            
        cursor.close()
        conn.close()
        
        # 2. Testar a conexão direta ao novo banco
        conn2 = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Conexão direta ao banco do projeto realizada com sucesso!")
        conn2.close()
        return True
    except Exception as e:
        print(f"Erro ao conectar ou criar base de dados: {e}")
        print("\nVerifique se o serviço PostgreSQL está ativo e se os dados no arquivo .env estão corretos.")
        return False

if __name__ == "__main__":
    testar_e_criar_db()
