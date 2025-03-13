import streamlit as st
from datetime import datetime
from Css import Css
from Paginas import Paginas
from Database import Database
from Functions import Functions

data = datetime.now().strftime('%Y-%m-%d')
db = Database()
fn = Functions()
app = Paginas()
css = Css()


def main():
    st.set_page_config(page_title="Estoque Inteligente", layout="wide", page_icon="🍻")
    css.tema()
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if st.session_state['authenticated']:
        if 'form_to_show' not in st.session_state:
            st.session_state.form_to_show = 'secao-vendas'
        app.menu()
    else:
        app.login()


# Chamada da função de login
if __name__ == '__main__':
    main()
