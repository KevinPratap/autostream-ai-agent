from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END
from google import genai
from dotenv import load_dotenv
import json, re, os

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """
You are AutoStream’s official AI assistant.

AutoStream is a premium AI-powered video editing platform for creators and businesses.

Be friendly, confident, natural and helpful.
Focus on benefits.
Guide users toward getting started.
Keep replies short and human.
"""

def gemini(prompt: str) -> str:
    r = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return r.text.strip()

class AgentState(TypedDict):
    messages: List[Dict]
    intent: str
    lead_data: Dict[str, Optional[str]]
    knowledge_context: Optional[str]
    next_action: str
    conversation_history: str

KNOWLEDGE_BASE = {
    "pricing": {
        "basic": {"price": 29, "videos": 10, "resolution": "720p"},
        "pro": {"price": 79, "videos": "Unlimited", "resolution": "4K"}
    },
    "policies": {
        "refunds": "No refunds after 7 days",
        "support": "24/7 support on Pro plan"
    }
}

def save_kb():
    with open("knowledge_base.json", "w") as f:
        json.dump(KNOWLEDGE_BASE, f, indent=2)

def retrieve_knowledge(q: str):
    q = q.lower()
    if any(w in q for w in ["price","pricing","cost","plan","plans","feature","features","fetures","basic","pro","options"]):
        b = KNOWLEDGE_BASE["pricing"]["basic"]
        p = KNOWLEDGE_BASE["pricing"]["pro"]
        return f"""
Basic – ${b['price']}/month: {b['videos']} videos, {b['resolution']}
Pro – ${p['price']}/month: Unlimited videos, {p['resolution']}, AI captions, 24/7 support
"""
    if "refund" in q:
        return KNOWLEDGE_BASE["policies"]["refunds"]
    if "support" in q:
        return KNOWLEDGE_BASE["policies"]["support"]
    return None

def classify_intent(state: AgentState):
    if state["next_action"] in ["awaiting_name","awaiting_email","awaiting_platform"]:
        return state

    msg = state["messages"][-1]["content"]
    m = msg.lower()

    try:
        intent = gemini(f"""
Classify intent into one word only:
casual
product_inquiry
high_intent

Message: "{msg}"
""").lower()
        if intent not in ["casual","product_inquiry","high_intent"]:
            intent = "casual"
        state["intent"] = intent
    except:
        state["intent"] = "casual"

    if any(w in m for w in ["price","pricing","cost","plan","plans","feature","features","tell me","options"]):
        state["intent"] = "product_inquiry"

    if any(w in m for w in ["buy","start","signup","sign up","trial","demo","interested","basic","pro"]):
        state["intent"] = "high_intent"

    if m.strip() in ["basic","pro","basic plan","pro plan"]:
        state["intent"] = "high_intent"

    return state

def rag_retrieval(state: AgentState):
    if state["intent"] == "product_inquiry":
        state["knowledge_context"] = retrieve_knowledge(state["messages"][-1]["content"])
    return state

def generate_response(state: AgentState):
    msg = state["messages"][-1]["content"]
    intent = state["intent"]
    lead = state["lead_data"]

    if intent == "casual":
        try:
            reply = gemini(f"""{SYSTEM_PROMPT}
User: {msg}
Reply naturally and briefly.
""")
        except:
            reply = "Hey! I can help you with AutoStream’s features, pricing, or getting started."
        state["messages"].append({"role":"assistant","content":reply})
        state["next_action"] = "continue"
        return state

    if intent == "product_inquiry":
        kb = state.get("knowledge_context","")
        try:
            reply = gemini(f"""{SYSTEM_PROMPT}
User question: {msg}
Info: {kb}
Explain benefits and ask if they want to get started.
""")
        except:
            reply = kb or "AutoStream helps creators turn raw clips into professional videos fast."
        state["messages"].append({"role":"assistant","content":reply})
        state["next_action"] = "continue"
        return state

    if intent == "high_intent":

        if state["next_action"] not in ["awaiting_name","awaiting_email","awaiting_platform"]:
            state["messages"].append({"role":"assistant","content":"Love that — let’s get you set up. What’s your name?"})
            state["next_action"] = "awaiting_name"
            return state

        if state["next_action"] == "awaiting_name":
            lead["name"] = msg.strip()
            state["messages"].append({"role":"assistant","content":"Nice to meet you! What’s the best email to reach you on?"})
            state["next_action"] = "awaiting_email"
            return state

        if state["next_action"] == "awaiting_email":
            if re.match(r"\b[\w.-]+@[\w.-]+\.\w+\b", msg):
                lead["email"] = msg.strip()
                state["messages"].append({"role":"assistant","content":"Great. Which platform are you mainly creating content for?"})
                state["next_action"] = "awaiting_platform"
                return state
            else:
                state["messages"].append({"role":"assistant","content":"That doesn’t look like a valid email. Could you enter a correct one?"})
                return state

        if state["next_action"] == "awaiting_platform":
            lead["platform"] = msg.strip().capitalize()
            state["next_action"] = "execute_tool"
            return state

    return state

def execute_lead_capture(state: AgentState):
    d = state["lead_data"]
    if all([d["name"], d["email"], d["platform"]]):
        try:
            reply = "🎉 " + gemini(f"Write a short enthusiastic welcome message for {d['name']} who creates on {d['platform']}.")
        except:
            reply = f"🎉 Welcome {d['name']}! We’ll reach out soon with next steps."
        state["messages"].append({"role":"assistant","content":reply})
        state["lead_data"] = {"name":None,"email":None,"platform":None}
        state["intent"] = "casual"
        state["next_action"] = "end"
    return state

def route_next(state: AgentState):
    return "execute_tool" if state.get("next_action") == "execute_tool" else END

def build_graph():
    g = StateGraph(AgentState)
    g.add_node("classify_intent", classify_intent)
    g.add_node("rag_retrieval", rag_retrieval)
    g.add_node("generate_response", generate_response)
    g.add_node("execute_tool", execute_lead_capture)
    g.set_entry_point("classify_intent")
    g.add_edge("classify_intent","rag_retrieval")
    g.add_edge("rag_retrieval","generate_response")
    g.add_conditional_edges("generate_response", route_next, {"execute_tool":"execute_tool", END:END})
    g.add_edge("execute_tool", END)
    return g.compile()

class AutoStreamAgent:
    def __init__(self):
        self.graph = build_graph()
        self.state = {
            "messages":[],
            "intent":"casual",
            "lead_data":{"name":None,"email":None,"platform":None},
            "knowledge_context":None,
            "next_action":"continue",
            "conversation_history":""
        }
        save_kb()

    def chat(self, text: str):
        self.state["messages"].append({"role":"user","content":text})
        result = self.graph.invoke(self.state)
        self.state = result
        msgs = [m for m in result["messages"] if m["role"]=="assistant"]
        return msgs[-1]["content"] if msgs else "I'm here to help."

def main():
    agent = AutoStreamAgent()
    print("\n" + "="*60)
    print("AutoStream AI Agent – Gemini Powered")
    print("="*60)
    try:
        greeting = gemini("Greet as AutoStream’s AI assistant and offer help.")
    except:
        greeting = "Hey! I’m AutoStream’s AI assistant. How can I help today?"
    print(f"\nAgent: {greeting}\n")

    while True:
        user = input("You: ").strip()
        if user.lower() in ["quit","exit","bye"]:
            print("\nAgent: Thanks for chatting 👋")
            break
        if not user:
            continue
        reply = agent.chat(user)
        print(f"\nAgent: {reply}\n")
        print(f"[Debug] Intent: {agent.state['intent']} | Lead: {agent.state['lead_data']}\n")

if __name__ == "__main__":
    main()
