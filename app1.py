import streamlit as st
import sqlite3
from datetime import datetime
import google.generativeai as genai
import os

# Configure Streamlit page 
st.set_page_config(
    page_title="SQL Query Generator",
    page_icon=":robot:",
    layout="wide"
)

# Custom CSS for sidebar menu styling
st.markdown("""
<style>
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);
        padding: 2rem 1rem;
        border-right: 1px solid #333;
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    
    /* Sidebar title */
    .css-1d391kg .sidebar-title {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-bottom: 2rem !important;
        text-align: center !important;
    }
    
    /* Radio buttons in sidebar */
    .css-1d391kg .stRadio > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .css-1d391kg .stRadio > div:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        transform: translateX(5px) !important;
    }
    
    /* Radio button labels */
    .css-1d391kg .stRadio label {
        color: white !important;
        font-weight: 500 !important;
        cursor: pointer !important;
    }
    
    /* Selected radio button */
    .css-1d391kg .stRadio [aria-checked="true"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-left: 4px solid #ffffff !important;
    }

    /* Sidebar footer */
    .sidebar-footer {
        margin-top: auto;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }

    .sidebar-footer-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }

    .sidebar-footer-social {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 0.5rem;
    }

    .sidebar-footer-social a {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        transition: all 0.3s ease;
        font-size: 1.2rem;
    }

    .sidebar-footer-social a:hover {
        color: white;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Configure API Key
api_key = st.secrets["general"]["google_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Initialize the database
DB_FILE = "queries.db"

def init_db():
    """Initialize the database and create a table if it doesn't exist."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                query TEXT NOT NULL,
                explanation TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """)
            conn.commit()
    except Exception as e:
        st.error(f"Error initializing database: {e}")

def save_query(description, query, explanation):
    """Save a query, its description, and explanation to the database."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                "INSERT INTO queries (description, query, explanation, timestamp) VALUES (?, ?, ?, ?)", 
                (description, query, explanation, datetime.now())
            )
            conn.commit()
    except Exception as e:
        st.error(f"Error saving query: {e}")

def get_saved_queries():
    """Retrieve all saved queries from the database."""
    try:
        if not os.path.exists(DB_FILE):
            return []

        with sqlite3.connect(DB_FILE) as conn:
            queries = conn.execute(
                "SELECT id, description, query, explanation, timestamp FROM queries"
            ).fetchall()
            return queries
    except sqlite3.OperationalError as e:
        st.error(f"Database error: {e}")
        return []

def delete_query(query_id):
    """Delete a query from the database by ID."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("DELETE FROM queries WHERE id = ?", (query_id,))
            conn.commit()
            st.success("Query deleted successfully!")
    except Exception as e:
        st.error(f"Error deleting query: {e}")

def create_sidebar():
    # Dictionary of menu options and their icons
    menu_options = {
        "Query Generator": "🤖",
        "Query Library": "📚",
        "Help & Documentation": "📖",
        "Settings": "⚙️",
        "About": "ℹ️",
        "Privacy Policy": "🔒",
        "Contact": "📞"
    }
    
    # Create radio buttons with icons
    selected_menu = st.sidebar.radio(
        "Menu",
        list(menu_options.keys()),
        format_func=lambda x: f"{menu_options[x]} {x}"
    )

    # Add footer to sidebar
    st.sidebar.markdown("""
        <div class="sidebar-footer">
            <div class="sidebar-footer-text">
                &copy; 2024 SQL Query Generator<br>
                Developed by Prajwal C Rathod
            </div>
            <div class="sidebar-footer-social">
                <a href="https://github.com/Prajwal-Rathod" target="_blank">
                    <i class="fab fa-github"></i>
                </a>
                <a href="https://www.linkedin.com/in/prajwal-c-s-b7ab07228" target="_blank">
                    <i class="fab fa-linkedin"></i>
                </a>
                <a href="tel:+919606436319">
                    <i class="fas fa-phone"></i>
                </a>
                <a href="mailto:prajwalcs4545@gmail.com">
                    <i class="fas fa-envelope"></i>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    return selected_menu

def main():
    # Get the selected menu option from sidebar
    selected_menu = create_sidebar()

    if "generated_query" not in st.session_state:
        st.session_state["generated_query"] = None
    if "query_explanation" not in st.session_state:
        st.session_state["query_explanation"] = None

    # Initialize Database
    init_db()

    # Main Content Area
    if selected_menu == "Query Generator":
        st.title("🤖 SQL Query Generator")

        # Input for query description
        text_input = st.text_input(
            "Describe your desired SQL query:", 
            placeholder="e.g., Select top 5 customers with highest total purchase amount"
        )

        # Generate Query Button
        if st.button("Generate SQL Query"):
            if text_input.strip():
                with st.spinner("Generating your query..."):
                    query_template = f"""
                    Create an SQL query snippet based on the following description:
                    '{text_input}'
                    Please provide only the SQL query without additional explanations.
                    """
                    explanation_template = f"""
                    Provide a detailed explanation of an SQL query for the following description:
                    '{text_input}'
                    """
                    try:
                        # Generate SQL query
                        query_response = model.generate_content(query_template)
                        st.session_state["generated_query"] = query_response.text

                        # Generate explanation
                        explanation_response = model.generate_content(explanation_template)
                        st.session_state["query_explanation"] = explanation_response.text

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a description for the SQL query.")

        # Display Results
        if st.session_state["generated_query"]:
            st.subheader("Generated SQL Query")
            st.code(st.session_state["generated_query"], language='sql')

        if st.session_state["query_explanation"]:
            st.subheader("Query Explanation")
            st.write(st.session_state["query_explanation"])

        # Save Query Button
        if st.session_state["generated_query"] and st.session_state["query_explanation"]:
            if st.button("Save Query"):
                try:
                    save_query(
                        description=text_input,
                        query=st.session_state["generated_query"],
                        explanation=st.session_state["query_explanation"]
                    )
                    st.success("Query saved successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a description for the SQL query.")

    elif selected_menu == "Query Library":
        st.title("📚 Query Library")
        saved_queries = get_saved_queries()

        if saved_queries:
            for query_id, description, query, explanation, timestamp in saved_queries:
                st.markdown(f"**Query ID:** {query_id}")
                st.markdown(f"**Description:** {description}")
                st.code(query, language='sql')
                st.markdown(f"**Explanation:** {explanation}")
                st.caption(f"Saved on: {timestamp}")

                # Delete Query Button
                if st.button(f"Delete Query {query_id}", key=f"delete_{query_id}"):
                    delete_query(query_id)
                    st.experimental_rerun()  # Refresh the app after deletion
        else:
            st.write("No saved queries found.")

    elif selected_menu == "Help & Documentation":
        st.title("🛠️ Help & Documentation")
        
        # Overview Section
        st.header("📘 Overview")
        st.write("""
        This SQL Query Generator is an AI-powered tool that helps you create SQL queries using natural language descriptions. 
        It simplifies the process of writing SQL queries by converting your plain English descriptions into proper SQL syntax.
        """)
        
        # Features Section
        st.header("🎯 Key Features")
        st.markdown("""
        1. **Query Generation**
           - Enter your query description in plain English
           - Get instant SQL query generation
           - Receive detailed explanations of the generated queries
        
        2. **Query Library**
           - Save generated queries for future reference
           - View all saved queries with their descriptions
           - Delete queries you no longer need
           
        3. **AI-Powered**
           - Powered by Google's Gemini Pro AI model
           - Accurate SQL query generation
           - Detailed query explanations
        """)
        
        # How to Use Section
        st.header("📝 How to Use")
        st.markdown("""
        **Query Generator:**
        1. Navigate to the "Query Generator" section
        2. Enter your query description in plain English
        3. Click "Generate SQL Query"
        4. Review the generated SQL query and explanation
        5. Click "Save Query" to store it in the library
        
        **Query Library:**
        1. Go to the "Query Library" section
        2. View all your saved queries
        3. Each query shows:
           - Query ID
           - Description
           - SQL query
           - Explanation
           - Timestamp
        4. Use the delete button to remove unwanted queries
        """)
        
        # Tips Section
        st.header("💡 Tips for Better Results")
        st.markdown("""
        1. Be specific in your query descriptions
        2. Include key information like:
           - Table names (if known)
           - Desired columns
           - Sorting requirements
           - Filtering conditions
        3. Review the explanation to understand the query logic
        4. Save important queries for future reference
        """)
        
        # Support Section
        st.header("🆘 Support")
        st.write("""
        If you encounter any issues or have questions, please contact the development team.
        We're continuously improving the application based on user feedback.
        """)

    elif selected_menu == "Settings":
        st.title("⚙️ Settings")
        
        # AI Model Configuration
        st.header("🤖 AI Model Configuration")
        model_type = st.selectbox(
            "Select AI Model",
            ["Gemini Pro", "Gemini Pro Vision", "Custom Model"],
            help="Choose the AI model for query generation"
        )
        
        if model_type == "Custom Model":
            st.text_input("Custom Model API Key", type="password")
            st.text_input("Custom Model Endpoint URL")
        
        # UI Theme Settings
        st.header("🎨 User Interface")
        theme = st.selectbox(
            "Select Theme",
            ["Dark Mode", "Light Mode", "System Default"],
            help="Choose your preferred UI theme"
        )
        
        # Query Settings
        st.header("📝 Query Settings")
        auto_save = st.checkbox(
            "Auto-save Generated Queries",
            value=True,
            help="Automatically save all generated queries to the library"
        )
        
        detailed_explanations = st.checkbox(
            "Enable Detailed Explanations",
            value=True,
            help="Show comprehensive explanations for generated SQL queries"
        )
        
        # Advanced Settings
        st.header("🔧 Advanced Settings")
        max_tokens = st.slider(
            "Maximum Response Length",
            min_value=100,
            max_value=1000,
            value=500,
            help="Set the maximum length for query explanations"
        )
        
        # Save Settings Button
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")
            # Here you would typically save these settings to a configuration file or database

    elif selected_menu == "About":
        st.title("ℹ️ About")
        
        # Developer Information
        st.header("🖥️ Developer Information")
        st.markdown("""
        **Developer:** Prajwal c Rathod  
        **Contact:** [prajwalcs4545@gmail.com](mailto:prajwalcs4545@gmail.com)  
        **GitHub:** [https://github.com/Prajwal-Rathod](https://github.com/Prajwal-Rathod)
        """)
        
        # Project Details
        st.header("🌐 Project Details")
        st.markdown("""
        **Version:** 1.0.0  
        **Created:** December 2024
        """)
        
        # Copyright Information
        st.header("📝 Copyright Information")
        current_year = datetime.now().year
        st.markdown(f"""
        {current_year} SQL Query Generator
        """)
        
        # License Information
        st.header("🔒 License")
        st.markdown("""
        **MIT License**

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files, to use, copy, modify,
        merge, publish, distribute, sublicense, and/or sell copies of the software.
        """)
        
        # Contributions
        st.header("🤝 Contributions")
        st.markdown("""
        Open-source contributions are welcome!  
        [Contribution Guidelines](https://github.com/Prajwal-Rathod/SQL_Query_Generator/contribute)
        """)
        
        # Disclaimer
        st.header("🛡️ Disclaimer")
        st.markdown("""
        - AI-generated queries should be reviewed before use
        - Not responsible for any database errors
        - Use at your own discretion
        """)

    elif selected_menu == "Privacy Policy":
        st.title("Privacy Policy")
        st.markdown("""
        ## Privacy Policy for SQL Query Generator

        **Last Updated: December 15, 2024**

        ### 1. Introduction
        Welcome to SQL Query Generator. We are committed to protecting your privacy and handling your data with transparency and care.

        ### 2. Information We Collect
        - **Query Data**: The SQL queries you generate
        - **Usage Data**: How you interact with our application
        - **Technical Data**: Browser type, device information

        ### 3. How We Use Your Information
        - To provide and improve our SQL query generation service
        - To maintain and optimize our application
        - To analyze usage patterns and improve user experience

        ### 4. Data Security
        We implement appropriate security measures to protect your information from unauthorized access or disclosure.

        ### 5. Data Retention
        We retain your data only for as long as necessary to provide our services and fulfill the purposes outlined in this policy.

        ### 6. Your Rights
        You have the right to:
        - Access your data
        - Request data deletion
        - Object to data processing
        - Request data correction

        ### 7. Contact Us
        For any privacy-related questions or concerns, please contact us at:
        - Email: prajwalcs4545@gmail.com
        - Phone: +91 9606436319
        """)

    elif selected_menu == "Contact":
        st.title("Contact Information")
        st.markdown("""
        ### Get in Touch

        Feel free to reach out to me for any queries, suggestions, or collaboration opportunities.

        #### Personal Information
        - **Name**: Prajwal C Rathod
        - **Role**: Full Stack Developer
        - **Location**: Bangalore, Karnataka, India

        #### Contact Details
        - **Email**: prajwalcs4545@gmail.com
        - **Phone**: +91 9606436319
        - **GitHub**: [Prajwal-Rathod](https://github.com/Prajwal-Rathod)
        - **LinkedIn**: [Prajwal C Rathod](https://www.linkedin.com/in/prajwal-c-s-b7ab07228)

        #### Professional Summary
        Experienced Full Stack Developer with expertise in:
        - Python Development
        - Web Applications
        - Database Management
        - AI/ML Integration

        Feel free to schedule a call or send an email. I'll get back to you within 24 hours.
        """)

if __name__ == "__main__":
    main()
