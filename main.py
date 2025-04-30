import streamlit as st
import openai
from dotenv import load_dotenv
import os
import socket
import sys
import warnings
import logging

# Suppress all warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

# Configure logging
logging.getLogger('streamlit').setLevel(logging.ERROR)

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# Set page config
st.set_page_config(
    page_title="Text to SQL Converter",
    page_icon="🔍",
    layout="centered"
)

# Title and description
st.title("Text to SQL Converter")
st.write("Enter your text description and get a SQL query!")

# Text input
user_input = st.text_area(
    "Enter your text description:",
    placeholder="e.g., Show me all customers who made purchases above $1000 in the last month",
    height=100
)

# Function to generate SQL query
def generate_sql(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a SQL expert. Convert the given text to a SQL query. Only return the SQL query, no explanations."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating SQL: {str(e)}")
        return None

# Generate SQL button
if st.button("Generate SQL"):
    if user_input:
        with st.spinner("Generating SQL query..."):
            sql_query = generate_sql(user_input)
            if sql_query:
                st.code(sql_query, language="sql")
    else:
        st.warning("Please enter some text first!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using OpenAI and Streamlit")

if __name__ == '__main__':
    port = 8501  # Streamlit's default port
    local_ip = get_ip()
    
    print("""
    ╔════════════════════════════════════════════╗
    ║            Text to SQL Converter           ║
    ╚════════════════════════════════════════════╝
    """)
    print(f"""
    🚀 Server is running!
    
    💻 Local URL:     http://localhost:{port}
    🌐 Network URL:   http://{local_ip}:{port}
    
    ⌛ Waiting for requests...
    
    Press Ctrl+C to quit.
    """)
    
    # Run Streamlit only if not already running
    if not os.environ.get('STREAMLIT_SERVER_RUNNING'):
        os.environ['STREAMLIT_SERVER_RUNNING'] = 'true'
        os.environ['STREAMLIT_LOGGING_LEVEL'] = 'error'
        os.system(f"streamlit run {os.path.abspath(__file__)} --logger.level=error")
