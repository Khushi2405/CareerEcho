# CareerEcho

CareerEcho is an AI-powered assistant designed to help users enhance their career development and learning journey. It provides comprehensive features for career growth, professional networking, and study assistance.

## Live Demo
Access the app here: [Career Agent](https://career-echo.streamlit.app/)

## Features
- **Resume Analysis**: Upload and get detailed analysis of PDF resumes with targeted feedback
- **LinkedIn Post Generator**: Create engaging LinkedIn posts with multiple variations and AI-powered editing
- **Study Cheatsheet Generator**: Generate comprehensive study cheatsheets for any topic with downloadable PDF format

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Khushi2405/CareerEcho.git
   ```
2. Navigate to the project directory:
   ```sh
   cd CareerEcho
   ```
3. **Create and activate a virtual environment (optional):**

    On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    On Windows:
    ```bash
    python -m venv venv
    source venv\Scripts\activate
    ```

4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. **Set up your Google API key:**
    - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)  
    - Sign in with your Google account  
    - Click **"Create API Key"**  
    - Create a `.env` file in the project root and add your key:
      ```ini
      GOOGLE_API_KEY=your_actual_api_key_here
      ```
6. Run the application:
    ```bash
    streamlit run main.py
    ```

## Project Structure
```
CareerEcho/
├── main.py                 # Entry point for the application
├── pages/                  # Contains UI and logic for different pages
│   ├── input_page.py      # LinkedIn post generation interface
│   ├── edit_page.py       # LinkedIn post editing and refinement
│   ├── upload_pdf.py      # Resume upload and analysis
│   └── cheatsheet_page.py # Study cheatsheet generator
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this file)
└── README.md              # Project documentation
```

## How to Use

### 📄 Resume Analysis
1. Upload your resume in PDF format
2. Specify the target role you're applying for
3. Get comprehensive feedback on education, experience, skills, and projects
4. Receive keyword suggestions and improvement recommendations

### ✍️ LinkedIn Post Generator
1. Enter your post topic and details
2. Select post type, tone, and target audience
3. Choose number of variations to generate (1-10)
4. Optionally include hashtags and emojis
5. Edit and refine posts with AI assistance

### 📚 Study Cheatsheet Generator
1. Enter the topic you want to study
2. Select difficulty level and cheatsheet type
3. Choose content length and additional requirements
4. Generate comprehensive markdown-formatted cheatsheets
5. Download as professionally formatted PDF

## Dependencies
- `streamlit` - Web application framework
- `langchain-google-genai` - Google Gemini AI integration
- `python-dotenv` - Environment variable management
- `PyPDF2` - PDF processing for resume analysis
- `reportlab` - PDF generation for cheatsheets

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.