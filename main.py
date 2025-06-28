import streamlit as st
import pandas as pd
from utils import carregar_arquivo, download_arquivo_tratado

def converter_data(df):
    for col in df.columns:
        try:
            # Tenta converter a coluna para datetime
            df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='raise') 
            # Se a conversão funcionar, formatação é feita
            df[col] = df[col].dt.strftime('%d/%m/%Y')

        except Exception:
            pass

    return df


def converter_valor(df):
    colunas_para_converter = ["valor", "preco"]  
    colunas_alvo = []

    # Identifica as colunas que devem ser convertidas
    for item in colunas_para_converter:
        for col in df.columns:
            if item.lower() in col.lower():
                colunas_alvo.append(col)

    # Converte somente as colunas identificadas
    for col in colunas_alvo:
        try:
            df[col] = df[col].astype(float).round(2)
            df[col] = df[col].astype(str).str.replace(".", ",", regex=False)
        except Exception:
            pass

    return df


with open("style.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.title("Tratamento de Erros em Planilha")
st.subheader("Correção de erros mais comuns ao tratar planilhas.")
st.write("")
st.markdown("""
**REGRAS DE USO**  
- Apenas arquivos .csv e .xlsx são aceitos;
- O resultado do tratamento é um arquivo .csv;
- O nome das colunas a serem alteradas precisam ser digitados **exatamente** como na planilha;
- Ao escolher a opção Adicionar Caractere, por padrão, o caractere a ser adicionado será \'A\';
- Datas são transformadas em texto automaticamente.
- O formato UTF-8 já é aplicado automaticamente.
- A formatação das colunas com números na tabela do programa não estão formatadas. A formatação correta pode ser vista no arquivo .csv exportado.
""")

st.markdown("**Arraste o arquivo ou clique para selecionar**")
upload = st.file_uploader("", type=["xlsx", "csv"])

df = None
if upload is not None:   # Se upload não estiver vazio, transforma arquivo em df
    df = carregar_arquivo(upload)
    df = converter_data(df)
    df = converter_valor(df)

operacao = st.selectbox("O que deseja fazer? ", ("Adicionar caractere no início da coluna", "Transformar coluna em texto", "Dividir planilha (arquivo grande)", "Filtrar planilha por mês/ano"))

if operacao == "Adicionar caractere no início da coluna":
    coluna_a_alterar = st.text_input("Insira o nome da coluna que deseja adicionar um caractere: ")
    if df is not None:
        if coluna_a_alterar in df.columns:
            df[coluna_a_alterar] = df[coluna_a_alterar].astype(str)
            df[coluna_a_alterar] = "A" + df[coluna_a_alterar]
            download_arquivo_tratado(df)
        else:
            st.error("Coluna não encontrada.")

elif operacao == "Transformar coluna em texto":   
    coluna_a_alterar = st.text_input("Insira o nome da coluna que deseja transformar em texto: ")
    if df is not None:
        if coluna_a_alterar in df.columns:
            df[coluna_a_alterar] = df[coluna_a_alterar].astype(str)
            download_arquivo_tratado(df)
        else:
            st.error("Coluna não encontrada.")

elif operacao == "Dividir planilha (arquivo grande)":
    if df is not None:
        meio = len(df) // 2
        metade1 = df.iloc[:meio]
        metade2 = df.iloc[meio:]

        download_arquivo_tratado(df, op="Dividir planilha (arquivo grande)", partes=[metade1, metade2])

elif operacao == "Filtrar planilha por mês/ano":
    coluna_a_filtrar = st.text_input("Insira o nome da coluna que deseja realizar o filtro")
    if df is not None:
        if coluna_a_filtrar in df.columns:
            try:
                # retorna "na" caso conversão não funcione
                df[coluna_a_filtrar] = pd.to_datetime(df[coluna_a_filtrar], format="%d/%m/%Y", errors="coerce")
                mes_a_filtrar = st.multiselect("Insira o mês a ser filtrado:", list(range(1, 13)))
                ano_a_filtrar = st.slider("Ano a ser filtrado:", 2020, 2025, 2025)

                if not mes_a_filtrar or not ano_a_filtrar:
                    st.error("Insira mês e ano.")

                # df apenas com as linhas que possuem o mês/ano escolhido
                df = df[(df[coluna_a_filtrar].dt.month.isin(mes_a_filtrar)) & (df[coluna_a_filtrar].dt.year == ano_a_filtrar)] 
                df[coluna_a_filtrar] = df[coluna_a_filtrar].dt.strftime('%d/%m/%Y')

                download_arquivo_tratado(df)

            except Exception:
                pass

        else:
            st.error("Coluna não encontrada.")
