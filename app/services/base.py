from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.base import BaseModel as DBBaseModel
from app.core.exceptions import NotFoundError

ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a record by ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_by_id_or_404(self, db: Session, id: int) -> ModelType:
        """Get a record by ID or raise 404"""
        obj = self.get_by_id(db, id)
        if not obj:
            raise NotFoundError(self.model.__name__, str(id))
        return obj
    
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """Update an existing record"""
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_by_id(self, db: Session, id: int, obj_in: UpdateSchemaType) -> ModelType:
        """Update a record by ID"""
        db_obj = self.get_by_id_or_404(db, id)
        return self.update(db, db_obj, obj_in)
    
    def delete(self, db: Session, db_obj: ModelType) -> None:
        """Delete a record"""
        db.delete(db_obj)
        db.commit()
    
    def delete_by_id(self, db: Session, id: int) -> None:
        """Delete a record by ID"""
        db_obj = self.get_by_id_or_404(db, id)
        self.delete(db, db_obj)
    
    def exists(self, db: Session, id: int) -> bool:
        """Check if a record exists"""
        return db.query(self.model).filter(self.model.id == id).first() is not None
    
    def count(self, db: Session) -> int:
        """Count total records"""
        return db.query(self.model).count()