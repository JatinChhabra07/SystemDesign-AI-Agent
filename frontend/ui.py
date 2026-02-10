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
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for Status & Info
with st.sidebar:
    st.title("🛠️ Agent Status")
    st.info("The multi-agent team uses Llama 3.3 (Groq) with a Gemini fallback for high reliability.")
    st.divider()

    st.markdown("**Agents Active:**")
    st.write("✅ Planner Agent")
    st.write("✅ Researcher Agent")
    st.write("✅ Architect Agent")
    st.write("✅ Validator Agent")

# Header
st.title("🏗️ SystemDesign-Pro: Agentic Architect")
st.markdown("Enter your app idea, and my multi-agent team will research and design the architecture.")

# Input Area
user_input = st.text_input(
    "What system are you building?",
    placeholder="e.g., A real-time stock trading platform"
)

# Main Button
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
                    timeout=120
                )

                # Success
                if response.status_code == 200:

                    data = response.json()

                    report = data.get("report", "")
                    title = data.get("title", "System Architecture Design")

                    st.success(f"✅ Successfully generated: {title}")

                    # Layout
                    col1, col2 = st.columns([1, 1])

                    
                    with col2:

                        st.subheader("📊 Architecture Visual")

                        # Extract Mermaid Block
                        mermaid_match = re.search(
                            r"```mermaid\s*(.*?)```",
                            report,
                            re.DOTALL
                        )

                        if mermaid_match:

                            mermaid_code = mermaid_match.group(1).strip()
                            if mermaid_code.startswith("mermaid"):
                                mermaid_code = mermaid_code.replace("mermaid", "", 1).strip()

                            # Render Diagram
                            st_mermaid(mermaid_code, key="mermaid_chart")

                        else:
                            st.info("ℹ️ No Mermaid diagram found in the report.")

                    
                    with col1:

                        st.subheader("📄 Technical Specifications")

                        # Remove Mermaid block
                        clean_report = re.sub(
                            r"```mermaid.*?```",
                            "\n\n*(See architecture diagram on the right)*\n\n",
                            report,
                            flags=re.DOTALL
                        )

                        st.markdown(clean_report)

                    st.divider()

                    # Download
                    st.download_button(
                        label="📥 Download Full Markdown Report",
                        data=report,
                        file_name=f"{title.replace(' ', '_')}.md",
                        mime="text/markdown"
                    )

                # Backend Error
                else:
                    st.error(
                        f"❌ Backend Error: {response.status_code}. "
                        "The agents may be rate-limited or crashed."
                    )

            # Connection Error
            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Could not connect to backend.\n\n"
                    "Make sure `server.py` is running on port 8000."
                )

            # Other Errors
            except Exception as e:
                st.error("❌ Unexpected error occurred.")
                st.exception(e)

# Footer
st.divider()
st.caption("SystemDesign-Pro AI | Built with LangGraph, FastAPI, and Streamlit")
