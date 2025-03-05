import pymongo
from config.settings import settings
from models.models import Employee, Review

client = pymongo.MongoClient(settings.MONGO_DB_TOKEN)
database = client["elcreat-bot"]
employees = database["employees"]

async def new_employee(employee_id: str, name: str, role: str, email):
    filter = {"discord_id": employee_id}
    if employees.count_documents(filter) == 0:
        new_employee = Employee(
            discord_id=employee_id,
            name=name,
            role=role,
            email=email
        ).model_dump()
        employees.insert_one(new_employee)
        return new_employee
    else:
        return False
    
async def check_stars(employee_id: str):
    employee = employees.find_one({"discord_id": employee_id})
    return employee["stars"] if employee else None

async def get_all_employees():
    return list(employees.find())

async def remove_stars(employee_id: str, quantity: float, reason: str):
    employee = employees.find_one({"discord_id": employee_id})
    if not employee:
        return None

    current_stars = float(employee.get("stars", 5.0))
    new_stars = current_stars - quantity
    if new_stars < 0:
        new_stars = 0

    new_review = Review(rating=-quantity, reason=reason)
    
    reviews_list = employee.get("reviews", [])
    reviews_list.append(new_review.model_dump())

    employees.update_one(
        {"discord_id": employee_id},
        {
            "$set": {
                "stars": new_stars,
                "reviews": reviews_list
            }
        }
    )

    return new_stars

async def add_stars(employee_id: str, quantity: float, reason: str):
    employee = employees.find_one({"discord_id": employee_id})
    if not employee:
        return None

    current_stars = float(employee.get("stars", 5.0))
    new_stars = current_stars + quantity
    if new_stars > 5:
        new_stars = 5

    new_review = Review(rating=+quantity, reason=reason)
    
    reviews_list = employee.get("reviews", [])
    reviews_list.append(new_review.model_dump())

    employees.update_one(
        {"discord_id": employee_id},
        {
            "$set": {
                "stars": new_stars,
                "reviews": reviews_list
            }
        }
    )

    return new_stars

async def update_employee(employee_id: str, updates: dict):
    result = employees.update_one(
        {"discord_id": employee_id},
        {"$set": updates}
    )
    if result.matched_count == 0:
        return None
    return employees.find_one({"discord_id": employee_id})
