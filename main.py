# API REST: https://fastapi.tiangolo.com/tutorial/sql-databases/

import uuid
from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# from faker import Faker
# import random

NIVELES = ["Básico", "Intermedio", "Avanzado"]

# FastAPI instance
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes reemplazar "*" por dominios específicos si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for data validation
class Curso(BaseModel): 
    id: Optional[str] = None
    name: str
    descripction: Optional[str] = None
    duration: int
    level: str

# Simulated database
cursos_db = [
    Curso(id="1", name="Curso 1", description="Descripcion del curso 1", duration=36, level="Basico"),
    Curso(id="2", name="Curso 2", description="Descripcion del curso 2", duration=45, level="Intermedio"),
    Curso(id="3", name="Curso 3", description="Descripcion del curso 3", duration=60, level="Avanzado")
]

# GET all courses
@app.get("/cursos", response_model=list[Curso])
def get_cursos():
    return cursos_db 

# Create a new course
@app.post("/cursos", response_model=Curso)
def create_curso(curso: Curso):
    curso.id = str(uuid.uuid4()) # Generate a unique ID
    # curso.name=Faker.bs().title(),  # genera un nombre tipo "Integración Sinérgica de Plataformas"
    # curso.description=Faker.text(max_nb_chars=100),
    # curso.duration=f"{random.randint(5, 50)}",
    # curso.level=random.choice(NIVELES)
    cursos_db.append(curso)
    return curso

# Retrieve a course by ID
@app.get("/cursos/{curso_id}", response_model=Curso)
def get_curso(curso_id: str):
    for curso in cursos_db:
        if curso.id == curso_id:
            return curso
    if curso_id == None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return None

# Update a course by ID
@app.put("/cursos/{curso_id}", response_model=Curso)
def update_curso(curso_id: str, curso: Curso):
    for index, existing_curso in enumerate(cursos_db):
        if existing_curso.id == curso_id:
            cursos_db[index] = curso
            return curso
    raise HTTPException(status_code=404, detail="Curso no encontrado")

# Delete a course by ID
@app.delete("/cursos/{curso_id}", response_model=Curso)
def delete_curso(curso_id: str):
    for index, curso in enumerate(cursos_db):
        if curso.id == curso_id:
            deleted_curso = cursos_db.pop(index)
            return deleted_curso
    raise HTTPException(status_code=404, detail="Curso no encontrado")

# Run the application with: uvicorn main:app --reload
# In Postman -> http://127.0.0.1:8000