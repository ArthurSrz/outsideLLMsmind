# InsideLLMsmind 🤖

![Animation - 1696517035167 (2)](https://github.com/ArthurSrz/insideLLMsmind/assets/55806298/39d7326f-5612-469b-bae8-79b7cd25878b)

## À propos / About

**InsideLLMsmind** est une petite application pour montrer que les modèles de langage (LLMs) ne sont pas des boîtes noires mystérieuses qui donnent des réponses intelligentes du néant. Ils peuvent être soigneusement conçus et adaptés pour répondre à des besoins spécifiques.

Dans cette application, deux agents IA ont été enchaînés ensemble. L'un peut récupérer des informations sur Internet, l'autre peut effectuer des calculs mathématiques. En fonction de votre question, l'application utilisera automatiquement l'outil approprié.

**Inside LLMs mind** is a small app to demonstrate that LLMs are not essentially black boxes that give out smart answers out of the fog. They can be carefully crafted and designed to answer specific needs.

In this app, two AI agents have been chained together. One can retrieve info on the Internet, the other perform math calculations. Depending on your prompt it will use the appropriate tool automatically.

## Caractéristiques / Features

- 🧠 **Visualize Agent Thinking** / **Visualisez la Pensée de l'Agent** - Voyez exactement comment l'agent réfléchit et prend ses décisions
- 🔧 **Tool Selection** / **Sélection d'Outil** - Comprenez comment l'agent choisit entre la calculatrice et la recherche Internet
- 📊 **Step-by-Step Explanation** / **Explication Étape par Étape** - Chaque étape est expliquée de manière claire et progressive
- 👶 **Kid-Friendly** / **Adapté aux Enfants** - Conçu pour être compris par les enfants de 5 ans!

## Comment utiliser / How to Use

```bash
# Installation des dépendances / Install dependencies
pip install -r requirements.txt

# Lancer l'application / Run the app
streamlit run app.py
```

## Configuration / Setup

### 🔑 API Key Configuration

The app checks for your OpenAI API key in this order:
1. `OPENAI_API_KEY` environment variable (highest priority)
2. Streamlit secrets (`.streamlit/secrets.toml`)

**Local Development - Method 1: Using Secrets File (Recommended)**

1. Create or edit `.streamlit/secrets.toml`:
```toml
openai_api_key = "sk-your-openai-api-key-here"
```

2. Run the app:
```bash
streamlit run app.py
```

**Local Development - Method 2: Using Environment Variable**

```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
streamlit run app.py
```

**Streamlit Cloud Deployment**

1. Go to your deployed app on Streamlit Cloud
2. Click **"Manage app"** (top right)
3. Go to **Settings** → **Secrets**
4. Add your secret:
```toml
openai_api_key = "sk-your-openai-api-key-here"
```
5. Redeploy the app

⚠️ **Important:** Never commit `.streamlit/secrets.toml` to git - it's in `.gitignore` for security!

## Examples / Exemples

Posez une question simple comme / Ask a simple question like:
- "Combien font 5 plus 3?" / "What is 5 plus 3?"
- "Qu'est-ce qu'un nuage?" / "What is a cloud?"

## Plus d'informations / More Info

Détails sur l'application dans mon carnet de recherche / Details about the app on my research notebook: https://dataflow.hypotheses.org/1068
