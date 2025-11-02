import streamlit as st
import requests
import time

# Cambia questo URL se deploy su Azure
BASE_URL = "http://localhost:7071/api"

st.title("🚀 Monitoraggio Funzione Asincrona (Durable)")

# Codice CSS per animazioni personalizzate
st.markdown(
    """
    <style>
    .pulse {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #4CAF50;
        box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% {
            transform: scale(0.9);
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
        }
        70% {
            transform: scale(1);
            box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
        }
        100% {
            transform: scale(0.9);
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
        }
    }
    </style>
    """, unsafe_allow_html=True
)

if 'job_id' not in st.session_state:
    st.session_state.job_id = None
if 'log' not in st.session_state:
    st.session_state.log = []
if 'show_confirmation' not in st.session_state:
    st.session_state.show_confirmation = False

# Funzione per aggiungere log
def add_log(message: str):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.log.append(f"[{timestamp}] {message}")

# Bottone per aprire il popup
if st.button("Avvia Funzione", key="start_btn"):
    st.session_state.show_confirmation = True

# Popup di conferma
if st.session_state.show_confirmation:
    with st.container():
        st.write("### ❗ Attenzione")
        st.write("Stai per avviare un processo asincrono che richiederà alcuni secondi.")
        disclaimer = st.checkbox("Ho letto e accetto il disclaimer. Confermo di voler avviare il processo.", key="disclaimer_checkbox")

        if st.button("Conferma e Avvia", disabled=not disclaimer, key="confirm_btn"):
            st.session_state.show_confirmation = False  # Chiudi il popup
            add_log("Avvio processo richiesto.")
            # Mostra un messaggio animato durante l'invio
            status_start = st.empty()
            status_start.markdown(f"📤 <span class='pulse'></span> Invio richiesta al server...", unsafe_allow_html=True)

            try:
                response = requests.post(f"{BASE_URL}/http_trigger_async", json={})
                add_log(f"Richiesta inviata. Status Code: {response.status_code}")
                job_id = response.json()["job_id"]
                st.session_state.job_id = job_id
                add_log(f"Funzione avviata con Job ID: {job_id}")
                status_start.success(f"✅ Funzione avviata! Job ID: `{job_id}`")
            except Exception as e:
                add_log(f"Errore durante l'avvio: {e}")
                status_start.error(f"❌ Errore: {e}")

        if st.button("Annulla", key="cancel_btn"):
            st.session_state.show_confirmation = False

if st.session_state.job_id:
    job_id = st.session_state.job_id
    st.write(f"**Job ID:** `{job_id}`")

    status_placeholder = st.empty()
    status_placeholder.markdown(f"🔄 <span class='pulse'></span> Stato: `in attesa...`", unsafe_allow_html=True)

    start_time = time.time()
    add_log(f"Monitoraggio avviato per Job ID: {job_id}")

    while True:
        try:
            resp = requests.get(f"{BASE_URL}/status/{job_id}")
            data = resp.json()
            status = data.get("status", "unknown")
            result = data.get("result")

            # Aggiorna lo stato con animazione
            if status == "running" or status == "pending":
                status_placeholder.markdown(f"🔄 <span class='pulse'></span> Stato: `{status}`", unsafe_allow_html=True)
                add_log(f"Stato aggiornato a: {status}")
            elif status == "completed":
                end_time = time.time()
                elapsed = end_time - start_time
                status_placeholder.success(f"✅ Completato! Risultato: `{result}` in {elapsed:.2f} secondi.")
                add_log(f"Processo completato. Risultato: {result}. Tempo impiegato: {elapsed:.2f}s")
                break
            elif status == "failed":
                status_placeholder.error("❌ Errore nell'esecuzione.")
                add_log("Processo fallito.")
                break
            else:
                status_placeholder.warning(f"❓ Stato sconosciuto: {status}")
                add_log(f"Stato sconosciuto ricevuto: {status}")
                break

        except Exception as e:
            st.error(f"❌ Errore nel recupero dello stato: {e}")
            add_log(f"Errore nel recupero dello stato: {e}")
            break

        time.sleep(1)

# Sezione di logging
with st.expander("📋 Log attività"):
    if st.session_state.log:
        for entry in st.session_state.log:
            st.text(entry)
    else:
        st.text("Nessun log disponibile.")