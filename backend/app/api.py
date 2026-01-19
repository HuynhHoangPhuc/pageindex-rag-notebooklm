from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.db import User, Document, get_session
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.rag import rag_client
import shutil
import os
from tempfile import NamedTemporaryFile

router = APIRouter()

@router.post("/auth/register")
def register(user: User, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.hashed_password = get_password_hash(user.hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User created successfully"}

@router.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/upload")
def upload_file(
    file: UploadFile = File(...), 
    user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    # Save file locally first
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Upload to PageIndex
    try:
        response = rag_client.upload_file(file_location)
        # Check for doc_id in dict or attribute
        if isinstance(response, dict):
            pageindex_id = response.get('doc_id') or response.get('id')
        else:
            pageindex_id = getattr(response, 'doc_id', None) or getattr(response, 'id', None)
            
        if not pageindex_id:
             pageindex_id = "mock_id" 
             print("Warning: Could not parse doc_id from upload response") 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PageIndex Upload Failed: {str(e)}")

    doc = Document(filename=file.filename, pageindex_file_id=str(pageindex_id), user_id=user.id, upload_status="processed")
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc

@router.post("/chat")
def chat(
    query: str, 
    file_ids: list[str], # PageIndex IDs
    user: User = Depends(get_current_user)
):
    try:
        response = rag_client.query(query, file_ids)
        # Parse response to string
        # Assuming response is object with 'choices' or similar (OpenAI style) or just text
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Query Failed: {str(e)}")

@router.get("/documents")
def list_documents(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    docs = session.exec(select(Document).where(Document.user_id == user.id)).all()
    return docs
