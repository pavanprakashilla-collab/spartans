def personal_finance_chatbot():
    print("Welcome to Personal Finance Chatbot!")
    print("I can help you with Savings, Taxes, and Investments.")
    print("Type 'exit' to quit anytime.\n")
    
    while True:
        user_input = input("You: ").lower()
        
        if user_input == "exit":
            print("Chatbot: Goodbye! Stay financially savvy!")
            break
        
        # Savings advice
        if "save" in user_input or "savings" in user_input:
            print("Chatbot: A good rule of thumb is to save at least 20% of your income. "
                  "Start by building an emergency fund of 3-6 months' expenses.")
        
        # Taxes advice
        elif "tax" in user_input or "taxes" in user_input:
            print("Chatbot: To reduce your taxable income, consider contributing to retirement accounts like a 401(k) or IRA. "
                  "Also, keep track of deductible expenses and tax credits.")
        
        # Investment advice
        elif "invest" in user_input or "investment" in user_input:
            print("Chatbot: Diversify your investments to balance risk and reward. "
                  "Consider low-cost index funds or ETFs for long-term growth.")
        
        # General help
        elif "help" in user_input or "advice" in user_input:
            print("Chatbot: I can help you with topics related to savings, taxes, and investments. "
                  "Try asking me something like 'How can I save money?' or 'What are good investment options?'")
        
        else:
            print("Chatbot: Sorry, I didn't understand that. Please ask about savings, taxes, or investments.")
            

if __name__ == "__main__":
    personal_finance_chatbot()
