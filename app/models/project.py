from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey, LargeBinary, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

# Many-to-many relationship table for projects and skills
project_skills = Table(
    'project_skills',
    BaseModel.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True),
    Column('relevance_score', Integer, default=5)  # 1-10 scale
)

class ProjectCategory(BaseModel):
    __tablename__ = "project_categories"
    
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Relationship
    projects = relationship("Project", back_populates="category")
    
    def __repr__(self):
        return f"<ProjectCategory(name='{self.name}')>"

class Project(BaseModel):
    __tablename__ = "projects"
    
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    detailed_description = Column(Text)
    technologies = Column(Text, nullable=False)  # Comma-separated string
    
    # Project classification
    category_id = Column(Integer, ForeignKey("project_categories.id"))
    difficulty_level = Column(Integer, default=1)  # 1-5 scale
    
    # Status and URLs
    status = Column(String(20), default="completed", nullable=False)
    is_deployed = Column(Boolean, default=False, nullable=False)
    live_url = Column(String(255))
    github_url = Column(String(255))
    
    # Project details
    client_name = Column(String(100))
    start_date = Column(String(20))
    end_date = Column(String(20))
    featured = Column(Boolean, default=False, nullable=False)
    
    # Storytelling fields - NEW
    problem_statement = Column(Text)
    solution_approach = Column(Text)
    key_challenges = Column(Text)
    lessons_learned = Column(Text)
    results_achieved = Column(Text)
    
    # Relationships
    category = relationship("ProjectCategory", back_populates="projects")
    images = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan")
    skills = relationship("Skill", secondary=project_skills, backref="projects")
    
    @property
    def technologies_list(self):
        """Convert comma-separated string to list"""
        return [tech.strip() for tech in self.technologies.split(",")] if self.technologies else []
    
    @technologies_list.setter
    def technologies_list(self, value):
        """Convert list to comma-separated string"""
        self.technologies = ", ".join(value) if value else ""
    
    @property
    def has_case_study(self):
        """Check if project has storytelling content"""
        return bool(self.problem_statement and self.solution_approach)
    
    def __repr__(self):
        return f"<Project(title='{self.title}', category='{self.category.name if self.category else None}')>"

class ProjectImage(BaseModel):
    __tablename__ = "project_images"
    
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    caption = Column(String(255))
    is_main = Column(Boolean, default=False, nullable=False)
    
    # Image stored as binary data
    image_data = Column(LargeBinary, nullable=False)
    image_type = Column(String(50), nullable=False)
    
    # Relationship
    project = relationship("Project", back_populates="images")
    
    def __repr__(self):
        return f"<ProjectImage(project_id={self.project_id}, is_main={self.is_main})>"