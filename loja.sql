create database if not exists loja;

use loja;

create table cliente(
    id_cliente int auto_increment primary key,
    nome_cliente varchar(100) not null,
    sobrenome_cliente varchar(50) not null,
    email_cliente varchar(50) null,
    telefone_celular_cliente varchar(11) null,
    endereco_cliente text not null,
    idade_cliente int null,
    cpf_cliente varchar(11) unique not null
);

create table produtos(
    id_produto int auto_increment primary key,
    nome_produto text not null,
    cod_barras_produto int not null,
    fabricante_produto varchar(50) not null,
    data_fabircacao_produto date not null,
    data_validade_produto date null,
    categoria_produto varchar(30) not null,
    peso_produto int not null,
    preco_produto int not null
);