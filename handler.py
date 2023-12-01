import json
import uuid
import base64
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from make_database import UserData

engine = create_engine("sqlite:///users_offline.sqlite3", echo=True)

# ========== Utils ==========

def add_session(func):
    session = sessionmaker(bind=engine)()
    
    def _inner_func(event, context):
        res = func(event, context, session=session)
        return res

    return _inner_func

def get_body(event):
    required_body = event.get("body", None)

    is_base64_encoded = event.get("isBase64Encoded", False)

    if is_base64_encoded:
        required_body = base64.b64decode(required_body).decode("utf-8")
    else:
        required_body = required_body

    return json.loads(required_body, strict=False)

# ==========================

# CREATE
@add_session
def handle_register_single_user(event, context, session):
    required_body = get_body(event)

    item = {
        "user_id": str(uuid.uuid1())[:20],
        "name": required_body.get("name", ""),
        "age": required_body.get("age", "")
    }

    new_user = UserData(user_id=item["user_id"], name=item["name"], age=item["age"])
    session.add(new_user)
    session.commit()

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }

# READ
@add_session
def handle_fetch_single_user(event, context, session):
    user_id = str(event.get("pathParameters").get("id"))

    trg_user = session.query(UserData).get(user_id)

    if trg_user is None:
        return {"statusCode": 404, "body": f"{user_id} user not found!"}
    
    item = {
        "user_id": user_id,
        "name": trg_user.name,
        "age": trg_user.age
    }

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }

@add_session
def handle_fetch_all_user(event, context, session):
    trg_users = session.query(UserData).all()

    if trg_users is None:
        return {"statusCode": 404, "body": f"No Data!!"}
    
    item = {i: {"user_id": trg_user.user_id, "name": trg_user.name, "age": trg_user.age} 
                                                    for i, trg_user in enumerate(trg_users)}

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }

# UPDATE
@add_session
def handle_update_single_user(event, context, session):
    user_id = str(event.get("pathParameters").get("id"))
    required_body = get_body(event)

    item = {
        "user_id": user_id,
        "name": required_body.get("name", ""),
        "age": required_body.get("age", "")
    }

    trg_user = session.query(UserData).get(item["user_id"])

    if trg_user is None:
        return {"statusCode": 404, "body": f"{user_id} user not found!"}

    item.update(old_name=trg_user.name, old_age=trg_user.age)

    trg_user.name = item["name"]
    trg_user.age = item["age"]
    session.commit()

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }

# DELETE
@add_session
def handle_delete_single_user(event, context, session):
    user_id = str(event.get("pathParameters").get("id"))

    trg_user = session.query(UserData).get(user_id)

    if trg_user is None:
        return {"statusCode": 404, "body": f"{user_id} user not found!"}

    session.delete(trg_user)
    session.commit()

    return {
        "statusCode": 200,
        "body": "Success!!"
    }
