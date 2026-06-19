# LLM Gateway

A high-performance, local API gateway and beautiful UI for interacting with multiple Large Language Model (LLM) providers (Groq and OpenRouter) through a single unified interface.

## 🌟 Features

*   **Unified API Interface:** Switch between Groq and OpenRouter without changing your client code.
*   **Real-time Streaming:** Token-by-token streaming responses for a fast, responsive user experience.
*   **Modern Web UI:** Built-in beautiful, dark-themed UI served directly from the backend.
*   **Markdown & Syntax Highlighting:** AI responses are rendered in rich Markdown with code syntax highlighting.
*   **Copy Code functionality:** Easily copy code snippets with a single click (works seamlessly in secure contexts).
*   **Dynamic Model Fetching:** Automatically fetches the latest free-tier models from OpenRouter.

## 🚀 Tech Stack

*   **Backend:** FastAPI, Python, Uvicorn
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript, Marked.js, Highlight.js
*   **Integrations:** Groq API SDK, OpenAI SDK (used for OpenRouter), HTTPX

## 📂 Project Structure

```text
AI-GATEWAY/
├── main.py                     # FastAPI application entry point
├── routers/
│   └── chat.py                 # API routes for chat and model listing
├── services/
│   ├── groq_service.py         # Groq API integration (sync & stream)
│   └── openrouter_service.py   # OpenRouter API integration (sync & stream)
├── schemas/
│   └── chat.py                 # Pydantic models for validation
├── frontend/
│   └── llm-gateway-ui.html     # The beautiful chat interface
├── .env                        # Environment variables (API keys)
└── requirements.txt            # Python dependencies
```

## 🛠️ Installation & Setup

1.  **Clone the repository** (if applicable) and navigate to the project directory:
    ```bash
    cd AI-GATEWAY
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install aiofiles  # Required for serving the frontend static files
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    OPENROUTER_API_KEY=your_openrouter_api_key_here
    ```

## 🏃‍♂️ How to Run

1.  **Start the FastAPI server:**
    Ensure your virtual environment is activated, then run:
    ```bash
    uvicorn main:app --reload
    ```

2.  **Access the Application:**
    *   **Chat UI:** Open your browser and go to: [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui)
    *   **API Documentation (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    *   **Alternative Docs (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🔌 API Endpoints

*   `POST /api/chat/stream`: Streams the LLM response token by token (used by the UI).
*   `POST /api/chat`: Returns the complete LLM response in a single JSON payload.
*   `GET /api/models`: Returns a static list of configured models for both providers.
*   `GET /api/openrouter-models`: Fetches the live list of free-tier models directly from the OpenRouter API.

## 📝 Important Notes

*   **Clipboard API (Copy Button):** The UI uses the modern `navigator.clipboard` API which requires a secure context. Serving the UI through FastAPI (via `http://127.0.0.1`) ensures this works natively. If opened directly via `file://`, a fallback mechanism is implemented.
*   **Adding Models:** You can update the static model lists in `routers/chat.py` or `frontend/llm-gateway-ui.html`. Make sure to use the exact model IDs as provided by the respective platforms (e.g., `meta-llama/llama-3.3-70b-instruct:free`).
