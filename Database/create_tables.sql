IF OBJECT_ID('departamentos', 'U') IS NULL
BEGIN
    CREATE TABLE departamentos
    (
        id_departamento INT IDENTITY PRIMARY KEY,
        nome VARCHAR(50) NOT NULL
    );
END
GO

IF OBJECT_ID('funcionarios', 'U') IS NULL
BEGIN
    CREATE TABLE funcionarios
    (
        matricula INT IDENTITY PRIMARY KEY,
        nome VARCHAR(20) NOT NULL,
        sobrenome VARCHAR(50) NOT NULL,
        cargo VARCHAR(30),
        salario DECIMAL(10, 2),
        data_admissao DATE,
        id_departamento INT,
        CONSTRAINT fk_funcionario_departamento FOREIGN KEY (id_departamento) REFERENCES departamentos (id_departamento)
    );
END
GO