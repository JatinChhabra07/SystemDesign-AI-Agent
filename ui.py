import streamlit as st
import requests
import streamlit_mermaid as st_mermaid

st.set_page_config(page_title="SystemDesign-Pro AI", layout="wide")

st.title("🏗️ SystemDesign-Pro: Agentic Architect")
st.markdown("Enter your app idea, and my multi-agent team will research and design the architecture.")

user_input = st.text_input("What system are you building?", "A high-scale Uber clone")

if st.button("Generate Architecture"):
    with st.spinner("Agents are researching and designing..."):
        try:
            response = requests.post(
                "http://localhost:8000/design",
                json={"query": user_input, "thread_id": "session_1"}
            )
  
            
            if response.status_code == 200:
                data = response.json()
                report = data['report']
                
                st.success(f"Project: {data['title']}")
                
                # Split view: Text on left, Diagram on right
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.subheader("Technical Specs")
                    st.markdown(report)
                    
                with col2:
                    st.subheader("Architecture Visual")
                    # Logic to extract Mermaid code between ```mermaid and ```
                    if "```mermaid" in report:
                        mermaid_code = report.split("```mermaid")[1].split("```")[0]
                        st_mermaid.st_mermaid(mermaid_code)
                    else:
                        st.info("No diagram code found in the response.")
                        
                st.download_button(
                    label="Download Architecture Report",
                    data=data['report'],
                    file_name="architecture_design.md",
                    mime="text/markdown"
                ) 
            
        except Exception as e:
            st.error(f"Could not connect to backend: {e}")