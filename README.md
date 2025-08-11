# CareerEcho

CareerEcho is an AI-powered assistant designed to help users enhance their career development. It provides features such as resume analysis and generating professional LinkedIn posts. Mre features will be added in the future.

## Live Demo
Access the app here: [Career Agent](https://career-echo.streamlit.app/)


## Features
- Upload and analyze PDF resumes
- Generate LinkedIn Posts and edit them

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Khushi2405/CareerEcho.git
   ```
2. Navigate to the project directory:
   ```sh
   cd CareerEcho
   ```
2. **Create and activate a virtual environment(optional):**

    On macOS/Linux:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    On Windows:

    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```

4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Get your Google API key
    - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)  
    - Sign in with your Google account  
    - Click **"Create API Key"**  
    - Copy the key and paste it into your `.env` file like this:

      ```ini
      GOOGLE_API_KEY=your_actual_api_key_here
      ```
6. Run the main script:

    ```bash
    streamlit run main.py

    ```

## Project Structure
- `main.py`: Entry point for the application
- `pages/`: Contains UI and logic for different pages
  - `input_page.py`: Handles user input to generate linkedin posts
  - `edit_page.py`: Allows editing selected linkedin posts
  - `upload_pdf.py`: upload resume to get detailed analysis
- `requirements.txt`: Python dependencies

## License
This project is licensed under the MIT License.
