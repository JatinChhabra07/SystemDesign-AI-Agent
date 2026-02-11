import streamlit as st
import requests
from streamlit_mermaid import st_mermaid
import re

# Page Config
st.set_page_config(
    page_title="SystemDesign-Pro AI",
    page_icon="🏗️",
    layout="wide"
)

# Custom Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    
    /* --- NEW: MERMAID DIAGRAM OPTIMIZATION --- */
    /* Target the Mermaid SVG specifically to force a readable size */
    svg[id^="mermaid-"] {
        max-width: none !important; /* Allow the diagram to be wider than the page */
        width: 1200px !important;   /* Force a large width */
        height: auto !important;
    }
    
    /* Optional: Add a scrollbar if the diagram exceeds column width */
    div.stHtml {
        overflow-x: auto !important;
        padding-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIDEBAR: RAG KNOWLEDGE BASE & STATUS ---
with st.sidebar:
    st.title("📚 Knowledge Base")
    st.markdown("Upload PDFs to provide context and **reduce API costs** by using local data first.")
    
    uploaded_file = st.file_uploader("Upload System Docs (PDF)", type="pdf")
    
    if uploaded_file is not None:
        if st.button("🚀 Process & Index PDF"):
            with st.spinner("Ingesting into local Vector DB..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    # Pointing to the new ingest endpoint in main.py
                    res = requests.post("http://localhost:8000/ingest", files=files)
                    if res.status_code == 200:
                        st.success(f"✅ '{uploaded_file.name}' indexed successfully!")
                    else:
                        st.error(f"Failed to index: {res.text}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
    
    st.divider()
    st.title("🛠️ Agent Status")
    st.info("The multi-agent team uses Llama 3.3 (Groq) with a Gemini fallback for high reliability.")
    
    st.markdown("**Core Capabilities:**")
    st.write("✅ Local RAG (ChromaDB)")
    st.write("✅ Web Search (Tavily)")
    st.divider()
    st.markdown("**Agents Active:**")
    st.write("✅ Planner | ✅ Researcher")
    st.write("✅ Architect | ✅ Validator")

# --- MAIN HEADER ---
st.title("🏗️ SystemDesign-Pro: Agentic Architect")
st.markdown("Enter your app idea, and my multi-agent team will research and design the architecture.")

# Input Area
user_input = st.text_input(
    "What system are you building?",
    placeholder="e.g., A real-time stock trading platform"
)

# Main Execution Button
if st.button("Generate Architecture"):

    if not user_input:
        st.warning("Please enter a system idea first!")

    else:
        with st.spinner("🚀 Agents are collaborating (Researching → Designing → Validating)..."):

            try:
                # Backend API Call
                response = requests.post(
                    "http://localhost:8000/design",
                    json={
                        "query": user_input,
                        "thread_id": "session_1"
                    },
                    timeout=300 
                )

                # Success Handling
                if response.status_code == 200:

                    data = response.json()
                    report = data.get("report", "")
                    title = data.get("title", "System Architecture Design")

                    st.success(f"✅ Successfully generated: {title}")

                    # 50/50 Layout for Specs and Visuals
                    col1, col2 = st.columns([0.3, 0.7])

                    with col2:
                        st.subheader("📊 Architecture Visual")

                        # Extract Mermaid Block using Regex
                        mermaid_match = re.search(
                            r"```mermaid\s*(.*?)```",
                            report,
                            re.DOTALL
                        )

                        if mermaid_match:
                            mermaid_code = mermaid_match.group(1).strip()

                            with st.expander("🔍 Debug: See Raw Mermaid Code"):
                                st.code(mermaid_code, language="mermaid")

                            # Strip leading 'mermaid' text if LLM included it inside backticks
                            if mermaid_code.lower().startswith("mermaid"):
                                mermaid_code = mermaid_code.replace("mermaid", "", 1).strip()

                            # Render the Interactive Diagram
                            st_mermaid(mermaid_code, height=600,key="mermaid_chart")
                        else:
                            st.info("ℹ️ No visual diagram found. The technical specs may still be valid.")
                            

                    with col1:
                        st.subheader("📄 Technical Specifications")

                        # Clean report: replace raw mermaid code with a friendly note
                        clean_report = re.sub(
                            r"```mermaid.*?```",
                            "\n\n*(Visual diagram rendered on the right)*\n\n",
                            report,
                            flags=re.DOTALL
                        )

                        st.markdown(clean_report)

                    st.divider()

                    # Download Feature
                    st.download_button(
                        label="📥 Download Full Markdown Report",
                        data=report,
                        file_name=f"{title.replace(' ', '_')}.md",
                        mime="text/markdown"
                    )

                # Backend Error Handling
                else:
                    st.error(
                        f"Backend Error: {response.status_code}. "
                        "The agents may be rate-limited or the server encountered an issue."
                    )

            # Connection Error Handling
            except requests.exceptions.ConnectionError:
                st.error(
                    "Connection Failed.\n\n"
                    "Please ensure your FastAPI backend (`main.py`) is running on http://localhost:8000"
                )

            except Exception as e:
                st.error("An unexpected error occurred.")
                st.exception(e)

# Footer
st.divider()
st.caption("SystemDesign-Pro AI | Local RAG + Multi-Agent Orchestration")