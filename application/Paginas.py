import streamlit as st
import mysql.connector
from datetime import datetime
from Database import Database
from Functions import Functions
data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
db = Database()
fn = Functions()


class Paginas:
    @staticmethod
    def login():
        st.title("Sistema Estoque Inteligente")
        st.subheader("Bem Vindo! Informe os dados de acesso")
        nome_usuario = st.text_input("Nome de Usuário:")
        senha_usuario = st.text_input("Senha:", type="password")
        botao_login = st.button("Login")

        if botao_login:
            usuario = db.select_credenciais(nome_usuario, senha_usuario)
            if usuario:
                st.session_state['authenticated'] = True
                st.session_state['username'] = usuario['nome_usuario']
                st.experimental_rerun()
            else:
                st.error("Dados de acesso inválidos!!")

    @staticmethod
    def menu():
        with st.sidebar:
            if st.button('Cadastrar Produtos'):
                st.session_state.form_to_show = 'cadastro-produtos'

            if st.button('Entrada de Produtos'):
                st.session_state.form_to_show = 'entrada-produtos'

            if st.button('Aplicar Promoções'):
                st.session_state.form_to_show = 'aplicar-promo'

            if st.button('Documentação'):
                st.session_state.form_to_show = 'documentacao'

            if st.button('Relatórios'):
                st.session_state.form_to_show = 'relatorios'

            if st.button('Cadastrar Usuários'):
                st.session_state.form_to_show = 'cadastro-usuario'

            if st.button('Seção de Vendas'):
                st.session_state.form_to_show = 'secao-vendas'

            if st.sidebar.button("Sair"):
                st.session_state.form_to_show = None
                st.session_state['authenticated'] = False
                st.session_state.pop('username')
                st.session_state.clear()
                st.experimental_rerun()

        if st.session_state.form_to_show == 'cadastro-produtos':
            Paginas.cadastrar_produto()

        elif st.session_state.form_to_show == 'entrada-produtos':
            Paginas.entrada_produtos()

        elif st.session_state.form_to_show == 'aplicar-promo':
            Paginas.aplicar_promocoes()

        elif st.session_state.form_to_show == 'documentacao':
            Paginas.documentacao()

        elif st.session_state.form_to_show == 'relatorios':
            Paginas.visualizar_relatorios()

        elif st.session_state.form_to_show == 'cadastro-usuario':
            Paginas.cadastrar_usuario()

        elif st.session_state.form_to_show == 'secao-vendas':
            Paginas.secao_vendas()

    @staticmethod
    def cadastrar_produto():
        tab1, tab2, tab3, tab4 = st.tabs(['Cadastrar Produto', 'Atualizar Preço', 'Atualizar Marca', 'Atualizar Nome'])
        if st.session_state.form_to_show == 'cadastro-produtos':

            with tab1:
                with st.form('cadastrar-produto', True):
                    st.title("Seção para Cadastro de Produtos")
                    marca = st.text_input('Marca:', placeholder='Marca do Produto')
                    nome = st.text_input('Nome:', placeholder='Nome do Produto')
                    cod_barras = st.text_input('Cód. Barras:', placeholder='Código de Barras')
                    preco = st.number_input('Preço:')
                    botao_cad = st.form_submit_button("Cadastrar")

                    if botao_cad:
                        nivel_acesso = db.select_nivel_acesso(st.session_state['username'])
                        if nivel_acesso == 3:
                            if marca != '' and nome != '' and cod_barras != '' and preco > 0:
                                try:
                                    db.insert_cadastrar_produto(marca, nome, cod_barras, preco, data)
                                    st.success('✅ Produto Cadastrado no Sistema ✅')
                                except mysql.connector.errors.IntegrityError:
                                    st.error('❌ Erro! Já existe um cadastro com este código de barras ou nome ❌')
                            else:
                                st.error('❌ Erro! Preencha todos os dados do produto corretamente ❌')
                        else:
                            st.error('❌ Nível de acesso não permitido para esta ação! ❌')

            with tab2:
                with st.form('atualizar-preco', True):
                    st.title('Atualizar Preço de Produto')
                    st.subheader('Preencha os Campos para Atualizar o Preço do Produto')
                    cod_barras = st.text_input('Informe o Código de Barras do Produto:', placeholder='Código de Barras')
                    novo_preco = st.number_input('Escolha um novo Preço para o produto:')
                    st.write('')

                    if st.form_submit_button('Atualizar Preço'):
                        if cod_barras != '' and novo_preco > 0:
                            nivel_acesso = db.select_nivel_acesso(st.session_state['username'])
                            if nivel_acesso == 3:
                                db.update_preco_produto(cod_barras, novo_preco)
                                st.success(f'O Preço do Produto foi Atualizado para R${novo_preco} ✅')
                            else:
                                st.error('Nível de Acesso não permitido para está ação ❌')
                        else:
                            st.error('❌ Erro! Preencha todos os dados do produto corretamente ❌')

            with tab3:
                with st.form('atualizar-marca', True):
                    st.title('Atualizar Marca de Produto')
                    st.subheader('Preencha os Campos para Atualizar a Marca do Produto')
                    cod_barras = st.text_input('Informe o Código de Barras do Produto:', placeholder='Código de Barras')
                    nova_marca = st.text_input('Escolha uma Nova Marca:', placeholder='Nova Marca do Produto')
                    st.write('')

                    if st.form_submit_button('Atualizar Marca'):
                        if cod_barras != '' and nova_marca != '':
                            nivel_acesso = db.select_nivel_acesso(st.session_state['username'])
                            if nivel_acesso == 3:
                                db.update_marca_produto(cod_barras, nova_marca)
                                st.success(f'Marca do Produto Atualizada para {nova_marca} ✅')
                            else:
                                st.error('Nível de Acesso não permitido para esta ação ❌')
                        else:
                            st.error('❌ Erro! Preencha todos os dados do produto corretamente ❌')

            with tab4:
                with st.form('atualizar-nome-produto'):
                    st.title('Atualizar Nome de Produto')
                    st.subheader('Preencha os Campos para Atualizar o Nome do Produto')
                    cod_barras = st.text_input('Informe o Código de Barras do Produto:', placeholder='Código de Barras')
                    novo_nome = st.text_input('Escolha um Novo Nome:', placeholder='Novo Nome do Produto')
                    st.write('')

                    if st.form_submit_button('Atualizar Nome'):
                        if cod_barras != '' and novo_nome != '':
                            nivel_acesso = db.select_nivel_acesso(st.session_state['username'])
                            if nivel_acesso == 3:
                                db.update_nome_produto(cod_barras, novo_nome)
                                st.success(f'Nome do Produto Atualizado para {novo_nome} ✅')
                            else:
                                st.error('Nível de Acesso não permitido para está ação ❌')
                        else:
                            st.error('❌ Erro! Preencha todos os dados do produto corretamente ❌')

    @staticmethod
    def entrada_produtos():
        if st.session_state.form_to_show == 'entrada-produtos':
            with st.form('entrada-produtos', True):
                st.title("Seção para Entrada de Produtos")
                st.subheader("preencha os Campos para Entrada de Produtos")
                cod_barras = st.text_input("Código de Barras:", placeholder='Cód. Barras')
                preco_entrada = st.number_input("Preço de Entrada:")
                quantidade = st.text_input("Quantidade:", placeholder='Quantidade')
                botao_cad = st.form_submit_button('Registrar')

                if botao_cad:
                    if cod_barras != '' and preco_entrada != '' and quantidade != '':
                        try:
                            db.registrar_entrada_produtos(cod_barras, preco_entrada, quantidade, data)
                            st.success('✅ O Produto foi inserido no estoque ✅')
                        except mysql.connector.errors.DatabaseError:
                            st.error('❌ Erro! Somente números inteiros para quantidade ❌')
                        except IndexError:
                            st.error('❌ Erro! O Produto não está cadastrado no sistema ❌')
                    else:
                        st.error('❌ Erro! Preencha todos os dados do produto corretamente ❌')

    @staticmethod
    def aplicar_promocoes():
        if st.session_state.form_to_show == 'aplicar-promo':
            with st.form('aplicar-promocao', True):
                st.title("Seção para Aplicar Promoções")
                st.subheader("preencha as Informações da Promoção")
                cod_barras = st.text_input('Código de Barras:', placeholder='Cód. Barras')
                preco_promo = st.number_input('Preço Promocional')
                data_inicio = data
                data_termino = st.date_input('Data FIM da Promoção:')
                botao_cad = st.form_submit_button('Aplicar')

                if botao_cad:
                    lista_produtos = db.select_lista_produtos()
                    if cod_barras in lista_produtos and cod_barras != '' and preco_promo != '':
                        db.insert_promocao(cod_barras, preco_promo, data_inicio, data_termino)
                        st.success(f'Promoção Aplicada, com validade até {data_termino}')
                    else:
                        st.error('❌ Erro! O Produto não é cadastrado no sistema ❌')

    @staticmethod
    def visualizar_relatorios():
        if st.session_state.form_to_show == 'relatorios':
            st.title("Seção para Análise de Relatórios")
            st.subheader("Navegue entre as abas para visualizar os diferentes tipos de relatórios")
            tab1, tab2, tab3, tab4 = st.tabs(['Estoque Atual', '+ Mais Vendidos (30 Dias)',
                                                    '+ Mais Vendidos (Geral)', 'Vendas (24hrs)'])
            with tab1:
                db.select_estoque_atual()

            with tab2:
                db.select_vendidos_30dias()

            with tab3:
                db.select_vendidos_geral()

            with tab4:
                db.select_vendas_dia()

            # with tab5:
            #     col1, col2, col3, col4 = st.columns([0.4, 0.1, 0.4, 0.1])
            #     with col1:
            #         st.subheader('Selecione a Data da Venda que Deseja Consultar')
            #         seleciona_data = st.date_input('Data Venda:')
            #         buscar_vendas = st.button('Buscar')
            #         if buscar_vendas:
            #             db.select_vendas(seleciona_data)
            #     with col2:
            #         st.write('')
            #     with col3:
            #         st.subheader('Para Visualizar a Venda Completa informe o ID')
            #         venda_id = st.number_input('ID Venda:', min_value=1)
            #         acessar_venda = st.button('Acessar')
            #         if acessar_venda:
            #             db.select_produtos_venda(venda_id)
            #     with col4:
            #         st.write('')

    @staticmethod
    def cadastrar_usuario():
        if st.session_state.form_to_show == 'cadastro-usuario':
            tab1, tab2, tab3 = st.tabs(['Cadastrar Usuário', 'Alterar Nome Usuário', 'Alterar Senha Usuário'])

            with tab1:
                with st.form('cadastro_usuario', True):
                    st.title("Seção para Cadastro de Usuários")
                    st.subheader("Preencha os dados do usuário que deseja cadastrar")
                    nome = st.text_input('Nome Completo:', placeholder='Nome Completo')
                    data_nascimento = st.date_input('Data de Nascimento')
                    cpf = st.text_input('CPF:', placeholder='Informe o CPF')
                    nome_usuario = st.text_input('Nome de Usuário:', placeholder='Username')
                    senha_usuario = st.text_input('Senha:', type='password', placeholder='Senha')
                    confirma_senha = st.text_input('Confirme a Senha:', type='password', placeholder='Senha')
                    botao_cad = st.form_submit_button('Cadastrar')

                    if botao_cad:
                        lista_usuarios = db.select_lista_usuarios()
                        nivel_acesso = db.select_nivel_acesso(st.session_state['username'])

                        if nivel_acesso == 3:
                            
                            if nome_usuario not in lista_usuarios and cpf not in lista_usuarios:
                                if senha_usuario == confirma_senha:
                                    if nome != '' and cpf != '' and nome_usuario != '' and senha_usuario != '':
                                        db.insert_cadastro_usuario(nome, data_nascimento, cpf, nome_usuario,
                                                                       senha_usuario)
                                        st.success('✅ Usuário Cadastrado com Sucesso ✅')
                                    else:
                                        st.error('❌ Erro! Preencha todos os dados do produto corretamente ❌')
                                else:
                                    st.error('❌ Erro! Você informou 2 senhas diferentes ❌')
                            else:
                                st.error('❌ Erro! Já existe um usuário com estes dados cadastrados! ❌')

                        
                        else:
                            st.error('❌ Nível de acesso não permitido para esta ação! ❌')

            with tab2:
                with st.form('atualizar-nome-usuario', True):
                    st.title('Alterar Nome de Usuário')
                    st.subheader('Preencha os Campos para Alterar Nome de Usuário')
                    cpf = st.text_input('CPF do Usuário que deseja Alterar o Nome:', placeholder='Informe o CPF')
                    novo_nome = st.text_input('Novo Nome de Usuário', placeholder='Escolha um novo Nome de Usuário')

                    if st.form_submit_button('Alterar Username'):

                        if cpf != '' and novo_nome != '':
                            nivel_acesso = db.select_nivel_acesso(st.session_state['username'])

                            if nivel_acesso == 3:
                                db.update_nome_usuario(cpf, novo_nome)
                                st.success(f'Nome de Usuário Alterado para {novo_nome} ✅')

                            else:
                                st.error('Nível de Acesso não permitido para está ação ❌')

                        else:
                            st.error('❌ Erro! Preencha todos os dados do produto corretamente ❌')

            with tab3:
                with st.form('atualizar-senha-usuario', True):
                    st.title('Alterar Senha de Usuário')
                    st.subheader('Preencha os Campos para Alterar Senha do Usuário')
                    cpf = st.text_input('CPF do Usuário que deseja Alterar a Senha:', placeholder='Informe o CPF')
                    nova_senha = st.text_input('Nova Senha do Usuário', placeholder='Escolha uma Nova Senha',
                                               type='password')
                    confirma_senha = st.text_input('Confirme a Senha:', placeholder='Insira a Senha Novamente',
                                                   type='password')

                    if st.form_submit_button('Alterar Senha'):

                        if cpf != '' and nova_senha != '' and confirma_senha != '':
                            nivel_acesso = db.select_nivel_acesso(st.session_state['username'])

                            if nivel_acesso == 3:
                                if nova_senha == confirma_senha:
                                    db.update_senha_usuario(cpf, nova_senha)
                                    st.success(f'Senha de Usuário Alterada com Sucesso ✅')
                                else:
                                    st.error('Erro! Você informou 2 Senhas diferentes ❌')
                            else:
                                st.error('Nível de Acesso não permitido para está ação ❌')
                        else:
                            st.error('❌ Erro! Preencha todos os dados do produto corretamente ❌')

    @staticmethod
    def secao_vendas():
        if st.session_state.form_to_show == 'secao-vendas':
            col1, col2 = st.columns([0.3, 0.7])
            with col1:
                with st.form('secao-vendas', True):
                    st.subheader("Scaneie todos os Produtos")
                    cod_barras = st.text_input('Código de Barras:', placeholder='Scaneie o código de barras')
                    quantidade = st.number_input('Quantidade:', min_value=1)

                    if st.form_submit_button('Inserir'):
                        lista_produtos = db.select_lista_produtos()
                        if cod_barras in lista_produtos:
                            nome_produto = db.select_nome_produto(cod_barras)
                            try:
                                preco = db.select_preco_promocao(cod_barras)
                                db.insert_produto_carrinho(nome_produto, preco, quantidade, cod_barras)
                            except IndexError:
                                preco = db.select_preco_produto(cod_barras)
                                db.insert_produto_carrinho(nome_produto, preco, quantidade, cod_barras)
                        else:
                            st.error('Erro! O Código informado não está cadastrado no sistema ❌')

                with st.form('cancelar-produto'):
                    cancelar_id = st.number_input('Retirar do Carrinho Produto ID:', min_value=1)
                    retirar_produto = st.form_submit_button('Retirar')
                    if retirar_produto:
                        db.delete_produto_carrinho(cancelar_id)

            with col2:
                with st.form('carrinho'):
                    st.title('Carrinho')
                    db.select_tabela_carrinho()
                    botao_venda = st.form_submit_button('Gerar Link Pagamento')

                    if botao_venda:
                        len_carrinho = db.select_len_carrinho()

                        if len_carrinho > 0:
                            fn.hiperlink_pagamento()
                            st.write('Finalizado o Pagamento Clique em Verificar 👇')

                        else:
                            st.error('Erro! O Carrinho está Vazio ❌')

                    else:
                        hiperlink = ''
                        st.markdown(hiperlink, unsafe_allow_html=True)

                    if st.form_submit_button('Verificar Pagamento'):
                        len_carrinho = db.select_len_carrinho()

                        if len_carrinho > 0:
                            status = db.select_status_pagamento()

                            if status == 'None':
                                fn.registra_status()
                                fn.verifica_status_pagamento(data)

                            elif status == 'rejected':
                                fn.registra_status()
                                fn.verifica_status_pagamento(data)

                            elif status == '':
                                st.error('Erro! Gere um novo Link para efetuar o Pagamento ❌')
                        else:
                            st.error('Erro! O Carrinho está Vazio ❌')

                    st.write('')
                    if st.form_submit_button('Cancelar Compra'):
                        db.truncate_carrinho()
                        st.experimental_rerun()

    @staticmethod
    def documentacao():
        st.title('INSTRUÇÕES DE USO DO SISTEMA')
        st.subheader('Documentação')
        tab1, tab2, tab3 = st.tabs(
            ['REALIZAR VENDAS E APLICAR PROMOÇÕES', 'CADASTRO E ENTRADA DE PRODUTOS', 'CADASTRO DE USUÁRIOS'])

        with tab1:
            st.video('videos/venda_promocao.mp4', autoplay=True)
            st.write('* PARA REALIZAR UMA VENDA LEIA O CÓDIGO DE TODOS OS PRODUTOS (DISPONÍVEL EM >> RELATÓRIOS <<)'
                     ' E APÓS CLIQUE EM '
                     '">> GERAR LINK DE PAGAMENTO <<, CLIQUE NO LINK GERADO PARA REALIZAR O PAGAMENTO. '
                     'APÓS FINALIZAR O PAGAMENTO CLIQUE EM >> VERIFICAR PAGAMENTO <<. SE O PAGAMENTO FOR '
                     'APROVADO O CARRINHO SERÁ LIMPO E A COMPRA FINALIZADA.')
            st.write('* PARA APLICAÇÃO DE PROMOÇÕES VÁ EM >> APLICAR PROMOÇÕES << E PREENCHA OS CAMPOS, '
                     'INFORMANDO A DATA FIM DA PROMOÇÃO. >> OBS: NO DIA DA DATA ESCOLHIDA A PROMOÇÃO JÁ NÃO TERÁ MAIS '
                     'VALIDADE <<')
            st.subheader('* DADOS DO CARTÃO PARA SIMULAÇÃO DE PAGAMENTO:')
            st.write('* PARA PAGAMENTO APROVADO UTILIZE O NOME DO TITULAR -> APRO')
            st.write('* PARA PAGAMENTO REPROVADO UTILIZE O NOME DO TITULAR -> OTHE')
            st.write('* Nº CARTÃO -> 5031 4332 1540 6351')
            st.write('* VALIDADE -> 11/25')
            st.write('* CÓDIGO DE SEGURANÇA -> 123')
            st.write('* CPF -> 12345678909')

        with tab2:
            st.video('videos/cadastro_entrada.mp4')
            st.write('* PARA REALIZAR O CADASTRO DE PRODUTOS NO SISTEMA VÁ EM >> CADASTRAR PRODUTOS << E PREENCHA TODOS'
                     ' OS CAMPOS. ')
            st.write('* IMPORTANTE:\n * O PREÇO FORNECIDO NO CADASTRO SERÁ O VALOR COBRADO PELO PRODUTO NAS VENDAS, '
                     'DESDE QUE NÃO SEJA APLICADA UMA PROMOÇÃO.\n* SÓ PODE HAVER 1 CADASTRO PRA CADA CÓDIGO DE BARRAS.')

        with tab3:
            st.video('videos/cadastro_usuario.mp4')
            st.write('* PARA REALIZAR O CADASTRO DE NOVOS USUÁRIOS NO SISTEMA, VÁ EM >> CADASTRAR USUÁRIOS << '
                     'E PREENCHA TODOS OS CAMPOS. OBS: SÓ PODE HAVER 1 CADASTRO PARA CADA CPF E USERNAME.')
