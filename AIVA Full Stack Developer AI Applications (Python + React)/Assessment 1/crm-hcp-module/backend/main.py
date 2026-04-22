"""FastAPI application and routes for CRM-HCP module"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import uvicorn
from typing import Optional, Dict, Any, List
import logging
from sqlalchemy.orm import Session

# Import schemas, agent, and database
from schemas import ChatRequest, ChatResponse, FormData, PatientInfo, HCPInfo, Message
from agent import process_message, initialize_agent
from database import get_db, HCP, Interaction, AIInsight, init_db

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app (without docs to hide GET/POST/PUT from Chrome)
app = FastAPI(
    title="CRM-HCP Module API",
    description="API for Customer Relationship Management and Healthcare Provider integration",
    version="1.0.0",
    docs_url=None,  # Disable Swagger UI docs
    redoc_url=None  # Disable ReDoc
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CRM-HCP Module API",
        "version": "1.0.0"
    }


# Chat endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process chat message through the LangGraph agent
    
    Args:
        request: ChatRequest object containing user_id, message, and optional context
        
    Returns:
        ChatResponse with agent response and metadata
    """
    try:
        logger.info(f"Processing chat message from user: {request.user_id}")
        
        # Process message through agent
        result = await process_message(
            user_id=request.user_id,
            message=request.message,
            conversation_id=request.conversation_id,
            context=request.context
        )
        
        response = ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            metadata=result.get("metadata", {})
        )
        
        logger.info(f"Chat response generated: {result['status']}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Patient information endpoints
@app.post("/api/patients")
async def create_patient(patient_info: PatientInfo):
    """Create a new patient record"""
    try:
        logger.info(f"Creating patient: {patient_info.name}")
        return {
            "status": "success",
            "message": "Patient created successfully",
            "patient_id": patient_info.patient_id,
            "data": patient_info.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/patients/{patient_id}")
async def get_patient(patient_id: str):
    """Retrieve patient information"""
    try:
        # Mock implementation - replace with actual database query
        logger.info(f"Retrieving patient: {patient_id}")
        return {
            "patient_id": patient_id,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Healthcare Provider endpoints
@app.post("/api/providers")
async def create_provider(hcp_info: HCPInfo, db: Session = Depends(get_db)):
    """Create a new healthcare provider record"""
    try:
        logger.info(f"Creating HCP: {hcp_info.name}")

        # Check if provider already exists
        existing_hcp = db.query(HCP).filter(HCP.provider_id == hcp_info.provider_id).first()
        if existing_hcp:
            raise HTTPException(status_code=400, detail="Provider ID already exists")

        # Create new HCP
        db_hcp = HCP(
            provider_id=hcp_info.provider_id,
            name=hcp_info.name,
            specialization=hcp_info.specialization,
            license_number=hcp_info.license_number,
            email=hcp_info.email,
            phone=hcp_info.phone
        )

        db.add(db_hcp)
        db.commit()
        db.refresh(db_hcp)

        return {
            "status": "success",
            "message": "Provider created successfully",
            "provider_id": db_hcp.provider_id,
            "data": {
                "id": db_hcp.id,
                "provider_id": db_hcp.provider_id,
                "name": db_hcp.name,
                "specialization": db_hcp.specialization,
                "license_number": db_hcp.license_number,
                "email": db_hcp.email,
                "phone": db_hcp.phone
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating provider: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/providers/{provider_id}")
async def get_provider(provider_id: str, db: Session = Depends(get_db)):
    """Retrieve healthcare provider information"""
    try:
        logger.info(f"Retrieving HCP: {provider_id}")

        hcp = db.query(HCP).filter(HCP.provider_id == provider_id).first()
        if not hcp:
            raise HTTPException(status_code=404, detail="Provider not found")

        return {
            "provider_id": hcp.provider_id,
            "name": hcp.name,
            "specialization": hcp.specialization,
            "license_number": hcp.license_number,
            "email": hcp.email,
            "phone": hcp.phone,
            "created_at": hcp.created_at,
            "updated_at": hcp.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving provider: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/providers")
async def get_all_providers(db: Session = Depends(get_db)):
    """Retrieve all healthcare providers"""
    try:
        hcps = db.query(HCP).all()
        return {
            "providers": [
                {
                    "provider_id": hcp.provider_id,
                    "name": hcp.name,
                    "specialization": hcp.specialization,
                    "email": hcp.email,
                    "phone": hcp.phone
                } for hcp in hcps
            ],
            "total": len(hcps)
        }
    except Exception as e:
        logger.error(f"Error retrieving providers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/providers/{provider_id}")
async def update_provider(provider_id: str, hcp_info: HCPInfo, db: Session = Depends(get_db)):
    """Update healthcare provider information"""
    try:
        logger.info(f"Updating HCP: {provider_id}")

        hcp = db.query(HCP).filter(HCP.provider_id == provider_id).first()
        if not hcp:
            raise HTTPException(status_code=404, detail="Provider not found")

        # Update fields
        for field, value in hcp_info.dict().items():
            if hasattr(hcp, field) and value is not None:
                setattr(hcp, field, value)

        db.commit()
        db.refresh(hcp)

        return {
            "status": "success",
            "message": "Provider updated successfully",
            "data": {
                "provider_id": hcp.provider_id,
                "name": hcp.name,
                "specialization": hcp.specialization,
                "email": hcp.email,
                "phone": hcp.phone
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating provider: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/providers/{provider_id}")
async def delete_provider(provider_id: str, db: Session = Depends(get_db)):
    """Delete healthcare provider"""
    try:
        logger.info(f"Deleting HCP: {provider_id}")

        hcp = db.query(HCP).filter(HCP.provider_id == provider_id).first()
        if not hcp:
            raise HTTPException(status_code=404, detail="Provider not found")

        db.delete(hcp)
        db.commit()

        return {
            "status": "success",
            "message": "Provider deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting provider: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Form submission endpoint
@app.post("/api/forms/submit")
async def submit_form(form_data: FormData, db: Session = Depends(get_db)):
    """Submit form data - creates HCP interactions"""
    try:
        logger.info(f"Processing form submission: {form_data.form_type}")

        if form_data.form_type == "hcp_interaction":
            # Extract HCP interaction data
            hcp_id = form_data.data.get("hcp_id")
            interaction_type = form_data.data.get("interaction_type")
            notes = form_data.data.get("notes")
            sentiment = form_data.data.get("sentiment")
            samples_provided = form_data.data.get("samples_provided")

            if not hcp_id:
                raise HTTPException(status_code=400, detail="HCP ID is required")

            # Find HCP
            hcp = db.query(HCP).filter(HCP.provider_id == hcp_id).first()
            if not hcp:
                raise HTTPException(status_code=404, detail="HCP not found")

            # Create interaction
            interaction = Interaction(
                hcp_id=hcp.id,
                interaction_type=interaction_type,
                notes=notes,
                sentiment=sentiment,
                samples_provided=samples_provided
            )

            db.add(interaction)
            db.commit()
            db.refresh(interaction)

            return {
                "status": "success",
                "message": "HCP interaction logged successfully",
                "interaction_id": interaction.id,
                "data": {
                    "hcp_id": hcp_id,
                    "interaction_type": interaction_type,
                    "notes": notes,
                    "sentiment": sentiment,
                    "samples_provided": samples_provided
                }
            }

        elif form_data.form_type == "hcp_info":
            # Handle HCP creation/update
            hcp_data = form_data.data
            provider_id = hcp_data.get("provider_id")

            if not provider_id:
                raise HTTPException(status_code=400, detail="Provider ID is required")

            # Check if HCP exists
            existing_hcp = db.query(HCP).filter(HCP.provider_id == provider_id).first()

            if existing_hcp:
                # Update existing HCP
                for key, value in hcp_data.items():
                    if hasattr(existing_hcp, key) and value is not None:
                        setattr(existing_hcp, key, value)
                db.commit()
                db.refresh(existing_hcp)
                message = "HCP information updated successfully"
            else:
                # Create new HCP
                new_hcp = HCP(**hcp_data)
                db.add(new_hcp)
                db.commit()
                db.refresh(new_hcp)
                message = "HCP created successfully"

            return {
                "status": "success",
                "message": message,
                "provider_id": provider_id
            }

        else:
            return {
                "status": "success",
                "message": "Form submitted successfully",
                "submission_id": f"FORM_{form_data.user_id}_{form_data.form_type}",
                "data": form_data.dict()
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing form submission: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Interaction endpoints
@app.get("/api/interactions/{hcp_id}")
async def get_hcp_interactions(hcp_id: str, db: Session = Depends(get_db)):
    """Get all interactions for a specific HCP"""
    try:
        logger.info(f"Retrieving interactions for HCP: {hcp_id}")

        hcp = db.query(HCP).filter(HCP.provider_id == hcp_id).first()
        if not hcp:
            raise HTTPException(status_code=404, detail="HCP not found")

        interactions = db.query(Interaction).filter(Interaction.hcp_id == hcp.id).all()

        return {
            "hcp_id": hcp_id,
            "hcp_name": hcp.name,
            "interactions": [
                {
                    "id": interaction.id,
                    "interaction_type": interaction.interaction_type,
                    "notes": interaction.notes,
                    "sentiment": interaction.sentiment,
                    "samples_provided": interaction.samples_provided,
                    "follow_up_date": interaction.follow_up_date,
                    "created_at": interaction.created_at
                } for interaction in interactions
            ],
            "total": len(interactions)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving interactions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interactions")
async def create_interaction(interaction_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new interaction"""
    try:
        logger.info(f"Creating interaction for HCP: {interaction_data.get('hcp_id')}")

        hcp_id = interaction_data.get("hcp_id")
        if not hcp_id:
            raise HTTPException(status_code=400, detail="HCP ID is required")

        hcp = db.query(HCP).filter(HCP.provider_id == hcp_id).first()
        if not hcp:
            raise HTTPException(status_code=404, detail="HCP not found")

        interaction = Interaction(
            hcp_id=hcp.id,
            interaction_type=interaction_data.get("interaction_type"),
            notes=interaction_data.get("notes"),
            sentiment=interaction_data.get("sentiment"),
            samples_provided=interaction_data.get("samples_provided"),
            follow_up_date=interaction_data.get("follow_up_date")
        )

        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        return {
            "status": "success",
            "message": "Interaction created successfully",
            "interaction_id": interaction.id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating interaction: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Appointment endpoints
@app.post("/api/appointments")
async def schedule_appointment(appointment_data: Dict[str, Any]):
    """Schedule an appointment"""
    try:
        logger.info(f"Scheduling appointment")
        return {
            "status": "confirmed",
            "appointment_id": "APT_001",
            "message": "Appointment scheduled successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Report generation endpoint
@app.post("/api/reports/generate")
async def generate_report(report_data: Dict[str, Any]):
    """Generate medical report"""
    try:
        logger.info(f"Generating report")
        return {
            "status": "generated",
            "report_id": "RPT_001",
            "message": "Report generated successfully",
            "content": "Report content here"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Error handler
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(exc)}
    )


if __name__ == "__main__":
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Could not initialize database: {e}")

    # Initialize agent
    try:
        initialize_agent()
        logger.info("Agent initialized successfully")
    except Exception as e:
        logger.warning(f"Could not initialize agent: {e}")

    # Run the server
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

app = FastAPI(title="HCP CRM Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """Handles conversational input, triggers LangGraph, and returns AI text + structured data."""
    
    # Run the LangGraph agent
    config = {"configurable": {"thread_id": req.thread_id}}
    state = agent_executor.invoke({"messages": [HumanMessage(content=req.message)]}, config)
    
    ai_response = state["messages"][-1].content
    extracted_data = {}

    # Check the tool calls in the state to extract the structured JSON payload
    # This syncs the chat with the React form UI
    for message in reversed(state["messages"]):
        if message.type == "tool" and "DB_SUCCESS" in message.content:
            try:
                payload_str = message.content.split("Payload: ")[1]
                extracted_data = json.loads(payload_str)
                break
            except (IndexError, json.JSONDecodeError):
                continue
                
    return {
        "reply": ai_response,
        "extracted_data": extracted_data
    }