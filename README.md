#🚀 AutoStream AI Agent
Agentic Social-to-Lead Conversion System using LangGraph & Gemini

AutoStream AI Agent is an agentic conversational system that converts natural conversations into qualified business leads for AutoStream, an AI-powered video editing SaaS.

It combines LLM intelligence, Retrieval-Augmented Generation (RAG), and deterministic workflow control to simulate a real-world AI sales and onboarding assistant.

##🎯 Project Overview

This system implements a full agentic workflow that:

Classifies user intent (casual, product inquiry, high-intent)

Retrieves grounded answers using RAG

Maintains multi-turn conversation state

Collects leads step-by-step (name → email → platform)

Executes tools only when all conditions are satisfied

This project demonstrates how modern AI agents are built using explicit state machines instead of simple prompt chaining.

##✨ Key Capabilities

Agentic state machine using LangGraph

Dual system: rule-based + AI-powered

Deterministic lead-qualification funnel

Real-world SaaS sales flow simulation

Production-style modular architecture

##⚡ Quick Start

Prerequisites

Python 3.9+

Google Gemini API key

Installation

git clone https://github.com/KevinPratap/autostream-ai-agent.git

cd autostream-ai-agent

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

Create a .env file and add:
GOOGLE_API_KEY=your_api_key_here

##▶️ Run the Agent

Rule-Based Version (no API required)
python agent_gemini.py

AI-Powered Version (Gemini)
python agent_gemini_ai.py

##🎬 Sample Conversation

You: tell me about pricing

Agent:
Basic – $29/month (10 videos, 720p)
Pro – $79/month (Unlimited, 4K, AI captions)

You: I want the Pro plan

Agent: Love that — what’s your name?

You: Kevin

Agent: What’s the best email to reach you on?

You: kevin@example.com

Agent: Which platform do you create for?

You: YouTube

LEAD CAPTURED SUCCESSFULLY

##🧠 System Architecture

LangGraph enables explicit, debuggable, and controllable AI workflows instead of fragile prompt chains.

Core design principles:

Explicit state graph

Persistent memory

Conditional routing

Isolated RAG module

Safe tool execution

##🔁 Workflow

User Input
↓
Intent Classification
↓
RAG Retrieval
↓
Response Generation
↓
State Evaluation
→ Tool Call or Continue Chat
↓
State Reset

##📊 Dual Implementation Strategy

Rule-Based Agent (agent_gemini.py)

Pattern-driven intent detection

Fully deterministic

Production-stable

Cost-free inference

AI-Powered Agent (agent_gemini_ai.py)

Gemini-powered reasoning

Context-aware conversations

Flexible phrasing support

Higher UX quality

See COMPARISON.md for details.

##📁 Project Structure

autostream-ai-agent/
agent_gemini.py
agent_gemini_ai.py
requirements.txt
.env.example
knowledge_base.json
README.md
COMPARISON.md
SETUP.md
QUICKSTART.md

##🧪 Testing Coverage

Intent detection accuracy

RAG grounding behavior

Multi-turn memory

Sequential lead capture

Edge-case handling

Tool execution safety

##🌐 Deployment Concept

This system can be extended using FastAPI, Redis session storage, WhatsApp Business API, and cloud deployment on AWS, GCP, or Azure.

##📌 Academic & Engineering Value

Agentic system design

Finite-state workflow control

Applied LLM integration

RAG system implementation

SaaS automation use-case

Production-style architecture

##🏆 Outcome

This project demonstrates the ability to design controlled AI agents, integrate LLMs responsibly, and engineer real-world automation systems.

##👤 Author

Kevin Pratap Sidhu
MBA Tech (AI), NMIMS
GitHub: https://github.com/KevinPratap

⭐ Support

If you find this project useful, consider starring the repository.
