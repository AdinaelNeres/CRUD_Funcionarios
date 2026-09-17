from pathlib import Path
import json
import funcoes as f
from conexao import conectar_master, conectar_empresa, fechar_banco

pasta_database = Path("Database")
arquivo = Path(__file__).parent/"config.json"
with open(arquivo, encoding="utf-8") as a:
    config = json.load(a)

# Conectando ao SQL Derver perfil master, para criar o database Empresa.
conexao, cursor = conectar_master()
f.gerar_database(cursor, pasta_database/"create_database.sql")
fechar_banco(conexao, cursor)

# Conectando ao banco Empresa para criar as tabelas, procedures, trigges e inserção de dados.
conexao, cursor = conectar_empresa(config)
f.gerar_database(cursor, pasta_database/"create_tables.sql")
f.cadastrar_departamentos(conexao, cursor)
print("Banco Empresa configurado com sucesso!")

# Funcionalidades do sistema.
while True:
    opcao = f.menu()
    match opcao:
        case 1:
            f.inserir_funcionario(conexao, cursor)
            print("Novo funcionáfrio incluido.")
            
        case 2:
            f.consultar_funcionarios(cursor)
                
        case 3:
            f.atualizar_cadastro(conexao, cursor)
            
        case 4:
            f.excluir_funcionario(conexao, cursor)
        
    opcao = f.menu_voltar_sair()
    if opcao == 2:
        break
        

fechar_banco(conexao, cursor)