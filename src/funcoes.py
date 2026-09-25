from pathlib import Path
import textwrap
from datetime import datetime
import pyodbc
import pandas as pd

def gerar_database(cursor, caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        sql = arquivo.read()
    
    comandos = sql.split("GO")
    
    for comando in comandos:
        comando.strip()
        
        if comando:
            cursor.execute(comando)
    
    cursor.connection.commit()

def cadastrar_departamentos(conexao, cursor):
    
    cursor.execute("""
                   SELECT id_departamento, nome 
                   FROM departamentos
                   """)
    
    linhas = cursor.fetchall()
    if not linhas:
        cursor.execute(f"""
                INSERT INTO departamentos (nome) VALUES
                ('Recursos humanos'),
                ('Vendas'),
                ('TI'),
                ('Markting'),
                ('Financeiro'),
                ('Serviços gerais');
                """)
        
        conexao.commit()

def menu():
    while True:
        try:
            opcao = int(input(textwrap.dedent("""
                                            Selecione a opção desejada:
                                            
                                            1 - Cadastrar funcionário
                                            2 - Listar todos os funcionários
                                            3 - Atualizar cadastro
                                            4 - Excluor funcionário
                                            5 - Consultar por nome
                                            6 - Exportar para excel
                                            7 - Sair 
                                            """)))
        except ValueError:
            print("Digiyte apenas números")
            continue
        
        if opcao < 1 or opcao > 7:
            print("Informe uma opção valida")
            continue
        
        else:
            break
        
    return opcao

def inserir_funcionario(conexao, cursor):
    nome = input("Nome:\n")
    sobrenome = input('Sobrenome:\n')
    cargo = input("Cargo:\n")
    while True:
        try:
            salario = float(input("Salário:\n"))
            break
        except ValueError:
            print("Informe apenas números")
    
    print("Estes são os departamentos disponíveis atualmente:\n\n")
    indices = []
    cursor.execute("""
                   SELECT id_departamento, nome
                   FROM departamentos;
                   """)
    linhas = cursor.fetchall()
    for linha in linhas:
        indices.append(linha[0])
        print(f"{linha[0]} - {linha[1]}")
    
    while True:
        while True:
            try:
                indice = int(input("Informe o indice do departamento desejado\n"))
                break
            except ValueError:
                print("Informe apenas números")
                
        if indice in indices:
            break
        print('Departamento não encontrado.')
    
    cursor.execute("""
                   EXECUTE sp_inserir_funcionario ?, ?, ?, ?, ?;
                   """, nome, sobrenome, cargo, salario, indice)
    
    conexao.commit()

def converter_para_DataFrame(cursor):
    
    cursor.execute("""
                   SELECT f.matricula as Matrícula,
                          f.nome as Nome,
                          f.sobrenome as Sobrenome,
                          f.cargo as Cargo,
                          d.nome as Departamento,
                          salario as Salário,
                          data_admissao as Data_de_admissão
                    FROM funcionarios f
                    INNER JOIN departamentos d
                    ON f.id_departamento = d.id_departamento;
                   """)
    
    linhas = cursor.fetchall()
    if not linhas:
        print('Não há funcionários cadastrados')
        return

    tabela_funcionarios = pd.DataFrame.from_records(
        linhas,
        columns=[coluna[0] for coluna in cursor.description]
    )

    return tabela_funcionarios


def atualizar_cadastro(conexao, cursor):
    while True:
        matricula = verificar_matricula(cursor)            
        cursor.execute("""
                       SELECT COLUMN_NAME 
                       FROM INFORMATION_SCHEMA.COLUMNS
                       WHERE TABLE_NAME = 'funcionarios'
                       AND COLUMN_NAME <> 'matricula';
                       """)
        
        colunas = [coluna[0] for coluna in cursor.fetchall()]
        print("\n")
        for coluna in colunas:
            print(coluna.capitalize())
        
        while True:
            campo = input("\nInforme o campo para atualização:\n")
            if campo in colunas:
                break
            
            print("Campo não encontrado")
        if campo == 'salario':
            nova_info = float(input("Nova informação: "))
        elif campo == 'id_departamento':
            nova_info = int(input("Nova informação: "))
        elif campo == 'data_admissao':
            while True:
                try:
                    nova_info = (input("Informe a nova data (Ex: AAAA/MM/DD): "))
                    nova_info = datetime.strptime(nova_info, '%Y/%m/%d').date()
                    break
                except ValueError:
                    print("Valor inválido")
        else:
            nova_info = input("Nova informação: ")
        
        try:
            cursor.execute(f"""
                           UPDATE funcionarios
                           SET {campo} = ?
                           WHERE matricula = ?;
                           """, nova_info, matricula)
            conexao.commit()
            
        except Exception as erro:
            print("Erro ao atualizar: ", erro)
            conexao.rollback()
            continue
            
        sql = """
        SELECT nome,
               sobrenome,
               cargo,
               salario,
               data_admissao,
               id_departamento
        FROM funcionarios
        WHERE matricula = ?;
        """
        cursor.execute(sql, matricula)
        linhas = cursor.fetchall()
        for linha in linhas:
            print(textwrap.dedent(f"""
                                  Dados atualizados:
                                  
                                  Nome:             {linha[0]} {linha[1]}
                                  Cargo:            {linha[2]}
                                  Salário:          {linha[3]}
                                  Data de admissão: {linha[4]}
                                  ID Departamento:  {linha[5]}
                                  ========================================
                                  """))
        break
        
def excluir_funcionario(conexao, cursor):
    
    while True:
        matricula = verificar_matricula(cursor)
        try:
            cursor.execute("""
                           SELECT nome, sobrenome
                           FROM funcionarios
                           WHERE matricula = ?;
                           """, matricula)
            
            nome = []
            nome = cursor.fetchone()
            opcao = input(textwrap.dedent(f"Tem certeza que deseja excluor {nome[0]} {nome[1]} (s/n): "))

            if opcao != 's':
                print("Exclusão cancelada!")
                break
            
            cursor.execute("""
                        EXECUTE sp_excluir_funcionario ?;
                        """, matricula)
            conexao.commit()
            print("Funcionário excluido com sucesso!")
            break
        
        except pyodbc.Error:
            print("Erro ao execultar: ")
            conexao.rollback()
            continue
        
def menu_voltar_sair():
    while True:
        try:
            opcao = int(input(textwrap.dedent("""
                                              1 - Voltar ao início
                                              2 - Sair
                                              """)))
        except ValueError:
            print("Digite 1 ou 2")
            continue
                
        if opcao == 1 or opcao == 2:
            return opcao
        else:
            print("Opção invalida")

def verificar_matricula(cursor):
    while True:
        try:
            matricula = int(input("Informe a matricula do funcionário:  "))
                        
        except ValueError:
            print("Digite apenas números!")
            continue
                    
        cursor.execute("""
                        SELECT matricula
                        FROM funcionarios
                        WHERE matricula = ?
                        """, matricula)
                    
        resultado = cursor.fetchone()
        if not resultado:
            print("funcionário não encontrado")
            continue
                
        return matricula

def consulta_por_nome(cursor):
    while True:
        primeiro_nome = input("Informe o nome do funcionário: ")
        ultimo_nome = input("Informe o sobrenome do funcicário: ")
        
        cursor.execute("""
                                    SELECT f.matricula,
                                           f.nome,
                                           f.sobrenome,
                                           f.cargo,
                                           d.nome,
                                           f.salario,
                                           f.data_admissao
                                    FROM funcionarios f
                                    INNER JOIN departamentos d
                                    ON f.id_departamento = d.id_departamento
                                    WHERE f.nome = ? AND f.sobrenome = ?;
                                     """, primeiro_nome, ultimo_nome)
        
        linhas = cursor.fetchall()
        mensagem = f"{primeiro_nome} {ultimo_nome} não consta em nossa base"
        mostrar_funcionario(linhas, mensagem)
        if mostrar_funcionario(linhas, mensagem):
            break
    
def mostrar_funcionario(linhas, mensagem):
    if not linhas:
        print(mensagem)
        return True
    
    for linha in linhas:
        print(textwrap.dedent(f"""
                                Matricula:        {linha[0]}
                                Nome:             {linha[1]} {linha[2]}
                                Cargo:            {linha[3]}
                                Departamento:     {linha[4]}
                                Salário           R$ {linha[5]:.2f}
                                Data de admissão: {linha[6]}
                                ========================================
                                """))
            