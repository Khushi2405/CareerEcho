# LinkedIn AI Agent

A beginner-friendly AI agent that generates professional LinkedIn posts using the Google Gemini API and LangChain.  
This project demonstrates basic prompt building and API integration as the foundation for more advanced AI agent features.

---

## Setup Instructions

1. **Clone the repo:**

    ```bash
    git clone https://github.com/Khushi2405/linkedin-ai-agent.git
    cd linkedin-ai-agent
    ```

2. **Create and activate a virtual environment:**

    On macOS/Linux:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    On Windows:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4. Get your Google API key
    - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)  
    - Sign in with your Google account  
    - Click **"Create API Key"**  
    - Copy the key and paste it into your `.env` file like this:

      ```ini
      GOOGLE_API_KEY=your_actual_api_key_here
      ```
5. Run the main script:

    ```bash
    python main.py
    ```
