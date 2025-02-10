# SQL Query Generator with Google Generative AI

This project is a **SQL Query Generator** web app built using **Streamlit** and **Google Generative AI**. It helps users generate SQL queries based on their descriptions. The app allows users to enter a query description, and it returns the corresponding SQL query with an explanation.

## Features
- Input a natural language description of the query.
- Generate SQL queries using Google Generative AI.
- Display the generated SQL query.
- Easy to use with a simple web interface.


## Testing the repo contains the app.py which is for testing 
## The main file is App1.py  which has the complete FOSS 
## Requirements

To run this project, you need to have the following Python libraries installed:

- **Streamlit**: To create the web app.
- **google-generativeai**: To interact with Google’s Generative AI API for generating SQL queries.

- 

You can install the necessary dependencies by running the following:


pip install streamlit google-generativeai

Setup
Obtain Google Cloud API Key:

You need to get a Google Cloud API key to access Google’s Generative AI service. You can get the key from the Google Cloud Console.
Ensure that Generative AI or Vertex AI API is enabled for your Google Cloud project.
Configure the API Key:

Once you have the API key, replace the GOOGLE_API_KEY in the app.py file with your API key.
python
Copy code
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
Run the Streamlit Application:

After setting up the API key, run the app with the following command:
bash
Copy code
streamlit run app.py
Access the Application:

After running the app, you can access it by opening the URL provided by Streamlit in your terminal (usually http://localhost:8501).
Usage
Enter Description:
Enter a description of the SQL query you want to generate in the input field.
Generate Query:
Click the "Generate Query" button, and the app will use Google’s Generative AI to create a corresponding SQL query.
View the SQL Query:
The app will display the generated SQL query below the input form.
Example
Input:
sql
Copy code
Select all records from a table named "employees" where age is greater than 30.
Generated SQL Query:
sql
Copy code
SELECT * FROM employees WHERE age > 30;
Troubleshooting
404 Error
If you encounter a 404 error, it might be due to:
Invalid or missing API key.
The Generative AI API is not enabled in your Google Cloud project.
Make sure the endpoint is correctly set and your API key has the necessary permissions.
Model Not Found or Errors in Generation
Ensure you're using the correct model ID, which is "models/text-bison-001" in this case. Refer to the Google Generative AI documentation for more details about available models.
Ensure Dependencies are Installed
If you face issues related to missing dependencies, make sure to run:

bash
Copy code
pip install -r requirements.txt
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Streamlit: For creating an easy-to-use framework for building web apps.
Google Generative AI: For providing the powerful AI model that enables natural language SQL query generation.
Google Cloud: For providing the cloud platform and API services.
Contributors: [Your name or other contributors].
Contact
For any inquiries or issues, feel free to reach out via email at [prajwalsc4545@gmail.com].

markdown
Copy code

### Key Points:
1. **Replace the API Key**: Make sure to replace the placeholder `"YOUR_GOOGLE_API_KEY"` with your actual API key.
2. **Setup Instructions**: Instructions on setting up the API and running the app locally.
3. **Example**: A clear example to demonstrate how users can input a description and generate a SQL query.
4. **Troubleshooting**: Tips to help resolve common issues, including 404 errors and API key configuration problems.
5. **License**: A section for the MIT license or your preferred license.




