CREATE DATABASE db;
USE db;

CREATE TABLE pass(
	plataforma VARCHAR(50) NOT NULL UNIQUE,
	senha VARCHAR(100) NOT NULL
);

INSERT INTO pass (plataforma,senha) VALUES('manager','manager');/* alterar a senha padrão */
