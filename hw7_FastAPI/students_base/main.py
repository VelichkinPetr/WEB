# Данные: простая база студентов.

# STUDENTS = [
#  {
#   "id": int,
#   "name": str,
#   "group": str,
#   "grades": [
#    {
#     "subject": str,
#     "value": int
#    }
#   ]
#  }
# ]

# Ограничения: 
# поле "value" внутри "grades" может содержать значение только от 1 до 5
# "name" и "group" - обязательные поля для студентов

# 1. Реализовать CRUD для студентов.
# 2. Добавить маршрут GET /students/{id}/avg-grade — вернуть средний балл.
# 3. Добавить фильтрацию GET /students?group=IVT-101 — фильтрация по группе.

from typing import Dict, Any
from fastapi import FastAPI, status, HTTPException
from model import Student, Grade
from services import StudentService


app = FastAPI()
student_service = StudentService()


@app.post('/students', status_code=status.HTTP_200_OK)
def create_student(data: Dict[str, Any]):
    return student_service.create(data)


@app.get('/students', status_code=status.HTTP_200_OK)
def get_students(id: int = None, group: str = None):
    if id is None and group is None:
        return {
                'all students':student_service.get_all()
        }
    
    elif id is not None and group is None:
                    return {
                            'student by id':student_service.get_by_id(id)
                    }
                
    elif id is None and group is not None:
         return {
                'student by group':student_service.get_by_group(group)
        }
    elif id is not None and group is not None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='NOT use ID with GROUP')
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student with id not found')


@app.put('/students/{id}', status_code=status.HTTP_200_OK)
def update_student(id: int, data: Dict[str, Any]):
    if not data.keys():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Update is empty')
    
    update_student = student_service.update(id, data)

    if not update_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student with id not found')


@app.delete('/student', status_code=status.HTTP_200_OK)
def delete_student(id: int = None):
    if student_service.is_empty():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Student BD is empty')
    if id is None:
        student_service.delete_all()
    else:
        if not student_service.delete_by_id(id): 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student with id not found')

    
@app.get('/students/{id}/avg-grade')
def get_student_avg_grade(id: int):
    student = student_service.get_by_id(id)

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student with id not found')
    
    if student_service.grade_is_empty(*student):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Grades is empty')
    
    avg_grade = student_service.get_avg_grade(*student)
    return {
            "name": student[0].name,
            "group": student[0].group,
            "avg_grade":avg_grade
        }
    