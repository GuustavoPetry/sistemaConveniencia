import streamlit as st


class Css:
    @staticmethod
    def tema():
        css = """
        <style>
        .stButton>button {
            background-color: #041360;
            color: #dae6e6;
            text-align: center;
            display: inline-block;
            width: 100%;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #271bda;
            color: #dae6e6;
        }
        .e1f1d6gn3:nth-child(1) .ef3psqc12 {
            height: 15px;
            display: flex;
        }
        .e1f1d6gn3+ .e1f1d6gn3 .ef3psqc12 {
            height: 15px;
            display: flex;
        }
        .e1f1d6gn4:nth-child(7) .ef3psqc7{
            color: #dae6e6;
            background-color: #6d0f0f;
        }
        .e1f1d6gn4:nth-child(7) .ef3psqc7:hover {
            background-color: #942020;
            color: white;
        } 
        .e1f1d6gn4:nth-child(8) .ef3psqc7{
            color: #dae6e6;
            background-color: #6d0f0f;
        }
        .e1f1d6gn4:nth-child(8) .ef3psqc7:hover {
            background-color: #942020;
            color: white;
        }
        .e1f1d6gn4:nth-child(7) .ef3psqc12:hover {
            color: #dae6e6;
            background-color: #12b716;
        }
        .e1f1d6gn4:nth-child(7) .ef3psqc12 {
            color: #dae6e6;
            background-color: #096004;
        }
        .e1f1d6gn4:nth-child(9) .ef3psqc12{
            color: #dae6e6;
            background-color: #6d0f0f;
        }
        .e1f1d6gn4:nth-child(9) .ef3psqc12:hover {
            background-color: #942020;
            color: white;
        }
        .e1f1d6gn4:nth-child(8) .ef3psqc12{
            color: #dae6e6;
            background-color: #6d0f0f;
            width: 100%;
            padding: 0px;
        }
        .e1f1d6gn4:nth-child(8) .ef3psqc12:hover {
            background-color: #942020;
            color: white;
        }
        .e1f1d6gn4:nth-child(5) .ef3psqc7 {
            color: #dae6e6;
            background-color: #096004;
        }
        .e1f1d6gn4:nth-child(5) .ef3psqc7:hover {
            color: #dae6e6;
            background-color: #12b716;
        }
        .e1f1d6gn4:nth-child(6) .ef3psqc12 {
            background-color: #041360;
            color: #dae6e6;
        }
        .e1f1d6gn4:nth-child(6) .ef3psqc7 {
            color: #dae6e6;
            background-color: #096004;
        }
        .e1f1d6gn4:nth-child(6) .ef3psqc7:hover {
            color: #dae6e6;
            background-color: #12b716;
        }
        .e1f1d6gn4:nth-child(6) .ef3psqc12:hover {
            background-color: #271bda;
            color: #dae6e6;
        }
        .e10yg2by1+ .e10yg2by1 .ef3psqc7 {
            color: #dae6e6;
            background-color: #6d0f0f;
            padding: 0px
        } 
        .e1f1d6gn4:nth-child(9) .ef3psqc7 {
            color: #dae6e6;
            background-color: #096004;
        }
        .e1f1d6gn4:nth-child(9) .ef3psqc7:hover {
            color: #dae6e6;
            background-color: #12b716;
        }
        .e10yg2by1+ .e10yg2by1 .ef3psqc7:hover {
            background-color: #942020;
            color: white;
        }
        .e16zdaao0 {
            color: #dae6e6;
            background-color: #096004;
            width: 100%;
            padding: 12px;
        }
        .e16zdaao0: hover {
            color: #dae6e6;
            background-color: #12b716;
            width: 100%;
            padding: 12px;
        }
         .ea3mdgi8 {
            background-color: #020111
        }
        .ezrtsby2 {
            background-color: #020111
        }
        .eczjsme3 {
            background-color: #020111
        }
        .e1nzilvr1 {
            color: #020111
        }
        #root :nth-child(1) {
            color: white;
        }
        .st-emotion-cache-uko8fv .ef3psqc7 {
            background-color: #041360;
            color: #dae6e6;
        }

        }
        .st-di {
            background-color:#020111
            border-color: #020111
        }
        .eczjsme8 {
            background-color: #03091D;
        }
        #number_input_4, #number_input_5 {
            background-color: #1a1a1d;
            border-color: #041360; 
        }

        .e1f1d6gn4 p {
            text-align: center;
            font-size: 18px;
        }
        .e1f1d6gn4 #carrinho {
            text-align: center;
        }
        .e1f1d6gn4 #sistema-estoque-inteligente {
            text-align: center;
        }
        .e1f1d6gn4 #bem-vindo-informe-os-dados-de-acesso {
            text-align: center;
        }
        .e1f1d6gn4 #para-visualizar-a-venda-completa-informe-o-id {
            text-align: center;
        }
        .e1f1d6gn4 #selecione-a-data-da-venda-que-deseja-consultar {
            text-align: center;
        }
        #tabs-bui13-tab-0, #tabs-bui13-tab-1, #tabs-bui13-tab-2, #tabs-bui13-tab-3, #tabs-bui13-tab-4 {
            background-color: black;
        }
        #tabs-bui15-tab-0, #tabs-bui15-tab-1, #tabs-bui15-tab-2, #tabs-bui15-tab-3 {
            background-color: black;
        }
        </style>
        """
        return st.markdown(css, unsafe_allow_html=True)
