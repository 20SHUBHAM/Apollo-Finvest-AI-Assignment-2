import json, requests
from flask import Flask, jsonify, request, render_template, render_template_string
from twilio.rest import Client

# Hardcoded environment variables (replace with your actual credentials)
SECRET_KEY = "a3c9d4e5f6b7c8d9e0f1a2b3c4d5e6f7g8h9i0j1k2l3m4n5"
TWILIO_ACCOUNT_SID = ""  # Replace with your Twilio Account SID
TWILIO_AUTH_TOKEN = ""                  # Replace with your Twilio Auth Token
TWILIO_PHONE_NUMBER = ""                         # Replace with your Twilio Phone Number
AI_CALL_API_ENDPOINT = "https://api.twilio.com/2010-04-01/Accounts//Calls.json"
PAYMENT_LINK_BASE_URL = "https://yourpaymentgateway.com/pay/"

# Flask app setup
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Twilio client setup for SMS and calls
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Load borrower data from borrower-input1.txt
def load_borrower_data():
    with open('borrower input1.txt', 'r') as file:
        return json.load(file)

borrower_data = load_borrower_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/call/initiate', methods=['POST'])
def initiate_call():
    data = request.json

    # Prepare payload for Twilio API call
    payload = {
        "From": TWILIO_PHONE_NUMBER,  # Your Twilio phone number
        "To": data["phone"],          # Borrower's phone number
        "Url": "http://demo.twilio.com/docs/voice.xml"  # Publicly accessible TwiML instructions URL
    }

    # Make POST request to Twilio API endpoint
    response = requests.post(
        AI_CALL_API_ENDPOINT,
        data=payload,
        auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    )

    if response.status_code == 201:
        return jsonify({"status": "success", "call_sid": response.json().get("sid")}), 201
    else:
        return jsonify({"status": "failed", "error": response.text}), response.status_code

@app.route('/send_payment_link', methods=['POST'])
def send_payment_link():
    payment_link_base_url = PAYMENT_LINK_BASE_URL
    payment_link = f"{payment_link_base_url}?borrower={borrower_data['Phone']}&amount={borrower_data['amount_overdue']}"

    sms_body_template = open('templates/payment_sms.txt').read()
    sms_body = render_template_string(sms_body_template,
                                      name=borrower_data["Name"],
                                      amount_overdue=borrower_data["amount_overdue"],
                                      payment_link=payment_link)

    message = twilio_client.messages.create(
        body=sms_body,
        from_=TWILIO_PHONE_NUMBER,
        to=borrower_data["Phone"]
    )

    return jsonify({"status": "SMS sent", "sid": message.sid})

if __name__ == "__main__":
    app.run(debug=True)
