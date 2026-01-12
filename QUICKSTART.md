# 🚀 Quick Start Guide - 5 Minutes to Running Agent

## Step 1: Setup (2 minutes)

```bash
# Clone and navigate
git clone <repo-url>
cd autostream-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Key (1 minute)

Create `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
```

Get your API key:
- **OpenAI**: https://platform.openai.com/api-keys
- **Gemini**: https://makersuite.google.com/app/apikey
- **Claude**: https://console.anthropic.com/

## Step 3: Run Demo (2 minutes)

### Option A: Interactive Chat
```bash
python agent.py
```

Then type:
1. "Hi, tell me about your pricing"
2. "I want to try the Pro plan for my YouTube channel"
3. "John Smith"
4. "john@example.com"

### Option B: Automated Demo (for video recording)
```bash
python test_conversation.py
```
Choose option `1` for full demo

## 📹 Recording Your Demo Video

1. **Start screen recording** (OBS, QuickTime, etc.)
2. **Run**: `python test_conversation.py`
3. **Choose option 1**: Full conversation demo
4. **Show**:
   - Agent answering pricing question (RAG)
   - Intent changing to "high_intent"
   - Lead data being collected
   - Console output: `Lead captured successfully: ...`

**Target Duration**: 2-3 minutes

## ✅ What You Should See

### Expected Console Output:
```
Agent: Hello! I'm the AutoStream AI assistant...
[Debug] Intent: casual | Lead Data: {'name': None, 'email': None, 'platform': None}

You: Tell me about your pricing
Agent: We offer two plans:

Basic Plan - $29/month
• 10 videos/month
• 720p resolution

Pro Plan - $79/month
• Unlimited videos
• 4K resolution
• AI captions
• 24/7 support

[Debug] Intent: product_inquiry | Lead Data: {'name': None, 'email': None, 'platform': None}

You: I want to try the Pro plan for my YouTube channel
Agent: That's great to hear! To get you started, could you please share your name?
[Debug] Intent: high_intent | Lead Data: {'name': None, 'email': None, 'platform': 'Youtube'}

You: John Smith
Agent: Perfect! And what's your email address?
[Debug] Intent: high_intent | Lead Data: {'name': 'John Smith', 'email': None, 'platform': 'Youtube'}

You: john@example.com
Lead captured successfully: John Smith, john@example.com, Youtube
Agent: 🎉 Awesome! We've captured your information, John Smith...
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'langgraph'"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
Check your `.env` file exists and has:
```
OPENAI_API_KEY=sk-...
```

### Agent not detecting platform
Say the platform explicitly: "I want to try it for YouTube" or "for my Instagram page"

## 📚 Next Steps

- Read full `README.md` for architecture details
- Customize `KNOWLEDGE_BASE` in `agent.py`
- Try different conversation flows
- Add more test cases in `test_conversation.py`

## 💡 Pro Tips for Demo Video

1. **Zoom in** on terminal (Cmd/Ctrl + Plus)
2. **Use dark mode** for better contrast
3. **Speak while typing**: "Now I'll ask about pricing..."
4. **Highlight key moments**: "Notice the intent changed to high_intent"
5. **Show the console log** when `mock_lead_capture()` is called

---

**Need Help?** Check the main README.md or contact ServiceHive team.
