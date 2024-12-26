# this file is for testing please refer App1.py
import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configure API Key (secure the key using environment variables in a real app)
GOOGLE_API_KEY = "YOUR_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Function to create sidebar
def create_sidebar():
    st.sidebar.title("🤖 MENU 🤖")
    
    # Menu options
    menu_option = st.sidebar.radio("Navigation", [
        "Query Generator", 
        "Query Library", 
        "Help & Documentation",
        "Settings", 
        "About & Copyright"
    ])

    # Additional sidebar elements based on selected menu
    if menu_option == "Query Library":
        st.sidebar.subheader("Saved Queries")
        # Placeholder for saved queries functionality
        st.sidebar.write("No saved queries yet.")
        st.sidebar.button("Create New Library")

    elif menu_option == "Help & Documentation":
        st.sidebar.subheader("Quick Help")
        st.sidebar.markdown("""
        ### How to Use
        - Enter a natural language description
        - Click "Generate SQL Query"
        - Review generated query and explanation
        
        ### Tips
        - Be specific in your query description
        - Use clear, concise language
        - Mention specific tables or columns if known
        """)

    elif menu_option == "About & Copyright":
        # Developer and Copyright Information
        st.sidebar.markdown("""
        ### 🖥️ Developer Information
        **Developer:** Prajwal c Rathod
        **Contact:** prajwalcs4545@gmail.com
        **GitHub:** https://github.com/Prajwal-Rathod
        
        ### 🌐 Project Details
        **Version:** 1.0.0
        **Created:** December 2024
        
        ### 📝 Copyright Information
        """)
        
        # Dynamic copyright year
        current_year = datetime.now().year
        st.sidebar.markdown(f"""
        © {current_year} SQL Query Generator
        
        ### 🔒 License
        **MIT License**
        
        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files, to use, copy, modify,
        merge, publish, distribute, sublicense, and/or sell copies of the software.
        
        ### 🤝 Contributions
        Open-source contributions are welcome!
        [Contribution Guidelines]
        
        ### 🛡️ Disclaimer
        - AI-generated queries should be reviewed
        - Not responsible for any database errors
        - Use at your own discretion
        """)

    elif menu_option == "Settings":
        st.sidebar.subheader("Application Settings")
        # AI Model Selection
        model_select = st.sidebar.selectbox("AI Model", [
            "Gemini Pro", 
            "Gemini Pro Vision", 
            "Custom Model"
        ])
        
        # Theme Selection
        theme_select = st.sidebar.selectbox("UI Theme", [
            "Dark Mode", 
            "Light Mode", 
            "System Default"
        ])
        
        # Additional settings
        st.sidebar.checkbox("Save Generated Queries")
        st.sidebar.checkbox("Enable Detailed Explanations")

    return menu_option

def main():
    # Page Configuration
    st.set_page_config(
        page_title="SQL Query Generator", 
        page_icon=":robot:",
        layout="wide"
    )

    # Custom CSS for Dark Mode
    st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    .sidebar .sidebar-content {
        background-color: #1e1e1e;
    }
    .main-container {
        background-color: #1e1e1e;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(255,255,255,0.1);
        border: 1px solid #333;
    }
    /* Previous CSS remains the same */
    </style>
    """, unsafe_allow_html=True)

    # Create sidebar and get selected menu option
    selected_menu = create_sidebar()

    # Main Content Area
    if selected_menu == "Query Generator":
        # Main Container
        st.markdown('<div class="main-container">', unsafe_allow_html=True)

        # Title
        st.markdown('<h1 class="main-title">🤖 SQL Query Generator</h1>', unsafe_allow_html=True)

        # Input for query description
        text_input = st.text_input(
            "Describe your desired SQL query:", 
            placeholder="e.g., Select top 5 customers with highest total purchase amount"
        )

        # Generate Query Button
        if st.button("Generate SQL Query"):
            if text_input.strip():
                with st.spinner("Generating your query..."):
                    # Template for generating SQL query
                    query_template = f"""
                    Create an SQL query snippet based on the following description:
                    '{text_input}'
                    Please provide only the SQL query without additional explanations.
                    """

                    # Template for generating explanation
                    explanation_template = f"""
                    Provide a detailed explanation of an SQL query for the following description:
                    '{text_input}'
                    Break down the query's purpose, each clause, and its significance in a clear, educational manner.
                    """

                    try:
                        # Generate SQL query
                        query_response = model.generate_content(query_template)
                        sql_query = query_response.text

                        # Generate explanation
                        explanation_response = model.generate_content(explanation_template)
                        sql_explanation = explanation_response.text

                        # Display results in styled containers
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.code(sql_query, language='sql')
                        st.markdown('</div>', unsafe_allow_html=True)

                        # Display explanation
                        st.markdown('<div class="explanation-box">', unsafe_allow_html=True)
                        st.markdown("### 🔍 Query Explanation")
                        st.markdown(sql_explanation)
                        st.markdown('</div>', unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a description for the SQL query.")

        # Close main container
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
