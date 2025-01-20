import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import io
import json


with open('/Users/andreaalessandrelli/Desktop/Legal/chat/metriche.json', 'r', encoding='utf-8') as f:
    data = json.load(f)




# Funzione ricorsiva per esplorare le voci annidate
def navigate_data(data, path=[]):
    if all(isinstance(v, (float, int)) for v in data.values()):  # Siamo al livello delle metriche
        display_metrics(data, path)
    else:  # Annidamento
        selected_key = st.selectbox(f"Seleziona una voce ({' > '.join(path)})", list(data.keys()))
        navigate_data(data[selected_key], path + [selected_key])

# Funzione per visualizzare le metriche
def display_metrics(metrics, path):
    st.subheader(f"Metriche per: {' > '.join(path)}")

    # Converti in DataFrame
    df_metrics = pd.DataFrame(metrics.items(), columns=["Metrica", "Valore"])

    # Filtro basato sulla soglia
    threshold = st.slider("Soglia minima per visualizzare le metriche", 0.0, 1.0, 0.0, 0.05)
    filtered_df = df_metrics[df_metrics["Valore"] >= threshold]

    if filtered_df.empty:
        st.warning("Nessuna metrica supera la soglia definita.")
        return

    # Colori con sfumature graduali (da rosso a verde)
    norm = mcolors.Normalize(vmin=0, vmax=1)
    cmap = plt.cm.get_cmap("RdYlGn")
    colors = filtered_df["Valore"].apply(lambda x: mcolors.to_hex(cmap(norm(x))))

    # Visualizza barre orizzontali
    fig, ax = plt.subplots()
    bars = ax.barh(filtered_df["Metrica"], filtered_df["Valore"], color=colors)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Valore")
    ax.set_title("Metriche")

    # Mostra valori accanto alle barre
    for bar, value in zip(bars, filtered_df["Valore"]):
        ax.text(value + 0.02, bar.get_y() + bar.get_height() / 2, f"{value:.2f}", va='center')

    # Mostra il grafico in Streamlit
    st.pyplot(fig)
    https://github.com/AndreaAlessandrelli4/streamlit-metrics-app

    # Scarica dati in CSV
    st.markdown("### Scarica i dati selezionati")
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Scarica CSV", data=csv, file_name=f"{'_'.join(path)}_metrics.csv", mime="text/csv")

# Titolo
st.title("Visualizzazione delle metriche")

# Inizia la navigazione dai dati di base
navigate_data(data)
