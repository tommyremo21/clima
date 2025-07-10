
import streamlit as st
import pandas as pd

# Carica il file Excel
df = pd.read_excel("File_App_Tommaso.xlsx", sheet_name="File App", engine="openpyxl")

# Funzione per estrarre le righe con unità esterne e le relative compatibilità
def get_matches_from_external():
    matches = []
    current_external = None
    current_code = None
    for _, row in df.iterrows():
        if pd.notna(row[4]) and "Unità esterna" in str(row[4]):
            current_external = row[5]
            current_code = row[8]
            matches.append({
                "unità_esterna": current_external,
                "codice_esterna": current_code,
                "unità_interne": []
            })
        elif pd.notna(row[10]) and "Unità interna" in str(row[10]):
            if matches:
                matches[-1]["unità_interne"].append({
                    "descrizione": row[11],
                    "codice": row[17]
                })
    return matches

# Funzione per estrarre le righe con unità interne e le relative compatibilità
def get_matches_from_internal():
    matches = []
    current_internal = None
    current_code = None
    for _, row in df.iterrows():
        if pd.notna(row[10]) and "Unità interna" in str(row[10]):
            current_internal = row[11]
            current_code = row[17]
            matches.append({
                "unità_interna": current_internal,
                "codice_interna": current_code,
                "unità_esterne": []
            })
        elif pd.notna(row[4]) and "Unità esterna" in str(row[4]):
            if matches:
                matches[-1]["unità_esterne"].append({
                    "descrizione": row[5],
                    "codice": row[8]
                })
    return matches

st.title("🔄 Match Unità Esterne e Interne Baxi")

tab1, tab2 = st.tabs(["🔹 Da Unità Esterna", "🔸 Da Unità Interna"])

with tab1:
    st.header("Seleziona un'unità esterna")
    esterne = get_matches_from_external()
    opzioni = [f"{e['unità_esterna']} ({e['codice_esterna']})" for e in esterne]
    scelta = st.selectbox("Unità esterna:", opzioni)
    selezionata = esterne[opzioni.index(scelta)]
    st.subheader("Unità interne compatibili:")
    for ui in selezionata["unità_interne"]:
        st.markdown(f"- **{ui['descrizione']}** (Codice: `{ui['codice']}`)")

with tab2:
    st.header("Seleziona un'unità interna")
    interne = get_matches_from_internal()
    opzioni = [f"{i['unità_interna']} ({i['codice_interna']})" for i in interne]
    scelta = st.selectbox("Unità interna:", opzioni)
    selezionata = interne[opzioni.index(scelta)]
    st.subheader("Unità esterne compatibili:")
    for ue in selezionata["unità_esterne"]:
        st.markdown(f"- **{ue['descrizione']}** (Codice: `{ue['codice']}`)")
