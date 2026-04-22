# CRM-HCP Module

A full-stack application combining Customer Relationship Management (CRM) and Healthcare Provider (HCP) integration with a conversational AI assistant. The project uses **FastAPI + LangGraph** for the backend and **React + Redux** for the frontend.

## Project Structure

```
crm-hcp-module/
│
├── backend/                          # Python FastAPI + LangGraph
│   ├── requirements.txt              # Python dependencies
│   ├── main.py                       # FastAPI application & routes
│   ├── agent.py                      # LangGraph workflow & ChatGroq setup
│   ├── tools.py                      # The 5 LangGraph tools
│   ├── schemas.py                    # Pydantic models for type safety
│   ├── .env.example                  # Environment variables template
│   └── .gitignore
│
└── frontend/                         # React + Redux with Vite
    ├── package.json                  # Node dependencies
    ├── vite.config.js                # Vite configuration
    ├── src/
    │   ├── App.jsx                   # Main component (2-panel layout)
    │   ├── App.css                   # Main styles
    │   ├── main.jsx                  # React entry point
    │   ├── store/
    │   │   ├── store.js              # Redux store config
    │   │   └── formSlice.js          # Redux slice for form state
    │   └── components/
    │       ├── FormUI.jsx            # Left-side structured form
    │       ├── FormUI.css
    │       ├── ChatUI.jsx            # Right-side chat interface
    │       └── ChatUI.css
    ├── public/
    │   └── index.html
    ├── .gitignore
    └── node_modules/ (after npm install)
```

## Features

### Backend (FastAPI + LangGraph)

- **5 LangGraph Tools:**
  1. `retrieve_patient_info` - Fetch patient data
  2. `retrieve_hcp_info` - Fetch healthcare provider data
  3. `process_patient_records` - CRUD operations on patient records
  4. `schedule_appointment` - Schedule appointments between patients and providers
  5. `generate_medical_report` - Generate medical reports

- **ChatGroq Integration** - AI-powered conversational interface
- **RESTful API Endpoints** - For patients, providers, forms, appointments, and reports
- **Pydantic Models** - Type-safe request/response validation
- **CORS Support** - Cross-origin requests enabled

### Frontend (React + Redux)

- **Dual-Panel Layout:**
  - **Left Panel**: Structured form interface for patient/HCP info and appointments
  - **Right Panel**: Conversational chat interface with the AI assistant

- **Redux State Management:**
  - Form data synchronization
  - Loading states
  - Error handling
  - Form validation

- **Real-time Chat:**
  - Message history
  - Loading indicators
  - Error messages
  - Responsive design

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Update `GROQ_API_KEY` with your actual Groq API key
   ```bash
   cp .env.example .env
   ```

6. **Run the FastAPI server:**
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000` (or `http://localhost:5173` with Vite)

4. **Build for production:**
   ```bash
   npm run build
   ```

## API Endpoints

### Health Check
- `GET /health` - API health status

### Chat
- `POST /api/chat` - Send a message to the AI assistant
  - Request: `{ user_id, message, conversation_id?, context? }`
  - Response: `{ conversation_id, response, metadata, timestamp }`

### Patients
- `POST /api/patients` - Create a new patient
- `GET /api/patients/{patient_id}` - Retrieve patient information

### Healthcare Providers
- `POST /api/providers` - Create a new HCP
- `GET /api/providers/{provider_id}` - Retrieve HCP information

### Forms
- `POST /api/forms/submit` - Submit form data

### Appointments
- `POST /api/appointments` - Schedule an appointment

### Reports
- `POST /api/reports/generate` - Generate a medical report

## Environment Variables

### Backend (.env)

```env
# API Configuration
PORT=8000
HOST=0.0.0.0

# Groq API Key (Required for ChatGroq)
GROQ_API_KEY=your_groq_api_key_here

# Database Configuration (optional)
DATABASE_URL=sqlite:///./test.db

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging
LOG_LEVEL=INFO
```

## Usage

### 1. Start the Backend Server
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

### 2. Start the Frontend Development Server
```bash
cd frontend
npm run dev
```

### 3. Access the Application
- Open `http://localhost:3000` (or `http://localhost:5173`) in your browser
- Use the left panel to fill out forms
- Use the right panel to chat with the AI assistant

## Redux Store Structure

```javascript
store = {
  form: {
    formData: {
      patientInfo: { name, dateOfBirth, email, phone, medicalHistory },
      hcpInfo: { providerName, specialization, licenseNumber, email, phone },
      appointmentInfo: { date, time, reason }
    },
    isLoading: boolean,
    error: string | null,
    lastSubmitted: { type, data, timestamp } | null
  }
}
```

## Available Redux Actions

- `updateFormField(section, field, value)` - Update a single field
- `updateFormSection(section, data)` - Update multiple fields in a section
- `setFormData(data)` - Set complete form data
- `resetForm()` - Reset to initial state
- `resetFormSection(section)` - Reset a specific section
- `setLoading(boolean)` - Update loading state
- `setError(string)` - Set error message
- `setLastSubmitted(data)` - Set last submitted data
- `clearError()` - Clear error message

## Development

### Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Linting

```bash
# Frontend
cd frontend
npm run lint
```

## Deployment

### Backend (FastAPI)
- Use Gunicorn or Uvicorn in production
- Deploy to Heroku, AWS, Google Cloud, etc.

### Frontend (React)
- Run `npm run build` to create optimized production build
- Deploy the `dist/` folder to Netlify, Vercel, AWS S3, etc.

## Troubleshooting

### Backend Issues

1. **ModuleNotFoundError:**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Port Already in Use:**
   - Change PORT in `.env` or run on a different port:
   ```bash
   PORT=8001 python main.py
   ```

3. **GROQ_API_KEY Error:**
   - Ensure `.env` file exists and contains valid GROQ_API_KEY

### Frontend Issues

1. **Cannot GET /:**
   - Make sure frontend is running on correct port
   - Check Vite configuration

2. **API Connection Error:**
   - Verify backend is running on `http://localhost:8000`
   - Check CORS configuration in backend

3. **Port 3000/5173 Already in Use:**
   ```bash
   npm run dev -- --port 3001
   ```

## Contributing

1. Create a feature branch
2. Make your changes
3. Commit with clear messages
4. Push to the repository
5. Create a Pull Request

## License

MIT License - Feel free to use this project for your needs.

## Support

For issues or questions, please create an issue in the repository.

## Dependencies

### Backend
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **langchain** - LLM framework
- **langgraph** - Graph-based workflows
- **langchain-groq** - Groq LLM integration
- **python-dotenv** - Environment variables

### Frontend
- **react** - UI library
- **redux** - State management
- **@reduxjs/toolkit** - Redux utilities
- **react-redux** - React-Redux bindings
- **axios** - HTTP client
- **vite** - Build tool

## Quick Start Summary

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
# Update GROQ_API_KEY in .env
python main.py

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser!
