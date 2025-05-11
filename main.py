import streamlit as st
import pandas as pd

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


st.title("Tratamento de Erro de Planilha")
st.subheader("Correção de erros mais comuns ao tratar planilhas. Para outros, é preciso verificar manualmente.")
st.write("")
st.markdown("""
**AVISOS**  
- Apenas arquivos CSV e XLSX são permitidos;
- O formato aceito pelos apps costumam ser o CSV. Logo, o resultado do tratamento é um arquivo CSV;
- O nome das colunas a serem alteradas precisam ser digitados **exatamente** como está na planilha;
- Ao escolher a opção Adicionar Caractere, por padrão, o caractere a ser adicionado será \'A\';
- O formato UTF-8 já é aplicado automaticamente.
""")

upload = st.file_uploader("Insira o arquivo para análise", type=["xlsx", "csv"])
# TODO: alterar todas as colunas do tipo data para string

df = None
if upload is not None:   # Se upload não estiver vazio, transforma arquivo em df
    if upload.name.endswith("xlsx"):
        df = pd.read_excel(upload, engine="openpyxl")
    else:
        df = pd.read_csv(upload)
    
    # Chama função de ajuste de data
    df = converter_data(df)
    df = converter_valor(df)

operacao = st.selectbox("O que deseja fazer? ", ("Adicionar caractere no início da coluna", "Transformar coluna em texto", "Dividir planilha (arquivo grande)"))

if operacao == "Adicionar caractere no início da coluna":
    coluna_a_alterar = st.text_input("Insira o nome da coluna que deseja adicionar um caractere: ")
    if df is not None:
        if coluna_a_alterar in df.columns:
            df[coluna_a_alterar] = df[coluna_a_alterar].astype(str)
            df[coluna_a_alterar] = "A" + df[coluna_a_alterar]

            st.dataframe(df)

            st.download_button("Baixar arquivo CSV", df.to_csv(index=False).encode('utf-8'), file_name="PlanilhaAlterada.csv", mime="text/csv")
        else:
            st.error("Coluna não encontrada.")

elif operacao == "Transformar coluna em texto":   
    coluna_a_alterar = st.text_input("Insira o nome da coluna que deseja transformar em texto: ")
    if df is not None:
        if coluna_a_alterar in df.columns:
            df[coluna_a_alterar] = df[coluna_a_alterar].astype(str)

            st.dataframe(df)
            
            st.download_button("Baixar arquivo CSV", df.to_csv(index=False).encode('utf-8'), file_name="PlanilhaAlterada.csv", mime="text/csv")
        else:
            st.error("Coluna não encontrada.")

elif operacao == "Dividir planilha (arquivo grande)":
    if df is not None:
        meio = len(df) // 2
        metade1 = df.iloc[:meio]
        metade2 = df.iloc[meio:]

        st.dataframe(metade1)
        st.dataframe(metade2)

        st.download_button("Baixar Parte 1", metade1.to_csv(index=False).encode('utf-8'), file_name="metade1.csv", mime="text/csv")
        st.download_button("Baixar Parte 2", metade2.to_csv(index=False).encode('utf-8'), file_name="metade2.csv", mime="text/csv")
