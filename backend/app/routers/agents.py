from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from app.core.database import get_db
from app.models.models import User, Agent, Rating, Review
from app.schemas.schemas import (
    AgentCreate, AgentUpdate, AgentResponse, AgentExecuteRequest, AgentExecuteResponse
)
from app.routers.auth import get_current_active_user
from app.services.agent_executor import execute_agent_code

router = APIRouter()


def get_agent_with_stats(db: Session, agent_id: int):
    """Get agent with average rating"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        return None
    
    # Calculate average rating
    avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.agent_id == agent_id).scalar()
    
    # Create response dict
    agent_dict = {
        "id": agent.id,
        "name": agent.name,
        "description": agent.description,
        "code": agent.code,
        "tags": agent.tags,
        "creator_id": agent.creator_id,
        "parent_id": agent.parent_id,
        "version": agent.version,
        "is_public": agent.is_public,
        "is_active": agent.is_active,
        "usage_count": agent.usage_count,
        "created_at": agent.created_at,
        "updated_at": agent.updated_at,
        "average_rating": float(avg_rating) if avg_rating else None,
        "creator_username": agent.creator.username if agent.creator else None
    }
    
    return agent_dict


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent: AgentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_agent = Agent(
        name=agent.name,
        description=agent.description,
        code=agent.code,
        tags=agent.tags,
        is_public=agent.is_public,
        creator_id=current_user.id
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    
    return get_agent_with_stats(db, db_agent.id)


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    tags: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Agent).filter(Agent.is_public == True, Agent.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                Agent.name.ilike(f"%{search}%"),
                Agent.description.ilike(f"%{search}%")
            )
        )
    
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]
        for tag in tag_list:
            query = query.filter(Agent.tags.ilike(f"%{tag}%"))
    
    agents = query.offset(skip).limit(limit).all()
    
    # Get agents with stats
    agents_with_stats = []
    for agent in agents:
        agent_dict = get_agent_with_stats(db, agent.id)
        if agent_dict:
            agents_with_stats.append(agent_dict)
    
    return agents_with_stats


@router.get("/my-agents", response_model=List[AgentResponse])
async def list_my_agents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    agents = db.query(Agent).filter(
        Agent.creator_id == current_user.id,
        Agent.is_active == True
    ).offset(skip).limit(limit).all()
    
    agents_with_stats = []
    for agent in agents:
        agent_dict = get_agent_with_stats(db, agent.id)
        if agent_dict:
            agents_with_stats.append(agent_dict)
    
    return agents_with_stats


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent_dict = get_agent_with_stats(db, agent_id)
    if not agent_dict:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent_dict


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if user is creator or admin
    if db_agent.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update fields
    update_data = agent_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_agent, field, value)
    
    db.commit()
    db.refresh(db_agent)
    
    return get_agent_with_stats(db, db_agent.id)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if user is creator or admin
    if db_agent.creator_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Soft delete
    db_agent.is_active = False
    db.commit()
    
    return None


@router.post("/{agent_id}/fork", response_model=AgentResponse)
async def fork_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Get parent agent
    parent_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not parent_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Create forked agent
    forked_agent = Agent(
        name=f"{parent_agent.name} (Fork)",
        description=parent_agent.description,
        code=parent_agent.code,
        tags=parent_agent.tags,
        creator_id=current_user.id,
        parent_id=parent_agent.id,
        version="1.0.0"
    )
    db.add(forked_agent)
    db.commit()
    db.refresh(forked_agent)
    
    return get_agent_with_stats(db, forked_agent.id)


@router.post("/execute", response_model=AgentExecuteResponse)
def execute_agent(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    agent = db.query(Agent).filter(Agent.id == request.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Execute agent code (now synchronous)
    result = execute_agent_code(agent.code, request.input_data)
    
    # Increment usage count
    agent.usage_count += 1
    db.commit()
    
    return result
