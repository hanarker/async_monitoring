# Async Monitoring Azure Functions Project

Questo progetto implementa un sistema di monitoraggio asincrono utilizzando Azure Functions con Python. Il sistema è progettato per gestire operazioni di lunga durata in modo asincrono, utilizzando pattern di orchestrazione Durable Functions.

## 📋 Prerequisiti

- Python 3.8 o superiore
- [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local) versione 4.x
- [.NET SDK](https://dotnet.microsoft.com/download)
- Visual Studio Code con le seguenti estensioni:
  - Azure Functions
  - Python

## 🚀 Struttura del Progetto

```
async_monitoring/
├── async_orchestrator/     # Orchestratore principale per le funzioni durevoli
├── http_trigger_async/     # Trigger HTTP per avviare il processo
├── monitor_task/           # Funzione di monitoraggio
├── wait_and_work/          # Funzione di elaborazione
├── host.json              # Configurazione dell'host
├── local.settings.json    # Impostazioni locali
└── requirements.txt       # Dipendenze Python
```

## ⚙️ Configurazione

1. Installare le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```   
## 🏃‍♂️ Esecuzione Locale

1. Avviare l'emulatore di Azurite per lo storage locale:
   ```bash
   azurite
   ```

2. Avviare le Functions localmente:
   ```bash
   func start
   ```

## 🔄 Flusso di Lavoro

1. Il client effettua una chiamata HTTP al trigger asincrono
2. L'orchestratore gestisce il flusso di lavoro
3. La funzione wait_and_work esegue l'elaborazione
4. Il monitor_task tiene traccia dello stato
5. Il client può interrogare lo stato attraverso l'endpoint di monitoraggio

## 📌 Endpoint API

- `POST /api/http_trigger_async`: Avvia un'operazione asincrona
  ```json
  {
    "taskId": "string",
    "parameters": {}
  }
  ```

- `GET /api/monitor_task/{taskId}`: Controlla lo stato di un'operazione
  ```json
  {
    "status": "running|completed|failed",
    "result": {}
  }
  ```

## 📝 Note di Sviluppo

- Il progetto utilizza Durable Functions per la gestione dello stato
- L'emulatore Azurite è necessario per il testing locale
- I file di configurazione sono esclusi dal controllo versione

## 🤝 Contributing

1. Fork del repository
2. Crea un branch per la feature (`git checkout -b feature/amazing-feature`)
3. Commit delle modifiche (`git commit -m 'Aggiunta una feature incredibile'`)
4. Push sul branch (`git push origin feature/amazing-feature`)
5. Apri una Pull Request

## 📄 Licenza

Distribuito sotto la licenza MIT. Vedere `LICENSE` per maggiori informazioni.

## 👥 Autori

- hanarker

## ❗ Risoluzione dei Problemi

### Problemi Comuni

1. **Errore di Permessi Functions Core Tools**:
   ```bash
   chmod +x /opt/homebrew/Cellar/azure-functions-core-tools@4/4.4.0/in-proc6/func
   ```

2. **Errore di Connessione Storage**:
   - Verificare che Azurite sia in esecuzione
   - Controllare le impostazioni in local.settings.json

3. **Errore .NET SDK**:
   - Verificare l'installazione di .NET
   - Controllare la variabile PATH