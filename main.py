import hashlib

import jwt
from fastapi import (Depends, FastAPI, File, Form, HTTPException, Request,
                     UploadFile, status)
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import Base, engine, sessionlocal
from models import company_info, user_info
from schemas import (Token, company_info_schema, user_info_login_schema,
                     user_info_schema)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

JWT_SECRETS = '9a60b9565dd8947f4dcee97b99896a9c8e323673634874b4555534930429a041'

templates = Jinja2Templates(directory='templates')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def index(request:Request):
    return templates.TemplateResponse("/index.html", {"request":request})

@app.get("/login")
def login_user(request:Request):
    return templates.TemplateResponse("/login.html", {"request":request})
    
@app.post("/login", response_model=Token)
def login(username: str = Form(...), password: str = Form(...)):
    password_hashed = hashlib.md5(password.encode())
    password_final = password_hashed.hexdigest()

    info = sessionlocal.query(user_info).get(username)

    if info and info.password == password_final:
        user_dict = {
            "email": info.email,
            "password" : info.password
        }
        encoded = jwt.encode(user_dict, JWT_SECRETS, algorithm='HS256')
        return {"access_token": encoded, "token_type": "bearer"}

    # check if email exists. If not, raise exception and return 404 not found response
    elif not info:
        raise HTTPException(status_code=404, detail=f"The user '{username}' is not registered with us.")
    
    elif info.password != password_final:
        return {"Error": "Incorrect Password"}


@app.get("/signup")
def signup(request:Request):
    return templates.TemplateResponse("/signup.html", {"request":request})


@app.post("/signup")
def create_user(photo: UploadFile = File(media_type='img') , name: str = Form(), email: str = Form(), password: str = Form(), company: str = Form("")):
    password_hashed = hashlib.md5(password.encode())
    password_final = password_hashed.hexdigest()
    if photo.content_type not in ["image/png", "image/jpg", "image/jpeg"]:
        raise HTTPException(400, detail="Invalid document type")
    
    contents = photo.file.read()
    with open(f'images/{name}.png', 'wb') as file:
        content = file.write(contents)
        if company == "":
            c_db = company_info(company= "NA", employee_email= email)
        else:
            c_db = company_info(company= company, employee_email= email)
    userdb = user_info(name = name, email = email, password = password_final, photo = f'images/{name}.png')

    info = sessionlocal.query(user_info).get(email)
    if info:
        return {"Error": "User is already registered"}
  
    sessionlocal.add(userdb)
    sessionlocal.add(c_db)
    sessionlocal.commit()

    return {"Message": "User has been created. Please login from the login page."}

@app.get("/users")
def get_users(request:Request):
    return templates.TemplateResponse("/users.html", {"request":request})

@app.post("/users")
async def users_data(request:Request):
    query = "SELECT users.name, users.email, users.password, users.photo, users.admin_account, companies.company FROM users INNER JOIN companies ON users.email=companies.employee_email"
    users_ = sessionlocal.execute(query).all()
    return users_


@app.post("/users/me")
async def users(token: str = Depends(oauth2_scheme)):
    try:
        data = jwt.decode(token, JWT_SECRETS, algorithms='HS256') #type:ignore
        query = f"SELECT users.name, users.email, users.password, users.photo, users.admin_account, companies.company FROM users INNER JOIN companies ON users.email=companies.employee_email WHERE(email='{data.get('email')}')"
        user = sessionlocal.execute(query).all()

        # user_data = sessionlocal.query(user_info).get(data.get('email'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='Invalid Token')
    else:
        return user
    
@app.put("/users/me/update")
async def update_details(token: str = Depends(oauth2_scheme), photo: UploadFile = File(media_type='img') , name: str = Form(), email: str = Form(), Old_password : str = Form("", description="Old password is required for changing password"), password: str = Form(""), company: str = Form("")):
    password_hashed = hashlib.md5(Old_password.encode())
    password_final = password_hashed.hexdigest()
    data = jwt.decode(token, JWT_SECRETS, algorithms='HS256') #type:ignore
    user = sessionlocal.query(user_info).get(data.get('email'))
    com_info = sessionlocal.query(company_info).get(data.get('email'))
    if data:
        if password and password_final != user.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Old Password did not match.')
        else:
            if photo.content_type not in ["image/png", "image/jpg", "image/jpeg"]:
                raise HTTPException(400, detail="Invalid document type")
    
            contents = photo.file.read()
            if company:
                com_info.company = company
            with open(f'images/{name}.png', 'wb') as file:
                content = file.write(contents)
            if password != "":
                password_hashed1 = hashlib.md5(password.encode())
                password_final1 = password_hashed.hexdigest()
                user.password = password_final1
            user.email = email
            user.name = name
            user.photo = f'images/{name}.png'
            sessionlocal.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token or Unauthorized User')
    return {"Message": "The profile has been updated."}
