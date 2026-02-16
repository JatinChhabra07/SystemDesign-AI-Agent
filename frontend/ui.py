import streamlit as st
import requests
from streamlit_mermaid import st_mermaid
import re
import os


if "messages" not in st.session_state:
    st.session_state.messages = []



# Page Config
st.set_page_config(
    page_title="Systemly.AI",
    page_icon="🚀",
    layout="wide"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/design")

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

    svg[id^="mermaid-"] {
        max-width: none !important;
        width: 1200px !important;
        height: auto !important;
    }

    div.stHtml {
        overflow-x: auto !important;
        padding-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")

    user_api_key = st.text_input(
        "Enter Groq API Key",
        type="password",
        help="Get your key at console.groq.com"
    )

    if not user_api_key:
        st.warning("⚠️ Please provide an API key.")

    st.divider()

    st.title("📚 Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload System Docs (PDF)",
        type="pdf"
    )

    if uploaded_file:
        if st.button("🚀 Process & Index PDF"):
            with st.spinner("Indexing..."):
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }

                try:
                    res = requests.post(
                        "http://localhost:8000/ingest",
                        files=files
                    )

                    if res.status_code == 200:
                        st.success("✅ Indexed!")
                    else:
                        st.error(res.text)

                except Exception as e:
                    st.error(e)

    st.divider()

    st.title("🛠️ Agent Status")

    st.info("Multi-agent system active")

    st.write("✅ Planner")
    st.write("✅ Researcher")
    st.write("✅ Architect")
    st.write("✅ Validator")



st.title("Systemly AI — Intelligent Agents for System Architecture Design")

st.markdown(
    "Enter your app idea, and my multi-agent team will design it."
)


st.subheader("💬 Assistant History")

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(
            f"🧠 **Assistant:**\n\n{msg['content']}"
        )

st.divider()



user_input = st.text_input(
    "What system are you building?",
    placeholder="e.g., A real-time stock trading platform"
)


if st.button("Generate Architecture"):

    if not user_api_key:
        st.error("Please enter API key!")

    elif not user_input:
        st.warning("Enter system idea!")

    else:

        with st.spinner("🚀 Agents Working..."):

            if "thread_id" not in st.session_state:
                import uuid
                st.session_state.thread_id = str(uuid.uuid4())

            try:

                # Store user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input
                })

                response = requests.post(
                    BACKEND_URL,
                    json={
                        "query": user_input,
                        "thread_id": st.session_state.thread_id
                    },
                    headers={
                        "X-Groq-API-Key": user_api_key
                    },
                    timeout=500
                )

               

                if response.status_code == 200:

                    data = response.json()

                    report = data.get("report", "")
                    title = data.get("title", "System Design")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": report
                    })

                    st.success(f"✅ Generated: {title}")

                    col1, col2 = st.columns([0.3, 0.7])


                    with col2:

                        st.subheader("📊 Architecture Visual")

                        mermaid_match = re.search(
                            r"```mermaid\s*(.*?)```",
                            report,
                            re.DOTALL
                        )

                        if mermaid_match:

                            mermaid_code = mermaid_match.group(1).strip()

                            with st.expander("🔍 Raw Mermaid"):
                                st.code(mermaid_code)

                            if mermaid_code.lower().startswith("mermaid"):
                                mermaid_code = mermaid_code.replace(
                                    "mermaid", "", 1
                                ).strip()

                            st_mermaid(
                                mermaid_code,
                                height=600,
                                key="mermaid_chart"
                            )

                        else:
                            st.info("No diagram found")


                    with col1:

                        st.subheader("📄 Technical Specs")

                        clean_report = re.sub(
                            r"```mermaid.*?```",
                            "\n\n*(Diagram on right)*\n\n",
                            report,
                            flags=re.DOTALL
                        )

                        st.markdown(clean_report)

                    st.divider()


                    st.download_button(
                        "📥 Download Report",
                        report,
                        file_name=f"{title.replace(' ', '_')}.md",
                        mime="text/markdown"
                    )


                else:

                    st.error(
                        f"Backend Error {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Backend not running on port 8000"
                )

            except Exception as e:

                st.exception(e)


# Footer
st.divider()

st.caption(
    "SystemDesign-Pro AI | Multi-Agent + RAG"
)
