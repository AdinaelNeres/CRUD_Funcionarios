from pathlib import Path
import funcoes as f
from conexao import conectar_master, conectar_empresa, fechar_banco

pasta_database = Path("Database")

# Conectando ao SQL Derver perfil master, para criar o database Empresa.
conexao, cursor = conectar_master()
f.gerar_database(cursor, pasta_database/"create_database.sql")
fechar_banco(conexao, cursor)

# Conectando ao banco Empresa para criar as tabelas, procedures, trigges e inserção de dados.
conexao, cursor = conectar_empresa()
f.gerar_database(cursor, pasta_database/"create_tables.sql")
f.gerar_database(cursor, pasta_database/"procedures.sql")
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
            
        case 5:
            break
        
    opcao = f.menu_voltar_sair()
    if opcao == 2:
        break
        

fechar_banco(conexao, cursor)