import pyodbc
import json
from pathlib import Path

def conectar_master():
    conexao = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=DESKTOP-BMTCK6O;"
        "Database=master;"
        "trusted_connection=yes;",
        autocommit=True
    )
    
    return conexao, conexao.cursor()

def conectar_empresa():
    
    arquivo = Path(__file__).parent/"config.json"
    with open(arquivo, encoding="utf-8") as a:
        config = json.load(a)
    
    conexao = pyodbc.connect(
        f"Driver={{{config['driver']}}};"
        f"Server={config['server']};"
        f"Database={config['database']};"
        f"Trusted_connection={config['trusted_connection']};",
    )
    
    return conexao, conexao.cursor()

def fechar_banco(conexao=None, cursor=None):
    try:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
        
    except Exception as erro:
        print(f"O comando falhou devido ao erro {erro}")