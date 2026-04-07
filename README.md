# Private NEPSE AI Advisor

A private web application built with Python and Streamlit to analyze the Nepal Stock Exchange (NEPSE), predict future trends, and act as a personal trading tutor using LLMs.

## Features
- **Privacy First**: Password-protected access.
- **Market Analysis**: Historical charts and basic future trend prediction algorithms.
- **AI Tutor**: Integrated AI chat to teach you trading concepts and act as your financial advisor.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dipeshkharal065/nepse-ai-advisor.git
   cd nepse-ai-advisor
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API Key:**
   You will need an OpenAI API key for the AI Tutor to work. Set it in your terminal:
   ```bash
   # Windows
   set OPENAI_API_KEY="your_api_key_here"
   
   # Mac/Linux
   export OPENAI_API_KEY="your_api_key_here"
   ```

4. **Run the Website:**
   ```bash
   streamlit run app.py
   ```
   *The app will open automatically in your browser at `http://localhost:8501`. The default password is `my_secret_nepse_password` (you should change this in `app.py`).*