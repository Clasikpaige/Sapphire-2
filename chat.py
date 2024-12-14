import json
import os
import logging
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Bot Responses
RESPONSES = {
    "thank you": "You're welcome! Got more questions? Just drop them in!",
    "goodbye": "Catch you later! Don't be a stranger! 👋",
    "hello": "Yo! How can I help? Ready to find some cool tools?",
    "help": "Need help? Type 'catalog' to explore the tools I got for you!",
    "thanks": "Glad I could help! Anything else? Hit me up!",
    "whats your name?": "I'm Sapphire, your personal assistant. What's up?",
    "how are you?": "I'm doing great, just here to help you out. 😎",
    "bye": "Later, alligator! 👋",
    "purchase": "Time to buy something cool? Go to 'catalog,' and let's get it!",
    "payment": "Once you pick a tool, I’ll give you the Bitcoin address to send the payment manually.",
    "yes": "Sweet, let's do this! What’s next?",
    "no": "No worries! Just let me know what you wanna do.",
    "please": "Always happy to help! What can I do for you?",
    "thank you very much": "No prob! I'm always here for you.",
    "what can I do for you?": "You can grab tools, ask questions, or just chat! 😎",
    "where is the catalog?": "Just type 'catalog,' and I’ll show you the goods.",
    "i want to buy a tool": "Awesome! Go to 'catalog' and pick your weapon of choice.",
    "show me the catalog": "Sure thing! Type 'catalog' and check it out.",
    "can i buy more than one?": "Oh yeah, go ahead! Grab as many as you want!",
    "how do i pay?": "Just send your payment to this Bitcoin address and upload a screenshot or receipt here.",
    "bitcoin payment": "Here’s your address: bc1qnuz0xer03tgrkw7gy5xnacrtuzpv3g8lrr56te. Just send the payment, then send me the receipt!",
    "is my payment confirmed?": "Once I get the receipt, I’ll confirm your payment and send your tool.",
    "i need help with payments": "Gotcha! Send the payment to that Bitcoin address, then send me the receipt. Got it?",
    "sorry": "No need to say sorry! I’m here to help. What’s up?",
    "please help me": "Of course! What’s on your mind?",
    "who created you": "I was created by Paige, a data scientist and hacker. Let me know if you need anything.",
    "thank you for your help": "You’re welcome anytime! Just hit me up if you need anything else.",
    "is this the right tool?": "Not sure? Let me know what you're looking for, and I’ll guide you!",
    "i am confused": "No worries! Drop your question, and I’ll make it clearer.",
    "can i go back?": "Absolutely! Type 'catalog' to go back and pick another tool.",
    "back": "Going back to the catalog now... Get ready to find your next tool!",
    "i changed my mind": "No sweat! What do you wanna do next? Hit me with your choice!",
    "what do i do next?": "Pick a tool, pay with Bitcoin, and then send me your receipt. Easy as that!",
    "continue": "Alright, let’s keep it rolling!",
    "stop": "Stopping now! Let me know if you wanna pick it back up.",
    "cancel": "No problem! Your purchase has been canceled. Feel free to ask anything else.",
    "how can i contact you?": "Just message me here on WhatsApp, and I’m all yours! 💬",
    "order confirmation": "I’ll confirm your order once I get the payment receipt. Don’t worry!",
    "invoice": "After payment, I'll confirm and send you the details of your order.",
    "thank you for choosing us": "It’s been awesome assisting you! Thanks for choosing Sapphire. ✨",
    "i love this bot": "Aww, you're the best! 😍 I'm here whenever you need me.",
    "do you have discounts?": "Stay tuned! Discounts and special offers coming soon. Keep an eye out!",
    "where do i see my order?": "I’ll send you your order details once the payment is confirmed.",
    "i made my payment": "Awesome! Upload your receipt, and I'll confirm it for you.",
    "confirm purchase": "Got your order! Upload your receipt, and I’ll process it.",
    "ready to buy": "Awesome! Let’s make this happen. Go to the catalog to pick your tool!",
    "checkout": "Ready to checkout! Just send the payment and upload the receipt when you’re done.",
    "processing payment": "I’ll process the payment as soon as I get that receipt from you.",
    "order placed": "Order placed! Send me your receipt, and I’ll finalize it.",
    "i'm done": "Thanks for wrapping it up! Let me know if you need anything else. 😎",
}

# Tools Data (JSON)
TOOLS_JSON = [
    {
        "id": "tool1",
        "name": "Phishing Page",
        "description": "A powerful phishlet with active payload to capture login credentials and session cookies.",
        "price": 2500.00,
    },
    {
        "id": "tool2",
        "name": "Keylogger",
        "description": "Keylogger, remote access trojan compiled as .exe, pdf, url.",
        "price": 6000.00,
    },
]

# Helper Function to Match Input
def get_response(input_text: str) -> str:
    """Match input text with the RESPONSES dictionary."""
    sanitized_input = " ".join(input_text.strip().lower().split())
    return RESPONSES.get(sanitized_input, "Sorry, I didn't get that. Type 'help' or 'catalog'.")

# Helper Function to Generate Catalog
def generate_catalog():
    """Create a formatted catalog message from JSON data."""
    message = "📦 *Catalog of Tools:*\n\n"
    for idx, tool in enumerate(TOOLS_JSON, 1):
        message += (
            f"{idx}. *{tool['name']}*\n"
            f"   {tool['description']}\n"
            f"   Price: ${tool['price']:.2f}\n\n"
        )
    message += "To purchase a tool, message me with the tool name and payment details."
    return message

# WhatsApp Webhook Handler
@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming WhatsApp messages from Twilio."""
    incoming_data = request.form
    message_body = incoming_data.get("Body", "").strip()
    from_number = incoming_data.get("From", "")
    
    logger.info(f"Incoming message from {from_number}: {message_body}")
    
    if message_body.lower() == "catalog":
        response_message = generate_catalog()
    else:
        response_message = get_response(message_body)
    
    return jsonify({"message": response_message})

# Main Function
if __name__ == "__main__":
    app.run(debug=True, port=5000)
