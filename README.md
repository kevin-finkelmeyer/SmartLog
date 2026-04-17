# SmartLog
KI-gestützter Log-Analyzer

# Features
Analysiert Log-Dateien, extrahiert die wichtigsten Infos und liefert mittels KI Lösungsansätze.

# Requirements
- **Python 3.14** 
- [Groq API Key](https://groq.com/)

# Installation
1. Repository klonen
2. Virtual Environment erstellen und aktivieren (```python -m venv .venv```, ```.venv/Scripts/activate```)
2. Dependencies installieren (```pip install -r requirements.txt```) 
3. .env datei erstellen (Siehe .env.example)

# Usage
Im Verzeichnis mittels ```python ./smartlog/analyzer.py [filename]``` aufrufen

# Beispiel-Output
```
ANOMALY: High frequency of errors and unexpected errors.

ROOT CAUSE: Potential issues with db-service, io-service, and auth-service, possibly due to code bugs or configuration problems.

ACTION: Investigate db-service, io-service, and auth-service logs for patterns or specific error messages. Review code and configuration for these services to identify and fix the root cause.```