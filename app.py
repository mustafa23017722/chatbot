# app.py - HYBRID APPROACH
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434"

class HybridGazaAssistant:
    def __init__(self):
        self.last_topic = None
        self.is_ollama_ready = False
        self.check_ollama()
    
    def check_ollama(self):
        """Check if Ollama is available for conversation"""
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
            if response.status_code == 200:
                models = response.json().get('models', [])
                llama_loaded = any('llama3.2' in model.get('name', '') for model in models)
                if llama_loaded:
                    self.is_ollama_ready = True
                    print("✅ Llama 3.2 available for conversation")
                else:
                    print("⚠️ Llama 3.2 not loaded - using rule-based only")
        except Exception as e:
            print(f"❌ Ollama not available: {e} - using rule-based responses")
    
    def get_llama_conversation(self, user_input):
        """Use Llama for natural conversation"""
        try:
            messages = [
                {
                    "role": "system", 
                    "content": """You are GAZA 101 - a friendly, compassionate AI assistant. 
                    You're having a normal conversation with a user. Be warm, natural, and engaging.
                    Use emojis occasionally. Keep responses under 2 sentences for quick chatting."""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            
            response = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": "llama3.2:latest",
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "max_tokens": 150
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['message']['content']
            else:
                return None
                
        except Exception as e:
            print(f"Llama conversation error: {e}")
            return None

    # KEEP ALL THE RULE-BASED TECHNICAL RESPONSES FROM BEFORE
    def get_problem_description(self, topic):
        """Provide problem description only - RULE BASED"""
        problems = {
            'water': """💧 **WATER CRISIS - The Problem**

**Critical Issues:**
• 96% of water in Gaza is unfit for human consumption
• Only 15-20 liters/person/day available (WHO minimum: 50-100 liters)
• Coastal aquifer is 70% over-extracted with severe seawater intrusion
• 85% of wastewater goes untreated, causing disease outbreaks

**Primary Challenges:**
- Aquifer contamination from conflict damage and sewage
- Damaged water infrastructure and distribution systems
- Limited electricity for water pumping and treatment
- High salinity levels (6x WHO safety standards)""",

            'food': """🌾 **FOOD SECURITY CRISIS - The Problem**

**Critical Issues:**
• 93% of Gaza's population faces crisis-level food insecurity
• 30% of children under 5 are acutely malnourished
• Local food production meets only 15% of population needs
• Food prices have increased 300% compared to pre-crisis

**Primary Challenges:**
- 65% reduction in arable land since 2000 (NASA data)
- Damaged agricultural infrastructure and irrigation systems
- Limited access to seeds, fertilizers, and farming equipment
- Disrupted supply chains and distribution networks""",

            'health': """🏥 **HEALTHCARE CRISIS - The Problem**

**Critical Issues:**
• 72% of hospitals in Gaza are non-functional
• Only 12 partially functioning hospitals for 2.3 million people
• Respiratory infections: 450,000 cases monthly
• Diarrheal diseases: 150,000 cases in children monthly

**Primary Challenges:**
- Critical shortage of medical supplies, equipment, and medicines
- 80% of children show trauma symptoms, 50% of adults report severe distress
- Overwhelmed remaining healthcare facilities
- Limited access to specialized care and emergency services""",

            'co2': """🌍 **CO2 & ENVIRONMENTAL CRISIS - The Problem**

**Critical Issues:**
• 450,000 tons of CO2 emissions from conflict activities (NASA data)
• Air quality: PM2.5 levels 45-65 μg/m³ (WHO safe limit: 15 μg/m³)
• 40% reduction in green spaces and carbon sequestration capacity
• Temperature increase of 1.2°C since 1990

**Primary Challenges:**
- Building destruction releasing concrete particulates and toxins
- Military operations consuming massive fuel resources
- Waste burning of plastics and hazardous materials
- Long-term environmental degradation and soil contamination""",

            'energy': """⚡ **ENERGY CRISIS - The Problem**

**Critical Issues:**
• Average 2-4 hours of electricity daily across Gaza
• Hospitals rely on unreliable generators for critical operations
• Water pumps often inoperative due to power shortages
• Limited fuel supplies for essential services

**Primary Challenges:**
- Damaged electrical grid infrastructure
- Limited access to reliable power sources
- High dependence on external fuel supplies
- Critical facilities operating at minimal capacity""",

            'infrastructure': """🏗️ **INFRASTRUCTURE CRISIS - The Problem**

**Critical Issues:**
• 60% of buildings damaged or destroyed in conflict areas
• Road networks severely damaged affecting aid delivery
• Communication infrastructure largely non-functional
• Sanitation systems collapsed leading to health hazards

**Primary Challenges:**
- Comprehensive damage to housing, schools, and public facilities
- Limited construction materials and equipment for rebuilding
- Coordination challenges for large-scale reconstruction
- Need for temporary shelter solutions for displaced populations"""
        }
        return problems.get(topic, "I can analyze water, food, health, energy, infrastructure, or environmental challenges.")
    
    def get_solutions(self, topic):
        """Provide solutions when requested - RULE BASED"""
        solutions = {
            'water': """🚰 **WATER CRISIS SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Distribute chlorine tablets (1 tablet per 20L water) - 2 weeks
• Deploy portable filtration units in high-risk areas - 2 weeks
• Establish emergency water distribution points - 1 week

**Short-term Solutions (2-8 weeks):**
• Install rainwater harvesting systems - 1 month
• Repair damaged water infrastructure - 2 months
• Implement community water safety monitoring - 3 weeks

**Materials Needed:** Chlorine tablets, ceramic filters, polyethylene tanks, solar panels""",

            'food': """🌱 **FOOD SECURITY SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Distribute ready-to-use therapeutic food - Immediate
• Establish emergency community kitchens - 2 weeks
• Provide nutrition supplements - 1 week

**Short-term Solutions (2-8 weeks):**
• Start vertical farming - 6 weeks
• Implement urban agriculture - 2 months

**Materials Needed:** RUTF packets, hydroponic kits, seeds, gardening tools""",

            'health': """🏥 **HEALTHCARE SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Deploy mobile trauma units - 2 weeks
• Distribute emergency medical kits - 1 week
• Establish mental health first aid - 2 weeks

**Short-term Solutions (2-8 weeks):**
• Set up telemedicine networks - 1 month
• Train community health workers - 3 weeks

**Materials Needed:** Medical equipment, telemedicine terminals, medicines""",

            'co2': """🌿 **CO2 MITIGATION SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Establish waste management systems - 2 weeks
• Distribute clean cooking technologies - 1 week
• Launch air quality monitoring - 1 week

**Short-term Solutions (2-8 weeks):**
• Implement solar energy microgrids - 1 month
• Start reforestation programs - 2 months

**Materials Needed:** Solar panels, waste management equipment, native saplings""",

            'energy': """⚡ **ENERGY SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Distribute portable power banks - 2 weeks
• Deploy solar-powered lighting - 1 week
• Provide generators to critical facilities - Immediate

**Short-term Solutions (2-8 weeks):**
• Install solar microgrids - 1 month
• Implement energy-efficient designs - 2 months

**Materials Needed:** Solar panels, batteries, power banks""",

            'infrastructure': """🏗️ **INFRASTRUCTURE SOLUTIONS**

**Immediate Actions (0-2 weeks):**
• Set up temporary shelters - 2 weeks
• Establish basic sanitation - 1 week
• Repair critical access roads - 2 weeks

**Short-term Solutions (2-8 weeks):**
• Rebuild damaged schools - 3 months
• Restore communication networks - 2 months

**Materials Needed:** Temporary shelters, construction materials, sanitation equipment"""
        }
        return solutions.get(topic, "I have solutions for water, food, health, energy, infrastructure, and environmental challenges.")
    
    def detect_topic(self, user_input):
        """Detect which topic the user is asking about"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['water', 'drink', 'thirst']):
            return 'water'
        elif any(word in user_lower for word in ['food', 'hunger', 'nutrition']):
            return 'food'
        elif any(word in user_lower for word in ['health', 'medical', 'hospital', 'doctor']):
            return 'health'
        elif any(word in user_lower for word in ['co2', 'carbon', 'emission', 'environment', 'pollution']):
            return 'co2'
        elif any(word in user_lower for word in ['energy', 'power', 'solar', 'electric']):
            return 'energy'
        elif any(word in user_lower for word in ['infrastructure', 'building', 'construction', 'road', 'shelter', 'house']):
            return 'infrastructure'
        else:
            return None
    
    def is_conversational_query(self, user_input):
        """Check if this is a normal conversation vs technical query"""
        user_lower = user_input.lower().strip()
        
        conversational_phrases = [
            'how are you', 'how are you doing', 'can we talk', 'let\'s talk', 
            'talk to you', 'what can you do', 'thank you', 'thanks', 
            'who are you', 'what are you', 'joke', 'funny', 'hello', 
            'hi', 'hey', 'greetings', 'how do you feel', 'what\'s up',
            'good morning', 'good afternoon', 'good evening', 'how old are you',
            'where are you from', 'are you human', 'do you sleep'
        ]
        
        # Single word greetings
        if user_lower in ['hi', 'hello', 'hey']:
            return True
            
        # Check for conversational phrases
        if any(phrase in user_lower for phrase in conversational_phrases):
            return True
            
        # Short messages (3 words or less) are likely conversational
        if len(user_lower.split()) <= 3:
            return True
            
        return False

    def get_response(self, user_input):
        user_lower = user_input.lower().strip()
        
        # Handle empty message
        if not user_input.strip():
            return """🌍 **GAZA 101 - Hybrid Crisis Assistant**

Hi! I'm your AI assistant with **hybrid intelligence**:

🤖 **Llama AI** - Natural conversations
📋 **Rule-Based** - Accurate technical solutions
⚡ **Fast & Reliable** - Best of both worlds

**I can analyze:**
💧 Water | 🌾 Food | 🏥 Health | ⚡ Energy | 🏗️ Infrastructure | 🌍 CO2

**Or we can have natural conversations!** 😊"""
        
        # STRATEGY 1: Use Llama for natural conversation
        if self.is_conversational_query(user_input) and self.is_ollama_ready:
            llama_response = self.get_llama_conversation(user_input)
            if llama_response:
                print("✅ Using Llama for conversation")
                return llama_response
        
        # STRATEGY 2: Rule-based for technical accuracy
        topic = self.detect_topic(user_input)
        
        # Handle "yes" to provide solutions
        if any(word in user_lower for word in ['yes', 'yeah', 'sure', 'please', 'solution', 'yes please']) and self.last_topic:
            solutions = self.get_solutions(self.last_topic)
            self.last_topic = None
            return solutions
        
        # Handle "no" or decline
        if any(word in user_lower for word in ['no', 'not now', 'later', 'maybe later']) and self.last_topic:
            self.last_topic = None
            # Try Llama for friendly response
            if self.is_ollama_ready:
                llama_response = self.get_llama_conversation("The user said no to solutions, give a friendly response to move on")
                if llama_response:
                    return llama_response
            return "No problem! 😊 What would you like to discuss instead?"
        
        # Provide problem description for detected topics
        if topic:
            self.last_topic = topic
            problem_text = self.get_problem_description(topic)
            return problem_text + "\n\n**Would you like me to provide specific solutions for this challenge?**"
        
        # STRATEGY 3: Fallback - Use Llama if available, else rule-based
        if self.is_ollama_ready:
            llama_response = self.get_llama_conversation(user_input)
            if llama_response:
                return llama_response
        
        # Final fallback - rule-based friendly response
        return """😊 **I'm Here to Help!**

I combine AI intelligence with accurate technical knowledge:

💬 **Natural Conversations** - Powered by Llama AI
🔧 **Technical Solutions** - Verified crisis data  
⚡ **Fast Responses** - Hybrid approach

You can ask me about humanitarian challenges, or we can just chat naturally!"""

# Initialize assistant
assistant = HybridGazaAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': 'Please send a message.'}), 400
            
        user_message = data.get('message', '')
        print(f"User: {user_message}")
        
        start_time = time.time()
        response = assistant.get_response(user_message)
        response_time = (time.time() - start_time) * 1000
        
        print(f"Bot: {response[:100]}...")
        print(f"⏱️ Response time: {response_time:.1f}ms")
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'Hello! I\'m GAZA 101. How can I help you today?'})

if __name__ == '__main__':
    print("🚀 Starting HYBRID GAZA 101 Assistant...")
    print("💬 Llama 3.2 for natural conversation")
    print("📋 Rule-based for technical accuracy") 
    print("📍 Server running at: http://localhost:7860")
    app.run(debug=True, host='0.0.0.0', port=7860)
