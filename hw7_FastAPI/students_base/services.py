from typing import Dict, Any

from model import Student, Grade


class StudentService():

    def __init__(self):
        self.students_bd: list[Student] = []
        self.student_id = 1
        self.grade_service = GradeService()

    def create(self, data: Dict[str, Any]) -> Student:
        data['id'] = self.student_id
        data['grades'] = self.grade_service.create(data)

        new_student = Student(**data)
        self.students_bd.append(new_student)
        self.student_id += 1
        return new_student
    
    def get_all(self) -> list[Student]:
        return self.students_bd
    
    def get_by_id(self, id: int) -> list[Student]:
        return [student for student in self.students_bd if student.id == id]
    
    def get_by_group(self, group: str) -> list[Student]:
        return [student for student in self.students_bd if student.group == group]
    
    def update(self, id: int, data: Dict[str, Any]) -> Student:
        for student in self.students_bd:
            if student.id == id:
                if {'grades'} <= data.keys():
                    self.grade_service.update(student, data)
                
                if {'name'} <= data.keys():
                    student.name = data['name']
                    
                if {'group'} <= data.keys():
                    student.group = data['group']
                return student
            
    def delete_all(self):
        self.students_bd.clear()

    def delete_by_id(self, id: int):
        for i,student in enumerate(self.students_bd):
            if student.id == id:
                del self.students_bd[i]
                return True
        return False
    
    def is_empty(self):
        return True if len(self.students_bd) == 0 else False
    
    def grade_is_empty(self, student: Student):
        return self.grade_service.is_empty(student)

    def get_avg_grade(self, student: Student):
        return self.grade_service.avg_grade(student)

    
class GradeService():

    def create(self, data: list[Dict[str, Any]]) -> Grade:
        grades = []
        for grade in data['grades']:
            grades.append(Grade(**grade))
        return grades
    
    def update(self,student: Student, data: list[Dict[str, Any]]):
        for grade in data['grades']:
            for student_grade in student.grades:
                if grade.get('subject') == student_grade.subject:
                    student_grade.value = grade.get('value')
    
    def is_empty(self, student: Student):
        return True if len(student.grades) == 0 else False
    
    def avg_grade(self, student: Student):
        values = [grade.value for grade in student.grades]
        return sum(values) / len(values)