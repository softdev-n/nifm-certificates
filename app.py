import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NIFM Certificate Portal", page_icon="🎓")

st.title("🎓 NIFM Certificate Download Portal")
st.write("Please enter your Employee ID below to securely download your certificate.")
st.markdown("---")


@st.cache_data
def load_data():
    df = pd.read_csv("employees.csv")
    df.columns = df.columns.str.strip()
    
    # FIX: Clean the data immediately when loading so it matches perfectly
    # 1. Convert ID to string, remove any '.0' that pandas might add, and remove spaces
    df['employee_id'] = df['employee_id'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    return df

df = load_data()


with st.form("download_form"):
    user_id = st.text_input("Employee ID")
    
    submit_button = st.form_submit_button("Download Certificate")

if submit_button:
    user_id = user_id.strip()
    
    # Match ID only (Email logic removed)
    match = df[df['employee_id'] == user_id]
    
    if not match.empty:
        st.success("✅ Record matched! Your certificate is ready.")
        
        
        raw_name = str(match.iloc[0]['employee_name']).strip()
        name_parts = raw_name.split()
        
        if len(name_parts) > 2:
            employee_name = f"{name_parts[0]} {name_parts[-1]}"
        else:
            employee_name = raw_name
            
        safe_name = employee_name.replace("/", "-")
        
        
        pdf_path = f"output_certificates/{user_id}_{safe_name}.pdf"
        
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Click Here to Download Your Certificate",
                    data=pdf_file,
                    file_name=f"{employee_name}_Certificate.pdf",
                    mime="application/pdf",
                    type="primary"
                )
            st.info(f"🔒 **Note:** Your PDF is securely locked. The password to open it is your Employee ID: **{user_id}**")
        else:
            st.error("⚠️ Your certificate was not found on the server. Please contact HR.")
    else:
        st.error("❌ Invalid Employee ID. Please try again.")