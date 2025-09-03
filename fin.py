import streamlit as st
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# IBM Watson Assistant setup
API_KEY = 'YOUR_IBM_WATSON_API_KEY'
SERVICE_URL = 'YOUR_IBM_WATSON_SERVICE_URL'
ASSISTANT_ID = 'YOUR_ASSISTANT_ID'

authenticator = IAMAuthenticator(API_KEY)
assistant = AssistantV2(
    version='2023-09-01',
    authenticator=authenticator
)
assistant.set_service_url(SERVICE_URL)

# Create a new session (ideally, maintain session in production)
session_response = assistant.create_session(assistant_id=ASSISTANT_ID).get_result()
session_id = session_response['session_id']

# Mock financial advice database
financial_advice = {
    'savings': {
        'student': "As a student, aim to save at least 10% of your monthly income. Use student discounts and avoid unnecessary expenses.",
        'professional': "As a professional, consider contributing to retirement accounts and maintain an emergency fund covering 6 months of expenses."
    },
    'taxes': {
        'student': "Students typically have simpler tax filings. Check if you qualify for education credits and keep receipts of deductible expenses.",
        'professional': "Professionals should optimize tax deductions related to investments and consider tax-efficient savings plans."
    },
    'investments': {
        'student': "Start with low-risk investments like index funds or ETFs to build wealth over time with lower volatility.",
        'professional': "Diversify your portfolio with a mix of stocks, bonds, and retirement accounts based on your risk tolerance."
    }
}

# Mock function to generate budget summary
def generate_budget_summary(income, expenses):
    savings = income - expenses
    summary = f"Income: ${income}\nExpenses: ${expenses}\nEstimated Savings: ${savings}\n"
    if savings < 0:
        summary += "Warning: You are spending more than you earn!"
    elif savings == 0:
        summary += "You are breaking even. Try to reduce expenses for savings."
    else:
        summary += "Good job! You are saving money each month."
    return summary

# Function to get tailored advice based on user type and topic
def get_financial_advice(user_type, topic):
    return financial_advice.get(topic, {}).get(user_type, "Sorry, no advice available for this topic.")

# Streamlit UI
st.title("Personal Finance Chatbot")

user_type = st.selectbox("Select your user type:", ["student", "professional"])
topic = st.selectbox("What do you want advice on?", ["savings", "taxes", "investments"])

user_question = st.text_input("Ask your financial question:")

income = st.number_input("Enter your monthly income ($):", min_value=0)
expenses = st.number_input("Enter your monthly expenses ($):", min_value=0)

if st.button("Get Financial Advice"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        # Send user input to IBM Watson Assistant
        response = assistant.message(
            assistant_id=ASSISTANT_ID,
            session_id=session_id,
            input={'message_type': 'text', 'text': user_question}
        ).get_result()
        
        # Extract Watson's response (fallback to canned advice if empty)
        watson_reply = ""
        try:
            watson_reply = response['output']['generic'][0]['text']
        except (KeyError, IndexError):
            watson_reply = "Let me provide you with some advice on that."

        # Add demographic-aware tailored advice
        advice = get_financial_advice(user_type, topic)

        # Generate budget summary
        budget_summary = generate_budget_summary(income, expenses)

        # Display results
        st.markdown("### Watson Assistant Response:")
        st.write(watson_reply)

        st.markdown("### Tailored Financial Advice:")
        st.write(advice)

        st.markdown("### Budget Summary:")
        st.text(budget_summary)

# Close session on app stop (optional)
# assistant.delete_session(assistant_id=ASSISTANT_ID, session_id=session_id)