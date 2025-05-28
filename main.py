from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database
from database import get_db
from models import generate_responses
from datetime import datetime
import uuid

app = FastAPI()

@app.post("/generate", response_model=schemas.GenerateResponse)
async def generate_response(
    request: schemas.GenerateRequest, 
    db: Session = Depends(get_db)
):
    try:
        # Generate AI responses
        casual, formal = generate_responses(request.query)
        
        # Save to database
        prompt = database.Prompt(
            user_id=request.user_id,
            query=request.query,
            casual_response=casual,
            formal_response=formal
        )
        db.add(prompt)
        db.commit()
        db.refresh(prompt)
        
        return {
            "casual_response": casual,
            "formal_response": formal
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=schemas.HistoryResponse)
async def get_history(user_id: str, db: Session = Depends(get_db)):
    try:
        history = db.query(database.Prompt).filter(
            database.Prompt.user_id == user_id
        ).order_by(database.Prompt.created_at.desc()).all()
        
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))