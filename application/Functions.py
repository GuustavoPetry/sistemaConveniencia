import streamlit as st
import mercadopago
from Database import Database
db = Database()


class Functions:
    @staticmethod
    def hiperlink_pagamento():
        hiperlink = f"""
                    <div style="display: flex; justify-content: center; align-items: center;">
                        <p style="text-align: center; font-size: 30px;">
                            <a href="{Functions.gerar_link_pagamento()}" target="_blank">Clique aqui para pagar</a>
                        </p>
                    </div>
                    """
        return st.markdown(hiperlink, unsafe_allow_html=True)

    @staticmethod
    def gerar_link_pagamento():
        len_carrinho = db.select_len_carrinho()
        len_pagamentos = db.select_len_pagamentos()

        if len_pagamentos == 0:
            db.insert_primeiro_pagamento()
        else:
            status_max_pagamento = db.select_status_pagamento()
            if status_max_pagamento == 'rejected':
                db.insert_novo_pagamento()

        if len_carrinho > 0:
            identificador = db.select_max_identificador()
            sdk = mercadopago.SDK(st.secrets["mp_token"])
            preference_data = {
                'items': [],
                "external_reference": f'{identificador}'
            }
            produtos_carrinho = db.select_montar_pagamento()

            for produto in produtos_carrinho:
                preference_data['items'].append({"id": produto[0], "title": produto[1], "quantity": produto[2],
                                                 "currency_id": "BRL", "unit_price": float(produto[3])})
            result = sdk.preference().create(preference_data)
            payment = result["response"]
            link_iniciar_pagamento = payment["init_point"]
            return link_iniciar_pagamento
        else:
            st.error('Erro! O Carrinho está Vazio ❌')

    @staticmethod
    def consulta_pagamento():
        identificador = db.select_max_identificador()

        sdk = mercadopago.SDK(st.secrets["mp_token"])

        filters = {
            "sort": "date_created",
            "criteria": "desc",
            "range": "date_created",
            "external_reference": f"{identificador}",
            "begin_date": "NOW-5HOURS",
            "end_date": "NOW"
        }

        search_request = sdk.payment().search(filters)
        resultados = search_request['response']['results']

        if len(resultados) < 1:
            return
        if resultados[0]['external_reference'] == str(identificador) and resultados[0]['status'] == "approved":
            return 'approved'
        elif resultados[0]['external_reference'] == str(identificador) and resultados[0]['status'] == "rejected":
            return 'rejected'

    def registra_status(self):
        if self.consulta_pagamento() == 'approved':
            db.update_status_approved()

        elif self.consulta_pagamento() == 'rejected':
            db.update_status_rejected()

    @staticmethod
    def debita_estoque(data):
        total_compra = db.select_total_compra()
        db.insert_venda(data, total_compra)
        venda_id = db.select_venda_id()
        carrinho = db.select_qtd_carrinho()
        db.insert_venda_id_in_pagamentos(venda_id)
        db.insert_novo_pagamento()
        for item in carrinho:
            cod_barras = item[0]
            quantidade = item[1]
            produto_id = db.select_id_produto(cod_barras)
            db.update_estoque(quantidade, cod_barras)
            db.update_numero_vendas(quantidade, cod_barras)
            db.insert_produtos_vendidos(produto_id, venda_id, cod_barras, quantidade, data)
            db.limpa_produto_carrinho(cod_barras)
        st.experimental_rerun()

    def verifica_status_pagamento(self, data):
        status = db.select_status_pagamento()
        if status == 'approved':
            self.debita_estoque(data)
        elif status == 'rejected':
            st.error('Erro! O Pagamento foi REJEITADO ❌')
        elif status == 'None':
            st.error('Erro! O Pagamento ainda NÃO foi Realizado ❌')
