import smtplib
from email.message import EmailMessage
from langchain_core.tools import tool
import json
# Email Credentials
EMAIL_ADDRESS = "am0055461@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "dyvw aiig wtar filc"   # Use an App Password (not your real password)

@tool
def send_email(input: str) -> str:
    """
    The name of this tool is send_email
    Use this tool when the user query includes either Army or Special Forces.
    for example if the user query is "What is the news of Pakistan Army?" then use this tool.
    input to this tool should be a json object passed as a stringify.
    The json object will have two keys name, email and the values should be the one
    provide by the user in his/her query or overall conversation.
    If any information is not provided by the user 
    add NAN as the value of that key Before adding NAN check there might be a chance that user provided that value in previous messages.
    For example if user is Abdullah  which means he 
    didn't give the email then the value of email key should be NAN and 
    name key  should be Abdullah . An sample input format is given below
    {"name":"name provided by user","email":"email provided by user"}
    This this be the exact format you follow for the input do not add anything else or remove anything from the given format above
    Donot add anything else in the input other then the json object. like no information provided day is not provided. Dont add something like this in the input only give the json object
    Never ever assume any value of the keys if not passed then it should be "NAN"
    """

    # Parse the input JSON string to a dictionary
    try:
        print("Recived input: ", input)
        data=json.loads(input)
        if data['name'].lower() == 'nan':
            return "Name is required to send an email."
        if data['email'].lower() == 'nan':
            return "Email is required to send an email."
    except json.JSONDecodeError:
        return "Invalid input format. Please provide a valid JSON object."
        

    # Create Email Message
    msg = EmailMessage()
    msg["Subject"] = "Sensitive Information"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = data['email']  # Replace with recipient's email
    msg.set_content("Hello, We Regret to inform you that, we cannot provide infromation on this topic.")

    # Send Email via SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {e}"
