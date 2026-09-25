# MerchantAI - Agentic SMB Marketing & Onboarding Copilot

A portfolio project demonstrating an AI-powered merchant onboarding and campaign planning system with agentic workflows, RAG implementation, and a complete demo mode.

## 🎯 Project Overview

MerchantAI helps small businesses onboard onto AI-powered advertising tools through an intelligent agent workflow that:

1. **Collects merchant information** through a guided onboarding process
2. **Validates completeness** and identifies missing information
3. **Plans campaigns** using AI agents with RAG-enhanced knowledge retrieval
4. **Generates ad copy** with multiple variations
5. **Creates creative briefs** for visual content direction
6. **Validates campaign readiness** before launch

## 🏗️ Architecture

```
Frontend (Next.js + TypeScript + Tailwind CSS)
    ↓ HTTP/REST API
Backend (FastAPI + Python)
    ↓
Agent & Tool Layer (Orchestrator)
    ↓
AI Provider Layer (Modular - Demo/OpenAI/Anthropic)
    ↓
RAG Layer (Local Knowledge Base)
    ↓
Database Layer (SQLite + SQLAlchemy)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Configure environment variables in `backend/.env`:

```env
AI_PROVIDER=demo
DATABASE_URL=sqlite:///./data/merchantai.db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Start the backend server:

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
cd frontend
npm install
```

Configure environment variables in `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the frontend server:

```bash
cd frontend
npm run dev
```

Access the application at `http://localhost:3000`

## 🎯 Demo Journey

The complete demo flow demonstrates:

1. **Landing Page** - Introduction to MerchantAI
2. **Merchant Onboarding** - Multi-step form collecting business information
3. **Onboarding Validation** - AI agent validates completeness
4. **Campaign Planning** - AI agent generates campaign strategy with RAG
5. **Ad Copy Generation** - AI agent creates compelling ad copy variations
6. **Creative Brief Generation** - AI agent produces visual content direction
7. **Readiness Check** - Validation system confirms campaign readiness
8. **Dashboard** - Complete view of all generated components

## 🤖 Agent Workflow

The system implements a genuine agent/tool workflow:

```
Merchant Input
    ↓
Onboarding Agent (Validation Tool)
    ↓
RAG Service (Knowledge Retrieval)
    ↓
Campaign Planning Agent
    ↓
Ad Copy Generator Agent
    ↓
Creative Brief Generator Agent
    ↓
Readiness Validator Tool
    ↓
Campaign Ready Status
```

## 📁 Project Structure

```
MerchantAI/
├── frontend/                    # Next.js Frontend
│   ├── src/
│   │   ├── app/                # Next.js App Router
│   │   ├── components/         # React components
│   │   │   ├── onboarding/    # Onboarding form
│   │   │   └── dashboard/     # Campaign dashboard
│   │   └── lib/                # Utilities & API client
│   └── package.json
│
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── api/                # API endpoints
│   │   ├── agents/             # AI agents
│   │   ├── tools/              # Agent tools
│   │   ├── models/             # Database models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   └── main.py             # FastAPI app
│   ├── data/
│   │   ├── knowledge_base/     # RAG knowledge base
│   │   └── merchantai.db       # SQLite database
│   └── requirements.txt
│
└── README.md
```

## 🔧 Technical Features

### Agent System
- **Orchestrator Agent**: Coordinates between different agents and tools
- **Onboarding Agent**: Validates merchant information and guides completion
- **Campaign Planning Agent**: Generates campaign strategies with RAG context
- **Ad Copy Generator**: Creates compelling ad copy with variations
- **Creative Brief Generator**: Produces detailed visual content direction

### RAG Implementation
- Local knowledge base with marketing guidance
- Keyword-based retrieval (MVP)
- Context-aware prompt enhancement
- Modular design for vector store upgrade

### Demo Mode
- Deterministic mock responses
- No API keys required
- Follows same architecture as production
- Clear separation from real AI providers

### Database
- SQLite with SQLAlchemy ORM
- Structured for PostgreSQL migration
- Comprehensive data models
- Relationship management

## 🎨 UI/UX

- **Professional Design**: Clean, minimal, premium aesthetic
- **Responsive**: Desktop-first, mobile-friendly
- **Loading States**: Clear feedback during operations
- **Error Handling**: Graceful error messages
- **Empty States**: Helpful guidance when no data exists

## 🔐 Security

- No API keys in frontend code
- Environment variable configuration
- CORS protection
- Input validation
- SQL injection prevention (ORM)

## 📊 Database Schema

### Core Models
- **Merchant**: Business information and onboarding status
- **Campaign**: Campaign planning and readiness status
- **AdCopy**: Generated ad copy with variations
- **CreativeBrief**: Visual content direction
- **ValidationIssue**: Campaign validation issues

## 🧪 Testing the Application

### Manual Testing Steps

1. **Start both servers** (backend on port 8000, frontend on port 3000)
2. **Open browser** to `http://localhost:3000`
3. **Click "Get Started"** to begin onboarding
4. **Fill business information**:
   - Business Name: "Test Boutique"
   - Business Type: "Fashion/Apparel"
   - Location: "Mumbai"
   - Product/Service: "Women's ethnic wear"
   - Target Customers: "Women aged 22-40"
   - Marketing Goal: "Increase Diwali sales"
   - Budget: 15000
   - Platform: "Instagram"
5. **Complete onboarding** and proceed to dashboard
6. **Click "Generate All"** to run the complete agent workflow
7. **Review generated components**:
   - Campaign plan with audience targeting
   - Ad copy with 3 variations
   - Creative brief with visual direction
   - Readiness validation
8. **Verify campaign status** shows "READY"

### API Testing

```bash
# Create merchant
curl -X POST http://localhost:8000/api/merchants/ \
  -H "Content-Type: application/json" \
  -d '{"business_name":"Test Boutique","business_type":"Fashion","location":"Mumbai","product_service":"Ethnic wear","target_customers":"Women 22-40","marketing_goal":"Sales","campaign_budget":15000,"preferred_platform":"Instagram"}'

# Validate onboarding
curl -X POST http://localhost:8000/api/merchants/1/validate-onboarding

# Plan campaign
curl -X POST http://localhost:8000/api/campaigns/plan \
  -H "Content-Type: application/json" \
  -d '{"merchant_id":1}'

# Generate ad copy
curl -X POST http://localhost:8000/api/campaigns/1/generate-ad-copy

# Generate creative brief
curl -X POST http://localhost:8000/api/campaigns/1/generate-creative-brief

# Check readiness
curl -X POST http://localhost:8000/api/campaigns/1/check-readiness
```

## 🔄 Demo Mode vs Production

### Demo Mode (Default)
- Uses deterministic mock responses
- No API keys required
- Perfect for demonstrations
- Follows same architecture

### Production Mode
Set `AI_PROVIDER=openai` or `AI_PROVIDER=anthropic` in `.env`
- Requires valid API keys
- Uses real LLM responses
- More dynamic and varied outputs
- Higher costs

## 🚀 Future Enhancements

- [ ] Vector-based RAG with ChromaDB
- [ ] Real-time chat interface
- [ ] Multiple campaign management
- [ ] A/B testing integration
- [ ] Analytics dashboard
- [ ] User authentication
- [ ] PostgreSQL migration
- [ ] Advanced agent orchestration

## 📝 Interview Talking Points

### Technical Depth
- **Agent Architecture**: Explain the orchestrator pattern and tool selection
- **RAG Implementation**: Discuss knowledge base design and retrieval strategy
- **State Management**: How the system maintains conversation context
- **Modular Design**: AI provider abstraction and demo mode implementation

### Problem Solving
- **Validation Strategy**: Multi-layer validation approach
- **Error Handling**: Graceful degradation in demo mode
- **Performance Considerations**: Async operations and loading states
- **Scalability**: Database design for future growth

### Business Value
- **SMB Focus**: Tailored for small business needs
- **Cost Effective**: Demo mode reduces barriers to entry
- **Practical Application**: Real marketing challenges addressed
- **User Experience**: Guided workflow reduces complexity

## 🛠️ Development

### Adding New Agents

1. Create agent class in `backend/app/agents/`
2. Implement tool methods in `backend/app/tools/`
3. Add orchestration logic in `orchestrator.py`
4. Create API endpoints in `backend/app/api/`
5. Update frontend components as needed

### Extending Knowledge Base

Add markdown files to `backend/data/knowledge_base/`:
- Campaign-specific guidance
- Industry best practices
- Platform-specific strategies

## 📄 License

This is a portfolio project for demonstration purposes.

## 👤 Author

Built as a portfolio project to demonstrate full-stack AI engineering skills.

---

**Note**: This project is a portfolio prototype and does not integrate with actual advertising platforms or process real payments.
