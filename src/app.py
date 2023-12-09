from fastapi import FastAPI, HTTPException
import asyncpg
import uvicorn
from datetime import datetime, date
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Параметры подключения к базе данных
DB_HOST = "localhost"  # или адрес вашего сервера БД
DB_USER = "postgres"  # ваше имя пользователя БД
DB_PASSWORD = "Zbujhm2001."  # ваш пароль БД
DB_NAME = "contacts"  # название вашей БД

class Contact(BaseModel):
    last_name: str
    first_name: str
    birthday: date
    mail: str

async def create_database():
    conn = await asyncpg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database="postgres"  # Подключаемся к базе postgres для создания новой БД
    )
    
    # Создание базы данных
    await conn.execute("DROP DATABASE contacts;")
    await conn.execute("CREATE DATABASE contacts;")
    await conn.close()

    # Подключаемся к новой базе данных
    conn = await asyncpg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )

    # Выполнение SQL-команд для создания таблиц и функций
    with open("DB.sql", "r") as file:
        sql_script = file.read()
        await conn.execute(sql_script)

    await conn.close()

async def startup_event():
    await create_database()

async def shutdown_event():
    pass

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

@app.get("/contacts/")
async def get_contacts():
    conn = await asyncpg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    rows = await conn.fetch("SELECT * FROM contacts")
    await conn.close()
    return rows


@app.get("/contacts_audit/")
async def get_contacts_audit():
    conn = await asyncpg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    rows = await conn.fetch("SELECT * FROM contacts_audit")
    await conn.close()
    return rows


@app.post("/add_contact/")
async def add_contact(contact: Contact):
    conn = await asyncpg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    await conn.execute(
        "SELECT add_contact($1, $2, $3, $4)",
        contact.last_name, contact.first_name, contact.birthday, contact.mail
    )
    await conn.close()
    return {"status": "Contact added successfully"}


@app.put("/update_contact/")
async def update_contact(contact: Contact):
    conn = await asyncpg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    await conn.execute(
        "SELECT update_contact($1, $2, $3, $4)",
        contact.last_name, contact.first_name, contact.birthday, contact.mail
    )
    await conn.close()
    return {"status": "Contact updated successfully"}


@app.delete("/delete_contact/{last_name}")
async def delete_contact(last_name: str):
    conn = await asyncpg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    await conn.execute("SELECT delete_contact($1)", last_name)
    await conn.close()
    return {"status": "Contact deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
