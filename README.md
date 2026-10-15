# Review-Analyser

Analyses customer reviews with Google Gemini. For each review it returns:

- **label**: `positive`, `negative` or `neutral`
- **score**: a sentiment score from 1 to 10
- **theme**: a short summary of what the review is about

It has a FastAPI backend that calls Gemini, and a Streamlit app where you can paste many reviews at once, see the results, save them to a local SQLite database and browse past results.

## Project structure

| File | Purpose |
|---|---|
| `api.py` | FastAPI app with the `POST /analyze` endpoint that calls Gemini |
| `streamlit_app.py` | Streamlit UI: analyze reviews, save results, view history |
| `database.py` | SQLite helpers: `init_db`, `save_results`, `read_history` |
| `main.py` | Minimal FastAPI app with `/` and `/health` endpoints |
| `.env.example` | Template for the `.env` file that holds your API key |

## Setup

You need Python 3.10 or newer.

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/MaruthiEranki/Review-Analyser.git
cd Review-Analyser

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Set up your Gemini API key

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).
2. Copy the example file to create your own `.env`:

   ```bash
   cp .env.example .env
   ```

3. Open `.env` and replace the placeholder with your key:

   ```
   GEMINI_API_KEY=your-actual-key-here
   ```

`api.py` loads this file automatically when it starts. If the key is missing, the API fails at startup with `KeyError: 'GEMINI_API_KEY'`.

> **Never commit your `.env` file.** It is already listed in `.gitignore`. Only `.env.example`, which has no real key, belongs in the repo.

## Running the app

Run the API and the UI in two separate terminals, with the virtual environment activated in both.

**Terminal 1: start the API**

```bash
fastapi dev api.py
```

The API runs at http://localhost:8000. Interactive docs are at http://localhost:8000/docs.

**Terminal 2: start the Streamlit UI**

```bash
streamlit run streamlit_app.py
```

Streamlit opens in your browser, usually at http://localhost:8501.

## Using the app

1. Paste reviews into the text box, **one review per line**.
2. Click **Analyze**. Each review is sent to the API, and the results appear in a table.
3. Click **Save** to store the results in the database.
4. The **History** section shows every saved result, newest first.

Results are stored in `reviews.db`, a SQLite file created in the folder you start Streamlit from.

## Calling the API directly

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "The food was great but the service was slow."}'
```

Example response:

```json
{
  "label": "neutral",
  "score": 6,
  "theme": "Good food, slow service"
}
```
