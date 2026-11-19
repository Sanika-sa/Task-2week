import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(page_title="AI Content Generator", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Generator")
st.markdown("Generate professional blog posts, social media captions, or text summaries instantly based on your topic and tone.")

# Sidebar for API Key and Configuration
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

# Main Input Form
content_type = st.selectbox(
    "Select Content Type:",
    ["Blog Post", "Social Media Caption", "Content Summary"]
)

topic = st.text_input("Enter Topic or Keywords:", placeholder="e.g., The Future of Artificial Intelligence in Healthcare")

tone = st.selectbox(
    "Select Tone:",
    ["Professional", "Casual & Friendly", "Persuasive", "Informative", "Humorous"]
)

if st.button("🚀 Generate Content", type="primary"):
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar.")
    elif not topic.strip():
        st.warning("Please enter a topic or keywords.")
    else:
        with st.spinner("Generating content..."):
            try:
                # Initialize Gemini client
                client = genai.Client(api_key=api_key)
                
                # Construct prompt template
                prompt = f"Write a {tone.lower()} {content_type.lower()} about the following topic: {topic}. Ensure the content is engaging, high-quality, and well-structured."
                
                # Call Gemini model
                response = client.models.generate_content(
                 model='gemini-3.5-flash-lite',
                 contents=prompt
                )
                
                generated_text = response.text
                
                # Display Generated Content
                st.subheader("📄 Generated Output")
                st.write(generated_text)
                
                # Metrics: Word and Character counts
                words = len(generated_text.split())
                chars = len(generated_text)
                
                col1, col2 = st.columns(2)
                col1.metric("Word Count", words)
                col2.metric("Character Count", chars)
                
                # Copy-friendly text box
                st.text_area("Copy Output:", value=generated_text, height=150)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                


