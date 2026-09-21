IF OBJECT_ID('sp_inserir_funcionario', 'P') IS NULL
BEGIN
    EXEC('
        CREATE PROCEDURE sp_inserir_funcionario @nome VARCHAR(20),
                                                @SOBRENOME VARCHAR(30),
                                                @cargo VARCHAR(20),
                                                @salario DECIMAL(10, 2),
                                                @id_departamento INT
        AS
        BEGIN
            INSERT INTO funcionarios
            (nome, sobrenome, cargo, salario, data_admissao, id_departamento)
            VALUES
            (@nome, @sobrenome, @cargo, @salario, GETDATE(), @id_departamento);
        END
        ')
END
GO

IF OBJECT_ID('sp_excluir_funcionario', 'P') IS NULL
BEGIN
    EXEC('
        CREATE PROCEDURE sp_excluir_funcionario @matricula INT
    AS
    BEGIN
        DELETE FROM funcionarios
        WHERE matricula = @matricula;
    END
    ')
END

