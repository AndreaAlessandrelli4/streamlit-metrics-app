import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import json

# Carica i dati dai file JSON
with open('metriche_TOTALI.json', 'r', encoding='utf-8') as f:
    data1 = json.load(f)
with open('metriche_TOTALI_prompt_UNICO.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)

# Funzione ricorsiva per esplorare le voci annidate e confrontare i dati
def navigate_data(data1, data2, path=[]):
    if all(isinstance(v, (float, int)) for v in data1.values()):  # Siamo al livello delle metriche
        display_metrics(data1, data2, path)
    else:  # Annidamento
        selected_key = st.selectbox(f"Seleziona una voce:", list(data1.keys()))
        navigate_data(data1[selected_key], data2[selected_key], path + [selected_key])

# Funzione per visualizzare e confrontare le metriche
def display_metrics(metrics1, metrics2, path):
    #st.subheader(f"Confronto metriche per: {' > '.join(path)}")

    # Converti in DataFrame
    df1 = pd.DataFrame(metrics1.items(), columns=["Metrica", "Valore1"])
    df2 = pd.DataFrame(metrics2.items(), columns=["Metrica", "Valore2"])

    # Unisci i dati
    df = pd.merge(df1, df2, on="Metrica", how="outer").fillna(0)

    # Filtro basato sulla soglia
    threshold = st.slider("Soglia minima per visualizzare le metriche", 0.0, 1.0, 0.0, 0.05)
    filtered_df = df[(df["Valore1"] >= threshold) | (df["Valore2"] >= threshold)]

    if filtered_df.empty:
        st.warning("Nessuna metrica supera la soglia definita.")
        return

    # Visualizza il confronto con barre affiancate
    fig, ax = plt.subplots()
    x = np.arange(len(filtered_df))
    width = 0.4

    bars1 =  ax.barh(x - width/2, filtered_df["Valore1"], width, label='Multiple prompt extraction', color='blue')
    bars2 = ax.barh(x + width/2, filtered_df["Valore2"], width, label='Unique prompt extraction', color='orange')
    
    ax.set_yticks(x)
    ax.set_yticklabels(filtered_df["Metrica"])
    ax.set_xlim(0, 1.1)
    ax.set_xticks([0.0,0.2,0.4,0.6,0.8,1.0],[0.0,0.2,0.4,0.6,0.8,1.0])
    ax.set_xlabel("Valore")
    ax.set_title("Confronto Metriche")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Aggiungi etichette con i valori sopra le barre
    for bars in [bars1, bars2]:
        ax.bar_label(bars, fmt="%.2f", padding=3)

    st.pyplot(fig)
    
    # Scarica dati in CSV
    st.markdown("### Scarica i dati selezionati")
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Scarica CSV", data=csv, file_name=f"{'_'.join(path)}_comparison.csv", mime="text/csv")

# Titolo
st.title("Confronto delle metriche di estrazione")

# Inizia la navigazione dai dati di base
navigate_data(data1, data2)
