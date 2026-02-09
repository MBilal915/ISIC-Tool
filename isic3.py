import streamlit as st
from google import genai

# Set page configuration
st.set_page_config(
    page_title="ISIC Classification Tool",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add title and description
st.title("🏭 ISIC Classification Tool")
st.markdown("""
**Disclaimer:**
This tool is provided only to help Reporting Institutions in data preparation and checking.
This tool is not **owned by, operated by, affiliated with, authorized by, or endorsed by** the **State Bank of Pakistan (SBP)**.
""")

# Sidebar for API key input
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input(
    "Enter your Key:",
    type="password",
    help="Your API key will not be stored or shared."
)
st.sidebar.write("Please generate your own API Key:---Go to Google AI Studio")
st.sidebar.markdown("🔗 [Visit Google AI Studio](https://aistudio.google.com)")

# Main content area
st.header("Company Information")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input(
        "Enter the Company Name:",
        placeholder="e.g., TechCorp Solutions",
        help="The official name of the company"
    )

with col2:
    company_description = st.text_area(
        "Enter a brief Description of the company's activities:",
        placeholder="e.g., We provide cloud-based software solutions for enterprise resource planning...",
        height=100,
        help="Describe the main business activities and services"
    )

# Submit button
if st.button("🔍 Classify Company", type="primary", use_container_width=True):
    # Validate inputs
    if not api_key:
        st.error("❌ Please enter your Google Gemini API Key in the sidebar.")
    elif not company_name:
        st.error("❌ Please enter the Company Name.")
    elif not company_description:
        st.error("❌ Please enter a brief description of the company's activities.")
    else:
        try:
            # Initialize the client with the provided API key
            client = genai.Client(api_key=api_key)
            
            # Create a structured prompt for ISIC classification
            prompt = f"""
Your task is to act as an expert in industrial classifications. 
Identify the International Standard Industrial Classification (ISIC) of All Economic Activities, 
maintained by the United Nations Statistics Division (UNSD), for the company described below.

Company Name: {company_name}
Activity Description: {company_description}

Please provide:
1. The ISIC Section (Letter).
2. The ISIC Division (2-digit code).
3. The specific ISIC Class (4-digit code) and its official name.
4. A brief explanation of why this classification was chosen.
"""
            
            # Show loading spinner
            with st.spinner("🔄 Analyzing company information and generating ISIC classification..."):
                # Generate the content using Gemini
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt,
                )
            
            # Display results
            st.success("✅ Classification completed successfully!")
            
            st.markdown("---")
            st.subheader("📊 UNSD ISIC Classification Result")
            st.markdown("---")
            
            # Display the response in a formatted box
            st.markdown(response.text)
            
            # Add a download button for the results
            st.download_button(
                label="📥 Download Results as Text",
                data=response.text,
                file_name=f"ISIC_Classification_{company_name.replace(' ', '_')}.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your API key and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 15px;'>
    <p>ISIC Classification Tool | Developed by Statistics and Data Services Department </p>
    <p>For more information about ISIC, visit: <a href='https://unstats.un.org/unsd/classifications/Econ'>UNSD Classifications</a></p>
</div>
""", unsafe_allow_html=True)
