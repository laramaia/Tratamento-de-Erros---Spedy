import streamlit as st
import pandas as pd

def carregar_arquivo(arquivo):
    if arquivo.name.endswith("xlsx"):
        df = pd.read_excel(arquivo, engine="openpyxl")
        return df
    else:
        df = pd.read_csv(arquivo)
        return df


def download_arquivo_tratado(arquivo, op=None, partes=None):
    if op == "Dividir planilha (arquivo grande)" and partes:
        st.dataframe(partes[0])
        st.dataframe(partes[1])
        st.download_button("Baixar Parte 1", partes[0].to_csv(index=False).encode('utf-8'), file_name="metade1.csv", mime="text/csv")
        st.download_button("Baixar Parte 2", partes[1].to_csv(index=False).encode('utf-8'), file_name="metade2.csv", mime="text/csv")
    else:
        st.dataframe(arquivo)
        st.download_button("Baixar arquivo CSV", arquivo.to_csv(index=False).encode('utf-8'), file_name="PlanilhaAlterada.csv", mime="text/csv")