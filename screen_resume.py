import streamlit as st
import pdfplumber
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Configuration
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")

st.title("📄 AI-Powered Resume Screening & Ranking Tool")
st.markdown("Upload candidate resumes in PDF format and provide a job description to automatically rank candidates based on relevance.")

# Sidebar for Job Description Input
st.sidebar.header("🎯 Job Description Setup")
job_description = st.sidebar.text_area(
    "Paste the Job Description here:",
    height=250,
    placeholder="Enter required skills, experience, and qualifications..."
)

# Main area for Resume Uploads
st.subheader("📁 Upload Candidate Resumes")
uploaded_files = st.file_uploader(
    "Upload PDF resumes", 
    type=["pdf"], 
    accept_multiple_files=True
)

def extract_text_from_pdf(uploaded_file):
    """Extract raw text from an uploaded PDF resume file object."""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        st.error(f"Error reading {uploaded_file.name}: {e}")
    return text

if st.button("🚀 Screen & Rank Resumes", type="primary"):
    if not job_description.strip():
        st.warning("Please enter a job description in the sidebar first!")
    elif not uploaded_files:
        st.warning("Please upload at least one PDF resume!")
    else:
        with st.spinner("Processing and ranking resumes..."):
            resumes_data = []
            documents = [job_description]
            
            # Extract text from each uploaded resume
            for file in uploaded_files:
                text = extract_text_from_pdf(file)
                if text.strip():
                    resumes_data.append({"filename": file.name, "text": text})
                    documents.append(text)
            
            if not resumes_data:
                st.error("Could not extract text from the uploaded PDFs.")
            else:
                # Compute TF-IDF Vectors
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(documents)
                
                # Compute Cosine Similarity between Job Description (index 0) and each resume
                similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
                
                # Build results list
                results = []
                for idx, data in enumerate(resumes_data):
                    score = float(similarity_scores[idx]) * 100  # Convert to percentage
                    results.append({
                        "Candidate File": data["filename"],
                        "Match Score (%)": round(score, 2),
                        "Status": "Top Match" if score >= 20 else "Moderate" if score >= 10 else "Low Match"
                    })
                
                # Sort candidates by score descending
                df_results = pd.DataFrame(results).sort_values(by="Match Score (%)", ascending=False).reset_index(drop=True)
                
                # Display Results
                st.success("Screening Complete!")
                st.subheader("🏆 Candidate Ranking Report")
                
                # Style and display dataframe
                st.dataframe(
                    df_results,
                    column_config={
                        "Match Score (%)": st.column_config.ProgressColumn(
                            "Match Score (%)",
                            format="%.1f%%",
                            min_value=0,
                            max_value=100,
                        )
                    },
                    use_container_width=True
                )
                
                # Provide CSV download for report deliverable
                csv_data = df_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Candidate Ranking Report (CSV)",
                    data=csv_data,
                    file_name="candidate_ranking_report.csv",
                    mime="text/csv",
                )



   
