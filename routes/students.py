from fastapi import APIRouter, HTTPException, Query, Path
from bson import ObjectId
from db import students_collection

router = APIRouter()

@router.post("/students", status_code=201)
async def create_student(student_data: dict):

    required_fields = ['name', 'age', 'address']
    missing_fields = [field for field in required_fields if field not in student_data]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {missing_fields}")
    
    result = students_collection.insert_one(student_data)
    
    return {"id": str(result.inserted_id)}

@router.get("/students", response_model=dict)
async def list_students(country: str = Query(None, description="Filter by country"), age: int = Query(None, description="Filter by age")):
    
    filters = {}
    if country:
        filters['address.country'] = country
    if age is not None:
        filters['age'] = {'$gte': age}
    
    students = list(students_collection.find(filters, {'_id': 0}))
    
    return {"data": students}

@router.get("/students/{id}", response_model=dict)
async def get_student(id: str = Path(..., description="The ID of the student")):

    student = students_collection.find_one({"_id": ObjectId(id)}, {'_id': 0})
    
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@router.patch("/students/{id}", status_code=204)
async def update_student(id: str = Path(..., description="The ID of the student"), student_data: dict = None):

    existing_student = students_collection.find_one({"_id": ObjectId(id)})
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = {key: value for key, value in student_data.items() if value is not None} if student_data else {}
    if update_data:
        students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    return {}

@router.delete("/students/{id}", status_code=200)
async def delete_student(id: str = Path(..., description="The ID of the student")):

    existing_student = students_collection.find_one({"_id": ObjectId(id)})
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    students_collection.delete_one({"_id": ObjectId(id)})
    
    return {}
