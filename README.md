# MCP-Based AI Chatbot 🤖

A modern, full-stack AI chatbot application built using the **Model Context Protocol (MCP)** that provides intelligent conversational experiences with integrated tools for weather information and news updates.

## 🌟 Features

### 🧠 Core Capabilities
- **Intelligent Conversations**: Powered by OpenAI GPT-4o-mini via OpenRouter API
- **Function Calling**: Smart tool selection based on user queries
- **Real-time Responses**: Fast, responsive chat interface
- **Error Handling**: Robust error management and user feedback

### 🔧 Integrated Tools
- **🌤️ Weather Information**: Get current weather and forecasts for any city worldwide
  - Real-time weather data using Open-Meteo API (free, no API key required)
  - Temperature, humidity, wind speed, and weather conditions
  - Daily forecasts with precipitation information
  - Global coverage with automatic geocoding

- **📰 News Updates**: Fetch latest news on any topic
  - Powered by NewsData.io API
  - Customizable topics and search terms
  - Real-time news headlines with source links
  - English language news from US sources

### 💻 Modern Tech Stack
- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + MCP Framework + uvicorn
- **APIs**: OpenRouter (GPT-4o-mini), Open-Meteo, NewsData.io
- **UI Components**: Radix UI + Lucide React icons

## 🏗️ Project Structure

```
MCP-AI-Chatbot/
├── MCP-chatbot-frontend/          # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.tsx        # Main chat interface
│   │   │   └── ui/                # Reusable UI components
│   │   ├── services/
│   │   │   └── chatApi.ts         # API communication layer
│   │   ├── App.tsx                # Root component
│   │   └── main.tsx               # Application entry point
│   ├── package.json               # Frontend dependencies
│   └── vite.config.ts             # Vite configuration
├── MCP-server-backend/            # FastAPI backend server
│   ├── chatbot_server.py          # Main server with MCP tools
│   ├── pyproject.toml             # Python dependencies
│   └── README.md                  # Backend documentation
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm/yarn
- **Python** 3.10+
- **uv** (Python package manager) - [Install uv](https://docs.astral.sh/uv/)

### 1. Clone the Repository
```bash
git clone https://github.com/sakthivel2264/MCP-AI-Chatbot.git
cd MCP-AI-Chatbot
```

### 2. Backend Setup

#### Install Dependencies
```bash
cd MCP-server-backend
uv sync
```

#### Environment Configuration
Create a `.env` file in the `MCP-server-backend` directory:
```env
# Required: OpenRouter API Key for AI responses
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Required: NewsData.io API Key for news functionality
NEWSDATA_API_KEY=your_newsdata_api_key_here
```

#### Start the Backend Server
```bash
uv run python chatbot_server.py
```
The server will start on `http://localhost:8000`

### 3. Frontend Setup

#### Install Dependencies
```bash
cd ../MCP-chatbot-frontend
npm install
```

#### Start the Development Server
```bash
npm run dev
```
The frontend will start on `http://localhost:5173`

## 🔑 API Keys Setup

### OpenRouter API Key
1. Visit [OpenRouter](https://openrouter.ai/)
2. Create an account and get your API key
3. Add it to your `.env` file as `OPENROUTER_API_KEY`

### NewsData.io API Key
1. Visit [NewsData.io](https://newsdata.io/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file as `NEWSDATA_API_KEY`

## 📱 Usage

### Chat Interface
1. Open your browser to `http://localhost:5173`
2. Start chatting with the AI assistant
3. Ask for weather: *"What's the weather in Tokyo?"*
4. Get news updates: *"Show me news about technology"*
5. General conversation: *"Tell me a joke"*

### Example Queries
```
🌤️ Weather Queries:
- "What's the weather in London?"
- "How's the temperature in New York today?"
- "Is it raining in Paris?"

📰 News Queries:
- "Latest news about artificial intelligence"
- "What's happening in technology?"
- "Show me sports news"

💬 General Chat:
- "Tell me a joke"
- "How are you today?"
- "What can you help me with?"
```

## 🛠️ Development

### Backend Development
```bash
cd MCP-server-backend

# Install dependencies
uv sync

# Run in development mode with auto-reload
uv run uvicorn chatbot_server:app --reload --host 0.0.0.0 --port 8000

# Health check
curl http://localhost:8000/health
```

### Frontend Development
```bash
cd MCP-chatbot-frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔧 Configuration

### Backend Configuration
- **Port**: Default 8000 (configurable in `chatbot_server.py`)
- **CORS**: Configured for `localhost:5173` and `localhost:3000`
- **Models**: Uses OpenAI GPT-4o-mini via OpenRouter

### Frontend Configuration
- **API Endpoint**: `http://localhost:8000/chat`
- **Development Port**: 5173 (Vite default)
- **Styling**: Tailwind CSS with custom gradients

## 🏛️ Architecture

### MCP (Model Context Protocol) Integration
- **Tools Registration**: Weather and news tools registered with MCP
- **Function Calling**: AI automatically selects appropriate tools
- **Response Processing**: Results formatted and returned to user

### API Flow
1. User sends message via React frontend
2. Frontend calls `/chat` endpoint
3. Backend processes with OpenRouter AI
4. AI determines if tools are needed
5. Tools executed if required (weather/news)
6. Response formatted and returned
7. Frontend displays the result

## 🧪 Testing

### Backend Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What'\''s the weather in Tokyo?"}'
```

### Frontend Testing
- Open browser developer tools
- Check network tab for API calls
- Verify CORS configuration
- Test error handling scenarios

## 🌐 Deployment

### Backend Deployment
- Use uvicorn with production settings
- Configure environment variables
- Set up reverse proxy (nginx/apache)
- Enable HTTPS

### Frontend Deployment
- Build: `npm run build`
- Deploy `dist/` folder to hosting service
- Update API endpoint in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Links

- **Repository**: [MCP-AI-Chatbot](https://github.com/sakthivel2264/MCP-AI-Chatbot)
- **OpenRouter**: [https://openrouter.ai/](https://openrouter.ai/)
- **NewsData.io**: [https://newsdata.io/](https://newsdata.io/)
- **MCP Documentation**: [Model Context Protocol](https://modelcontextprotocol.io/)

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/sakthivel2264/MCP-AI-Chatbot/issues) page
2. Create a new issue with detailed information
3. Include error logs and configuration details

---

**Built with ❤️ using MCP, React, and FastAPI**