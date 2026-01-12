"""
AutoStream AI Agent - PERFECT WORKING VERSION
Rule-based implementation with proper intent detection
"""

from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Dict]
    intent: str
    lead_data: Dict[str, Optional[str]]
    knowledge_context: Optional[str]
    next_action: str
    awaiting_name: bool

KNOWLEDGE_BASE = {
    "pricing": {
        "basic": {"price": 29, "videos": 10, "resolution": "720p"},
        "pro": {"price": 79, "videos": "Unlimited", "resolution": "4K"}
    }
}

def mock_lead_capture(name: str, email: str, platform: str):
    print(f"\n{'='*60}")
    print(f"🎯 LEAD CAPTURED SUCCESSFULLY!")
    print(f"{'='*60}")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Platform: {platform}")
    print(f"{'='*60}\n")

def retrieve_knowledge(query: str) -> Optional[str]:
    return """AutoStream Pricing Plans:

Basic Plan - $29/month:
- 10 videos/month
- 720p resolution

Pro Plan - $79/month:
- Unlimited videos
- 4K resolution
- AI captions
- 24/7 support"""

def extract_information(text: str):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = re.search(email_pattern, text)
    platforms = ['youtube', 'instagram', 'tiktok', 'twitter', 'facebook']
    platform = next((p.capitalize() for p in platforms if p in text.lower()), None)
    return {'email': email.group(0) if email else None, 'platform': platform}

def classify_intent(state: AgentState):
    msg = state['messages'][-1]['content'].lower()
    
    # If waiting for name, keep high_intent
    if state.get('awaiting_name'):
        state['intent'] = 'high_intent'
        return state
    
    # Enhanced high-intent patterns
    high_intent_keywords = [
        'want to try', 'sign up', 'interested', 'i want', 'try the',
        'get started', 'basic plan', 'pro plan', 'subscribe', 'purchase',
        'buy', 'i would like to try', 'i\'d like', 'take the', 'go with'
    ]
    
    product_keywords = ['pricing', 'price', 'cost', 'plans', 'features', 'how much']
    
    if any(p in msg for p in high_intent_keywords):
        state['intent'] = 'high_intent'
    elif any(p in msg for p in product_keywords):
        state['intent'] = 'product_inquiry'
    else:
        state['intent'] = 'casual'
    return state

def rag_retrieval(state: AgentState):
    if state['intent'] == 'product_inquiry':
        state['knowledge_context'] = retrieve_knowledge(state['messages'][-1]['content'])
    return state

def generate_response(state: AgentState):
    intent = state['intent']
    lead_data = state['lead_data']
    latest_msg = state['messages'][-1]['content']
    extracted = extract_information(latest_msg)
    
    # Update extracted data
    if extracted['email'] and not lead_data.get('email'):
        lead_data['email'] = extracted['email']
    if extracted['platform'] and not lead_data.get('platform'):
        lead_data['platform'] = extracted['platform']
    
    # Casual
    if intent == 'casual' and not state.get('awaiting_name'):
        response = "Hello! I'm here to help you with AutoStream. Would you like to know about our pricing plans or features?"
        state['messages'].append({'role': 'assistant', 'content': response})
        state['next_action'] = 'continue'
        return state
    
    # Product inquiry
    if intent == 'product_inquiry':
        response = state.get('knowledge_context', "I can help with pricing and features!")
        response += "\n\nWould you like to get started with any of our plans?"
        state['messages'].append({'role': 'assistant', 'content': response})
        state['next_action'] = 'continue'
        return state
    
    # High intent - lead collection
    if intent == 'high_intent':
        if not lead_data.get('name'):
            if state.get('awaiting_name'):
                # This message IS the name
                lead_data['name'] = latest_msg.strip()
                state['awaiting_name'] = False
                response = "Perfect! And what's your email address?"
            else:
                # Ask for name
                response = "That's great to hear! To get you started, could you please share your name?"
                state['awaiting_name'] = True
            state['messages'].append({'role': 'assistant', 'content': response})
            state['next_action'] = 'collect_info'
        
        elif not lead_data.get('email'):
            response = "Great! What's your email address?"
            state['messages'].append({'role': 'assistant', 'content': response})
            state['next_action'] = 'collect_info'
        
        elif not lead_data.get('platform'):
            response = "Awesome! Last question - which platform do you create content for? (YouTube, Instagram, TikTok, etc.)"
            state['messages'].append({'role': 'assistant', 'content': response})
            state['next_action'] = 'collect_info'
        
        else:
            # All data collected
            state['next_action'] = 'execute_tool'
        
        state['lead_data'] = lead_data
    
    return state

def execute_lead_capture(state: AgentState):
    ld = state['lead_data']
    if all([ld.get('name'), ld.get('email'), ld.get('platform')]):
        mock_lead_capture(ld['name'], ld['email'], ld['platform'])
        response = f"🎉 Awesome! We've captured your information, {ld['name']}. Our team will reach out to {ld['email']} shortly to help you get started with AutoStream for your {ld['platform']} channel. Welcome aboard!"
        state['messages'].append({'role': 'assistant', 'content': response})
        state['lead_data'] = {'name': None, 'email': None, 'platform': None}
        state['intent'] = 'casual'
        state['awaiting_name'] = False
        state['next_action'] = 'end'
    return state

def route_next(state: AgentState):
    return 'execute_tool' if state.get('next_action') == 'execute_tool' else 'end'

def build_agent_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("rag_retrieval", rag_retrieval)
    workflow.add_node("generate_response", generate_response)
    workflow.add_node("execute_tool", execute_lead_capture)
    workflow.set_entry_point("classify_intent")
    workflow.add_edge("classify_intent", "rag_retrieval")
    workflow.add_edge("rag_retrieval", "generate_response")
    workflow.add_conditional_edges("generate_response", route_next, {"execute_tool": "execute_tool", "end": END})
    workflow.add_edge("execute_tool", END)
    return workflow.compile()

class AutoStreamAgent:
    def __init__(self):
        self.graph = build_agent_graph()
        self.state = {
            'messages': [],
            'intent': 'casual',
            'lead_data': {'name': None, 'email': None, 'platform': None},
            'knowledge_context': None,
            'next_action': 'continue',
            'awaiting_name': False
        }
    
    def chat(self, user_message: str) -> str:
        self.state['messages'].append({'role': 'user', 'content': user_message})
        result = self.graph.invoke(self.state)
        self.state = result
        ai_msgs = [m for m in result['messages'] if m.get('role') == 'assistant']
        return ai_msgs[-1]['content'] if ai_msgs else "I'm here to help!"

def main():
    agent = AutoStreamAgent()
    print("=" * 60)
    print("AutoStream AI Agent - Rule-Based Version")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    print("Agent: Hello! I'm the AutoStream AI assistant. How can I help you today?\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                print("\nAgent: Thanks for chatting!")
                break
            if not user_input:
                continue
            response = agent.chat(user_input)
            print(f"\nAgent: {response}\n")
            print(f"[Debug] Intent: {agent.state['intent']} | Lead Data: {agent.state['lead_data']}\n")
        except KeyboardInterrupt:
            print("\n\nAgent: Thanks for chatting!")
            break

if __name__ == "__main__":
    main()
