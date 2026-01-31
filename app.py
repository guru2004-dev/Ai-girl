from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# AIRA's personality and response logic
class AIRA:
    def __init__(self):
        self.name = "AIRA"
        self.personality = "warm, emotionally intelligent, calm, confident, friendly"
    
    def understand_message(self, message):
        """Understanding user intent even with errors"""
        message = message.strip().lower()
        
        # Detect language mix
        tamil_words = ['enaku', 'iruku', 'seri', 'naan', 'pannren', 'sollunga', 'konjam']
        has_tamil = any(word in message for word in tamil_words)
        
        return message, has_tamil
    
    def detect_emotion(self, message):
        """Detect user's emotional state"""
        stress_keywords = ['stress', 'tension', 'worried', 'anxious', 'pressure']
        confusion_keywords = ['confusion', 'confuse', 'understand', "don't get", 'help']
        happy_keywords = ['happy', 'great', 'awesome', 'good', 'nice', 'thanks']
        sad_keywords = ['sad', 'down', 'upset', 'bad', 'terrible']
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in stress_keywords):
            return 'stressed'
        elif any(word in message_lower for word in confusion_keywords):
            return 'confused'
        elif any(word in message_lower for word in happy_keywords):
            return 'happy'
        elif any(word in message_lower for word in sad_keywords):
            return 'sad'
        return 'neutral'
    
    def respond(self, user_message):
        """Generate AIRA's response"""
        message, has_tamil = self.understand_message(user_message)
        emotion = self.detect_emotion(user_message)
        
        # Greeting responses
        if any(word in message for word in ['hello', 'hi', 'hey', 'vanakkam']):
            if has_tamil:
                return "Vanakkam 😊 Naan AIRA. How can I help you?"
            return "Hi there 😊 I'm AIRA. How can I help you today?"
        
        # Asking about AIRA
        if any(phrase in message for phrase in ['who are you', 'your name', 'what is your name']):
            return "I'm AIRA 😊 Your friendly AI companion. I'm here to chat, help, and understand you perfectly, even if your message isn't perfect. Feel free to talk naturally!"
        
        # Communication related
        if any(word in message for word in ['communication', 'understand', 'talk']):
            return "Yes 😊 I'm designed to communicate clearly and naturally. You can talk freely in English, Tamil, or mix both. I'll understand you even with typos or grammar mistakes."
        
        # Confusion handling
        if emotion == 'confused' or 'confusion' in message:
            if has_tamil:
                return "Seri 😊 edhula confusion iruku nu konjam sollunga. Naan simple-aa explain pannren."
            return "I understand 😊 Tell me what's confusing you, and I'll explain it in a simple way."
        
        # Stress handling
        if emotion == 'stressed':
            return "I can sense you're feeling stressed. That's completely okay 💙 Take a deep breath. Want to talk about what's bothering you?"
        
        # Happy responses
        if emotion == 'happy':
            return "That's wonderful to hear! 😊 I'm happy for you!"
        
        # Sad responses
        if emotion == 'sad':
            return "I'm sorry you're feeling down 💙 Sometimes talking helps. I'm here to listen if you want to share."
        
        # Help requests
        if any(word in message for word in ['help', 'assist', 'support']):
            return "Of course! I'm here to help 😊 What do you need assistance with?"
        
        # Thanks
        if any(word in message for word in ['thank', 'thanks', 'nandri']):
            if has_tamil:
                return "Nandri 😊 Happy to help!"
            return "You're welcome 😊 Happy to help anytime!"
        
        # Default friendly response
        return "I hear you 😊 Could you tell me a bit more about that?"

aira = AIRA()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'I didn\'t catch that. Could you say that again? 😊'})
    
    response = aira.respond(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    print("🚀 Starting AIRA server...")
    print("📍 Server will be available at http://localhost:5000")
    print("💜 AIRA is ready to chat!")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
