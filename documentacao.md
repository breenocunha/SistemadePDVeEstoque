# Sistema de PDV e Estoque - Documentação

## Sumário
1. [Introdução](#introdução)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Módulos](#módulos)
   - [Vendas](#módulo-de-vendas)
   - [Produtos](#módulo-de-produtos)
   - [Clientes](#módulo-de-clientes)
   - [Relatórios](#módulo-de-relatórios)
   - [Fiscal](#módulo-fiscal)
   - [Banco de Dados](#módulo-de-banco-de-dados)
4. [Instalação](#instalação)
5. [Configuração](#configuração)
6. [Uso do Sistema](#uso-do-sistema)
7. [Manutenção](#manutenção)
8. [Solução de Problemas](#solução-de-problemas)
9. [Referências](#referências)

## Introdução

O Sistema de PDV e Estoque é uma aplicação desktop desenvolvida em Python para gerenciamento de vendas, controle de estoque, cadastro de clientes e geração de relatórios. O sistema foi projetado para pequenos e médios negócios que necessitam de uma solução completa e integrada para suas operações comerciais.

### Principais Funcionalidades

- Registro de vendas com interface intuitiva
- Controle de estoque com alertas de produtos com estoque baixo
- Cadastro e gerenciamento de clientes
- Geração de relatórios detalhados
- Módulo fiscal para emissão de documentos fiscais
- Interface moderna e responsiva

## Arquitetura do Sistema

O sistema foi desenvolvido seguindo o padrão de arquitetura MVC (Model-View-Controller), que separa a lógica de negócios da interface do usuário, facilitando a manutenção e expansão do código.

### Estrutura de Diretórios