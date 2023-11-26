from fastapi import FastAPI, HTTPException
import asyncpg
import uvicorn
from datetime import datetime

app = FastAPI()

# Параметры подключения к базе данных
DB_HOST = "localhost"  # или адрес вашего сервера БД
DB_USER = "username"  # ваше имя пользователя БД
DB_PASSWORD = "password"  # ваш пароль БД
DB_NAME = "contacts"  # название вашей БД

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
async def add_contact(last_name: str, first_name: str, birthday: str, mail: str):
    conn = await asyncpg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
    await conn.execute(
        "SELECT add_contact($1, $2, $3, $4)",
        last_name, first_name, birthday_date, mail
    )
    await conn.close()
    return {"status": "Contact added successfully"}


@app.put("/update_contact/")
async def update_contact(last_name: str, first_name: str, birthday: str, mail: str):
    conn = await asyncpg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
    await conn.execute(
        "SELECT update_contact($1, $2, $3, $4)",
        last_name, first_name, birthday_date, mail
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
