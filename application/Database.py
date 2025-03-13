from sqlalchemy import create_engine, text
from datetime import datetime
import mysql.connector
import streamlit as st
import pandas as pd
datetime = datetime.now().strftime('%Y-%m-%d')


class Database:
    @staticmethod
    def conexao_db():
        return mysql.connector.connect(
            host=st.secrets["db_host"],
            port=st.secrets["db_port"],
            user=st.secrets["db_user"],
            password=st.secrets["db_password"],
            database=st.secrets["database"]
        )

    @staticmethod
    def conn_sqlalchemy():
        return create_engine(
            f"mysql+mysqlconnector://{st.secrets['db_user']}:{st.secrets['db_password']}"
            f"@{st.secrets['db_host']}:{st.secrets['db_port']}/{st.secrets['database']}"
        )

    def select_len_carrinho(self):  # Line 28
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT * FROM carrinho'
        cursor.execute(sql)
        return len(cursor.fetchall())

    def insert_novo_pagamento(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'INSERT INTO pagamentos(data_inicio, identificador, status) VALUES (%s, %s, %s);'
        dados = (datetime, self.select_max_identificador()+1, "None")
        cursor.execute(sql, dados)
        conn.commit()

    def insert_primeiro_pagamento(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'INSERT INTO pagamentos(data_inicio, identificador, status) VALUES (%s, %s, %s);'
        dados = (datetime, 10150, "None")
        cursor.execute(sql, dados)
        conn.commit()

    def select_len_pagamentos(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT * FROM pagamentos'
        cursor.execute(sql)
        return len(cursor.fetchall())

    def select_max_identificador(self):  # Line 32
        conn = self.conexao_db()
        cursor = conn.cursor()
        len_pagamentos = self.select_len_pagamentos()
        if len_pagamentos == 0:
            self.insert_primeiro_pagamento()
        else:
            sql = 'SELECT identificador FROM pagamentos WHERE id = (SELECT MAX(id) FROM pagamentos);'
            cursor.execute(sql)
            identificador = cursor.fetchall()[0][0]
            return identificador

    def select_penultimo_identificador(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT identificador FROM pagamentos WHERE id = (SELECT MAX(id)-1 FROM pagamentos);'
        cursor.execute(sql)
        identificador = int(cursor.fetchall()[0][0])
        return identificador

    def select_montar_pagamento(self):  # Line 51
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT id, nome_produto, quantidade, preco FROM carrinho;'
        cursor.execute(sql)
        produtos_carrinho = cursor.fetchall()
        return produtos_carrinho

    def insert_proximo_pagamento(self, result, identificador):  # Line 63
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'INSERT INTO pagamentos (data_inicio, identificador, status) VALUES (%s, %s, %s);'
        dados = (result, identificador, "None")
        cursor.execute(sql, dados)
        conn.commit()

    def truncate_carrinho(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'TRUNCATE TABLE carrinho;'
        cursor.execute(sql)
        conn.commit()

    def select_credenciais(self, username, password):
        conn = self.conexao_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nome_usuario, senha_usuario FROM usuarios "
                       "WHERE nome_usuario = %s AND senha_usuario = %s", (username, password))
        usuario = cursor.fetchone()
        print(usuario)
        conn.commit()
        return usuario

    def select_nivel_acesso(self, username):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT nivel_acesso FROM usuarios WHERE nome_usuario = %s;'
        dados = (username,)
        cursor.execute(sql, dados)
        nivel_acesso = cursor.fetchall()[0][0]
        return nivel_acesso

    def insert_cadastrar_produto(self, marca, nome, cod_barras, preco, data):  # Line 213
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('INSERT INTO produtos(marca_produto, nome_produto, cod_barras, preco, '
               'numero_vendas) VALUES (%s, %s, %s, %s, %s);')
        dados = (marca, nome, cod_barras, preco, 0)
        cursor.execute(sql, dados)
        conn.commit()

        produto_id = self.select_id_produto(cod_barras)

        sql = ('INSERT INTO precos_produtos(produto_id, cod_barras, preco_produto, '
               'data_inicio, data_termino) VALUES (%s, %s, %s, %s, %s);')
        dados = (produto_id, cod_barras, preco, data, data)
        cursor.execute(sql, dados)

        sql = 'INSERT INTO estoque(produto_id, cod_barras, qtd_estoque) VALUES (%s, %s, %s);'
        dados = (produto_id, cod_barras, 0)
        cursor.execute(sql, dados)
        conn.commit()

    def update_preco_produto(self, cod_barras, novo_preco):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('UPDATE produtos p1 JOIN (SELECT id FROM produtos WHERE cod_barras = %s) '
               'p2 ON p1.id = p2.id SET p1.preco = %s;')
        dados = (cod_barras, novo_preco)
        cursor.execute(sql, dados)
        conn.commit()

    def update_marca_produto(self, cod_barras, nova_marca):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('UPDATE produtos p1 JOIN (SELECT id FROM produtos WHERE cod_barras = %s) '
               'p2 ON p1.id = p2.id SET p1.marca_produto = %s;')
        dados = (cod_barras, nova_marca)
        cursor.execute(sql, dados)
        conn.commit()

    def update_nome_produto(self, cod_barras, novo_nome):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('UPDATE produtos p1 JOIN (SELECT id FROM produtos WHERE cod_barras = %s) '
               'p2 ON p1.id = p2.id SET p1.nome_produto = %s;')
        dados = (cod_barras, novo_nome)
        cursor.execute(sql, dados)
        conn.commit()

    def registrar_entrada_produtos(self, cod_barras, preco, quantidade, data):
        conn = self.conexao_db()
        cursor = conn.cursor()

        produto_id = self.select_id_produto(cod_barras)

        sql = ('INSERT INTO entradas(produto_id, cod_barras, preco, qtd_entrada, data_entrada) '
               'VALUES (%s, %s, %s , %s, %s);')
        dados = (produto_id, cod_barras, preco, quantidade, data)

        cursor.execute(sql, dados)

        sql = 'UPDATE estoque SET qtd_estoque =  qtd_estoque + %s WHERE cod_barras = %s;'
        dados = (quantidade, cod_barras)

        cursor.execute(sql, dados)
        conn.commit()

    def select_lista_produtos(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT cod_barras FROM produtos;'
        cursor.execute(sql)
        lista_codigos = []
        for codigo in cursor.fetchall():
            lista_codigos.append(codigo[0])
        return lista_codigos

    def select_id_produto(self, cod_barras):
        conn = self.conexao_db()
        cursor = conn.cursor()
        select = f'SELECT id FROM produtos WHERE cod_barras = {cod_barras}'
        cursor.execute(select)
        produto_id = cursor.fetchall()[0][0]
        return produto_id

    def insert_promocao(self, cod_barras, preco, data_inicio, data_termino):
        conn = self.conexao_db()
        cursor = conn.cursor()
        produto_id = self.select_id_produto(cod_barras)
        sql = ('INSERT INTO precos_produtos(produto_id, cod_barras, preco_produto, data_inicio, '
               'data_termino) VALUES (%s, %s, %s, %s, %s);')
        dados = (produto_id, cod_barras, preco, data_inicio, data_termino)
        cursor.execute(sql, dados)
        conn.commit()

    def select_estoque_atual(self):
        conn = self.conn_sqlalchemy()
        with conn.connect():
            sql = text('SELECT estoque.cod_barras AS "CÓDIGO DE BARRAS", produtos.nome_produto AS PRODUTO, '
                       'estoque.qtd_estoque AS QUANTIDADE FROM estoque '
                       'INNER JOIN produtos ON estoque.produto_id = produtos.id '
                       'ORDER BY estoque.qtd_estoque ASC;')
            tabela_estoque = pd.read_sql(sql, conn)
            return st.dataframe(tabela_estoque, hide_index=True, use_container_width=True)

    def select_vendidos_30dias(self):
        conn = self.conn_sqlalchemy()
        with conn.connect():
            sql = text('''
                      SELECT 
                       pv.cod_barras AS "CÓDIGO DE BARRAS", 
                       p.nome_produto AS PRODUTO, 
                       SUM(pv.qtd_vendida) AS VENDAS
                      FROM 
                       produtos_vendidos pv
                      INNER JOIN 
                       produtos p ON pv.produto_id = p.id
                      WHERE 
                       pv.data_venda >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                      GROUP BY 
                       pv.cod_barras, p.nome_produto
                      ORDER BY VENDAS DESC;
                      ''')
            tabela_vendas30 = pd.read_sql(sql, conn)
            return st.dataframe(tabela_vendas30, hide_index=True, use_container_width=True)

    def select_vendidos_geral(self):
        conn = self.conn_sqlalchemy()
        with conn.connect():
            sql = text('SELECT cod_barras AS "CÓDIGO DE BARRAS", nome_produto AS PRODUTO, '
                       'numero_vendas AS VENDAS FROM produtos ORDER BY numero_vendas DESC;')
            tabela_vendas_geral = pd.read_sql(sql, conn)
            return st.dataframe(tabela_vendas_geral, hide_index=True, use_container_width=True)

    def select_vendas_dia(self):
        conn = self.conn_sqlalchemy()
        with conn.connect():
            sql = text('''
                        SELECT 
                        pv.cod_barras AS "CÓDIGO DE BARRAS", 
                        p.nome_produto AS PRODUTO, 
                        SUM(pv.qtd_vendida) AS VENDAS,
                        SUM(p.preco) AS "PREÇO",
                        (SUM(pv.qtd_vendida) * SUM(p.preco)) AS "PREÇO TOTAL"
                        FROM 
                        produtos_vendidos pv
                        INNER JOIN 
                        produtos p ON pv.produto_id = p.id
                        WHERE 
                        pv.data_venda >= DATE_SUB(CURDATE(), INTERVAL 01 DAY)
                        GROUP BY 
                        pv.cod_barras, p.nome_produto
                        ORDER BY VENDAS DESC;
                        ''')
            tabela_vendas_dia = pd.read_sql(sql, conn)
            return st.dataframe(tabela_vendas_dia, hide_index=True, use_container_width=True)

    def select_lista_usuarios(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT nome_usuario, cpf FROM usuarios;'
        cursor.execute(sql)
        lista_usuarios = []

        for user in cursor.fetchall():
            lista_usuarios.append(user[0])
            lista_usuarios.append(user[1])

        return lista_usuarios

    def select_lista_cpf(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT cpf FROM usuarios;'
        cursor.execute(sql)
        lista_cpf = []
    
        for user in cursor.fetchall():
            lista_cpf.append(user[0])
    
        return lista_cpf

    def select_nome_usuario(self, cpf):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT nome_usuario FROM usuarios WHERE cpf = %s;'
        dados = (cpf,)
        cursor.execute(sql, dados)
        nome_usuario = cursor.fetchall()[0][0]
        
        return nome_usuario

    def insert_cadastro_usuario(self, nome, data_nascimento, cpf, nome_usuario, senha_usuario):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('INSERT INTO usuarios(nome_completo, data_nascimento, cpf, nome_usuario, '
               'senha_usuario, nivel_acesso) '
               'VALUES (%s, %s, %s, %s, %s, %s)')
        dados = (nome, data_nascimento, cpf, nome_usuario, senha_usuario, 1)
        cursor.execute(sql, dados)
        conn.commit()

    def update_nome_usuario(self, cpf, novo_nome):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('UPDATE usuarios user1 JOIN (SELECT id FROM usuarios WHERE cpf = %s) '
               'user2 ON user1.id = user2.id SET user1.nome_usuario = %s;')
        dados = (cpf, novo_nome)
        cursor.execute(sql, dados)
        conn.commit()

    def update_senha_usuario(self, cpf, nova_senha):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('UPDATE usuarios user1 JOIN (SELECT id FROM usuarios WHERE cpf = %s) '
               'user2 ON user1.id = user2.id SET user1.senha_usuario = %s;')
        dados = (cpf, nova_senha)
        cursor.execute(sql, dados)
        conn.commit()

    def select_nome_produto(self, cod_barras):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT nome_produto FROM produtos WHERE cod_barras = %s'
        dados = (cod_barras,)
        cursor.execute(sql, dados)
        nome_produto = cursor.fetchall()[0][0]
        return nome_produto

    def select_preco_promocao(self, cod_barras):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('SELECT preco_produto FROM precos_produtos WHERE cod_barras = %s '
               'AND data_termino > CURDATE() ORDER BY data_termino DESC;')
        dados = (cod_barras,)
        cursor.execute(sql, dados)
        preco = cursor.fetchall()[0][0]
        return preco

    def select_preco_produto(self, cod_barras):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT preco FROM produtos WHERE cod_barras = %s;'
        dados = (cod_barras,)
        cursor.execute(sql, dados)
        preco = cursor.fetchall()[0][0]
        return preco

    def insert_produto_carrinho(self, nome_produto, preco, quantidade, cod_barras):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('INSERT INTO carrinho(nome_produto, preco, quantidade, valor_total, cod_barras) '
               'VALUES (%s, %s, %s, %s, %s);')
        dados = (nome_produto, preco, quantidade, preco * quantidade, cod_barras)
        cursor.execute(sql, dados)
        conn.commit()

    def delete_produto_carrinho(self, produto_id):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'DELETE FROM carrinho WHERE id = %s;'
        dados = (produto_id,)
        cursor.execute(sql, dados)
        conn.commit()

    def select_tabela_carrinho(self):
        conn = self.conn_sqlalchemy()
        with conn.connect():
            sql = text('SELECT id as ID, nome_produto as PRODUTO, preco AS PRECO, quantidade QUANTIDADE, '
                       'valor_total "VALOR TOTAL" FROM carrinho;')
            tabela_carrinho = pd.read_sql(sql, conn)
            return st.dataframe(tabela_carrinho, hide_index=True, use_container_width=True)

    def select_status_pagamento(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        try:
            sql = 'SELECT status FROM pagamentos WHERE id = (SELECT MAX(id) FROM pagamentos);'
            cursor.execute(sql)
            status = cursor.fetchall()[0][0]
            return status
        except IndexError:
            st.error('Erro! Gere um Link para efetuar o Pagamento ❌')

    def update_status_approved(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SET @ultimo_id = (SELECT MAX(id) FROM pagamentos);'
        cursor.execute(sql)
        sql = '''
              UPDATE pagamentos
              SET status = 'approved'
              WHERE id = @ultimo_id;
        '''
        cursor.execute(sql)
        conn.commit()

    def update_status_rejected(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SET @ultimo_id = (SELECT MAX(id) FROM pagamentos);'
        cursor.execute(sql)
        sql = '''
              UPDATE pagamentos
              SET status = 'rejected'
              WHERE id = @ultimo_id;
        '''
        cursor.execute(sql)
        conn.commit()

    def select_total_compra(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT SUM(valor_total) FROM carrinho'
        cursor.execute(sql)
        total_compra = cursor.fetchall()[0][0]
        return total_compra

    def insert_venda(self, data, total_compra):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'INSERT INTO vendas(data_venda, valor_venda) VALUES (%s, %s);'
        dados = (data, total_compra)
        cursor.execute(sql, dados)
        conn.commit()

    def select_venda_id(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT MAX(id) FROM vendas;'
        cursor.execute(sql)
        venda_id = cursor.fetchall()[0][0]
        return venda_id

    def select_qtd_carrinho(self):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SELECT cod_barras, quantidade FROM carrinho;'
        cursor.execute(sql)
        carrinho = cursor.fetchall()
        return carrinho

    def insert_venda_id_in_pagamentos(self, venda_id):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = """
             UPDATE pagamentos AS p1
             JOIN (SELECT MAX(id) AS max_id FROM pagamentos) AS p2
             SET p1.venda_id = %s
             WHERE p1.id = p2.max_id;
             """
        dados = (venda_id,)
        cursor.execute(sql, dados)
        conn.commit()

    def update_estoque(self, quantidade, cod_barras):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'UPDATE estoque SET qtd_estoque = qtd_estoque - %s WHERE cod_barras = %s;'
        dados = (quantidade, cod_barras)
        cursor.execute(sql, dados)
        conn.commit()

    def update_numero_vendas(self, quantidade, cod_barras):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'UPDATE produtos SET numero_vendas = numero_vendas + %s WHERE cod_barras = %s;'
        dados = (quantidade, cod_barras)
        cursor.execute(sql, dados)
        conn.commit()

    def insert_produtos_vendidos(self, produto_id, venda_id, cod_barras, quantidade, data):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = ('INSERT INTO produtos_vendidos(produto_id, venda_id, cod_barras, qtd_vendida, '
               'data_venda) VALUES (%s, %s, %s, %s, %s);')
        dados = (produto_id, venda_id, cod_barras, quantidade, data)
        cursor.execute(sql, dados)
        conn.commit()

    def limpa_produto_carrinho(self, cod_barras):
        conn = self.conexao_db()
        cursor = conn.cursor()
        sql = 'SET sql_safe_updates = 0;'
        cursor.execute(sql)
        sql = 'DELETE FROM carrinho WHERE cod_barras = %s;'
        dados = (cod_barras,)
        cursor.execute(sql, dados)
        conn.commit()
        sql = 'SET sql_safe_updates = 1;'
        cursor.execute(sql)
