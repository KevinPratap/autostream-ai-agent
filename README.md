\# AutoStream AI Agent - Social-to-Lead Workflow



A conversational AI agent built with LangGraph that converts social media conversations into qualified business leads for AutoStream, an automated video editing SaaS platform.



\## 🎯 Project Overview



This project implements an intelligent agent that:

\- ✅ Classifies user intent (casual, product inquiry, high-intent)

\- ✅ Retrieves knowledge using RAG from a local knowledge base

\- ✅ Manages conversation state across 5-6 turns

\- ✅ Sequentially collects lead data (name → email → platform)

\- ✅ Executes tool only when all data is collected



\*\*Built for:\*\* ServiceHive Inflx Platform  

\*\*Assignment:\*\* ML Intern - Agentic Workflow



---



\## 🚀 Quick Start



\### Prerequisites

\- Python 3.9+

\- Google Gemini API key (free)



\### Installation

```bash

\# Clone repository

git clone <your-repo-url>

cd autostream-agent



\# Create virtual environment

python -m venv venv

venv\\Scripts\\activate.bat  # Windows

\# source venv/bin/activate  # Mac/Linux



\# Install dependencies

pip install -r requirements.txt



\# Configure API key (for AI version)

echo GOOGLE\_API\_KEY=your-key-here > .env

```



\### Run Agent



\*\*Rule-Based Version (No API needed):\*\*

```bash

python agent\_gemini.py

```



\*\*AI-Powered Version (Requires API key):\*\*

```bash

python agent\_gemini\_ai.py

```



---



\## 🎬 Demo Conversation

```

You: tell me about your pricing



Agent: AutoStream Pricing Plans:

&nbsp;      Basic Plan - $29/month: 10 videos, 720p

&nbsp;      Pro Plan - $79/month: Unlimited videos, 4K, AI captions



You: I want to try the Pro plan for my YouTube channel



Agent: That's great to hear! To get you started, could you please share your name?



You: Kevin Pratap



Agent: Perfect! And what's your email address?



You: kevin@example.com



============================================================

🎯 LEAD CAPTURED SUCCESSFULLY!

============================================================

Name: Kevin Pratap

Email: kevin@example.com

Platform: Youtube

============================================================



Agent: 🎉 Awesome! We've captured your information, Kevin Pratap...

```



---



\## 🏗️ Architecture



\### Why LangGraph?



I chose \*\*LangGraph\*\* for its superior state management and deterministic workflow control:



1\. \*\*Explicit State Graph\*\*: Each node (intent classification, RAG, response generation, tool execution) is clearly defined, making the workflow predictable and debuggable.



2\. \*\*Persistent State\*\*: The `AgentState` maintains conversation history, intent, lead data, and knowledge context across multiple turns without relying on LLM memory.



3\. \*\*Conditional Routing\*\*: Dynamic workflow routing based on state (e.g., "collect more info" vs "execute tool") enables complex conversation flows.



4\. \*\*RAG Integration\*\*: Knowledge retrieval is isolated in a dedicated node, making it easy to swap or enhance the retrieval mechanism.



5\. \*\*Controlled Tool Execution\*\*: The lead capture tool is only triggered when all three fields (name, email, platform) are confirmed present, preventing premature API calls.



\### System Flow

```

User Message → Intent Classification → RAG Retrieval → Response Generation

&nbsp;                                                              ↓

&nbsp;                                                   Check State Conditions

&nbsp;                                                      ↙           ↘

&nbsp;                                             Execute Tool    Return Response

&nbsp;                                                  ↓

&nbsp;                                             Reset State

```



---



\## 📱 WhatsApp Deployment Strategy



To integrate this agent with WhatsApp:



\### Architecture



1\. \*\*Webhook Server\*\* (FastAPI/Flask)

&nbsp;  - HTTPS endpoint for Meta's WhatsApp Business API

&nbsp;  - Message parsing and routing

&nbsp;  - Webhook verification



2\. \*\*Session Management\*\* (Redis/DynamoDB)

&nbsp;  - Store agent state per phone number

&nbsp;  - Handle concurrent users

&nbsp;  - Session timeout (24h)



3\. \*\*Implementation\*\*

```python

from fastapi import FastAPI, Request

from agent\_gemini import AutoStreamAgent

import redis



app = FastAPI()

cache = redis.Redis()



@app.post("/webhook")

async def handle\_message(request: Request):

&nbsp;   data = await request.json()

&nbsp;   phone = data\['entry']\[0]\['changes']\[0]\['value']\['messages']\[0]\['from']

&nbsp;   message = data\['entry']\[0]\['changes']\[0]\['value']\['messages']\[0]\['text']\['body']

&nbsp;   

&nbsp;   # Load or create agent state

&nbsp;   state = cache.get(f"agent:{phone}")

&nbsp;   agent = AutoStreamAgent()

&nbsp;   if state:

&nbsp;       agent.state = json.loads(state)

&nbsp;   

&nbsp;   # Process message

&nbsp;   response = agent.chat(message)

&nbsp;   

&nbsp;   # Save state

&nbsp;   cache.set(f"agent:{phone}", json.dumps(agent.state), ex=86400)

&nbsp;   

&nbsp;   # Send response via WhatsApp API

&nbsp;   send\_whatsapp\_message(phone, response)

&nbsp;   

&nbsp;   return {"status": "success"}

```



4\. \*\*Production Considerations\*\*

&nbsp;  - Use Meta's official WhatsApp Business API or Twilio

&nbsp;  - Implement rate limiting and message queueing

&nbsp;  - Add logging and monitoring (Sentry, CloudWatch)

&nbsp;  - Support media messages and quick replies



---



\## 📊 Two Implementation Approaches



I've implemented \*\*TWO versions\*\* to demonstrate different strategies:



\### Rule-Based Version (`agent\_gemini.py`)

\- Pattern matching for intent classification

\- Template-based responses

\- ⚡ Instant, deterministic behavior

\- ✅ Perfect for production reliability



\### AI-Powered Version (`agent\_gemini\_ai.py`)

\- Google Gemini 1.5 Flash for natural language understanding

\- Dynamic, context-aware responses

\- 🤖 Handles varied user phrasing

\- ✅ Better user experience



See \[COMPARISON.md](COMPARISON.md) for detailed analysis.



---



\## 📁 Project Structure

```

autostream-agent/

├── agent\_gemini.py              # Rule-based implementation

├── agent\_gemini\_ai.py           # AI-powered implementation

├── requirements.txt             # Python dependencies

├── .env.example                 # Environment template

├── knowledge\_base.json          # RAG data (auto-generated)

├── README.md                    # This file

├── COMPARISON.md                # Version comparison

├── SETUP.md                     # Detailed setup guide

└── QUICKSTART.md                # 5-minute quick start

```



---



\## 🧪 Testing



\### Manual Testing

```bash

\# Test rule-based version

python agent\_gemini.py



\# Test conversations:

\# 1. Pricing inquiry → Lead qualification → Tool execution

\# 2. Feature questions → RAG retrieval

\# 3. Edge cases (incomplete emails, etc.)

```



\### Expected Behavior



1\. \*\*Intent Detection\*\*: Correctly classifies messages as casual, product\_inquiry, or high\_intent

2\. \*\*RAG Retrieval\*\*: Returns pricing/policy information from knowledge base

3\. \*\*State Management\*\*: Remembers context across 5-6 turns

4\. \*\*Tool Execution\*\*: Calls `mock\_lead\_capture()` only when all data collected



---



\## 🛠️ Customization



\### Update Knowledge Base



Edit `agent\_gemini.py`:

```python

KNOWLEDGE\_BASE = {

&nbsp;   "pricing": {

&nbsp;       "basic": {"price": 29, "videos": 10, "resolution": "720p"},

&nbsp;       "pro": {"price": 79, "videos": "Unlimited", "resolution": "4K"}

&nbsp;   }

}

```



\### Add More Platforms

```python

platforms = \['youtube', 'instagram', 'tiktok', 'twitter', 'facebook', 'linkedin']

```



---



\## 📝 Requirements Met



| Requirement | Status | Implementation |

|------------|--------|----------------|

| Intent Classification | ✅ | 3 types: casual, product\_inquiry, high\_intent |

| RAG Knowledge Retrieval | ✅ | JSON knowledge base with pricing \& policies |

| Tool Execution | ✅ | Sequential collection (name→email→platform) |

| State Management | ✅ | LangGraph StateGraph with 5-6 turn memory |

| LangGraph Framework | ✅ | 5 nodes with conditional routing |

| Python 3.9+ | ✅ | Type hints, modern syntax |



---



\## 🎥 Demo Video



\[Link to demo video]



\*\*Demonstrates:\*\*

\- RAG answering pricing questions

\- Intent detection (product\_inquiry → high\_intent)

\- Sequential lead data collection

\- Tool execution with console output

\- State management across turns



---



\## 🤝 Contributing



This is an internship assignment project.



---



\## 📄 License



MIT License



---



\## 👤 Author



\*\*\Kevin Pratap Sidhu\*\*  

Email: \Pratapkevin8@gmail.com 



Built for ServiceHive's Inflx Platform - ML Intern Assignment



---



\*\*⭐ If you found this helpful, please star the repo!\*\*

