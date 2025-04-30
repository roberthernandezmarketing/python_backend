# API REST: https://fastapi.tiangolo.com/tutorial/sql-databases/

import uuid
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

# FastAPI instance
app = FastAPI() 

# Pydantic model for data validation
class Curso(BaseModel): 
    id: Optional[str] = None
    name: str
    descripction: Optional[str] = None
    duration: int
    level: str

# Simulated database
cursos_db = [
    Curso(id="1", name="Curso 1", descripction="Descripcion del curso 1", duration=30, level="Basico"),
    Curso(id="2", name="Curso 2", descripction="Descripcion del curso 2", duration=45, level="Intermedio"),
    Curso(id="3", name="Curso 3", descripction="Descripcion del curso 3", duration=60, level="Avanzado")
]

# GET all courses
@app.get("/cursos", response_model=list[Curso])
def get_cursos():
    return cursos_db 

# Create a new course
@app.post("/cursos", response_model=Curso)
def create_curso(curso: Curso):
    curso.id = str(uuid.uuid4()) # Generate a unique ID
    # curso.id = 5 # Generate a unique ID
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