import asyncio
import sqlite3
import aiosmtplib

from email.message import EmailMessage
from more_itertools import chunked


LIMITATION = 20


class Person:
    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email
        self.email_msg = f'''Уважаемый {self.name}!
        Спасибо, что пользуетесь нашим сервисом объявлений.'''


# генератор людей
def gen_peoples():
    con = sqlite3.connect('contacts.db')
    cur = con.cursor()
    sql = 'select first_name, last_name, email from contacts'
    peoples = [Person(row[0], row[1], row[2]) for row in cur.execute(sql)]
    for person in peoples:
        yield person


# функция генерации сообщения
async def send_email(email, msg):
    message = EmailMessage()
    message["From"] = "root@localhost"
    message["To"] = email
    message["Subject"] = "Hello World!"
    message.set_content(msg)

    await aiosmtplib.send(message, port=1025)


async def main():
    for persons in chunked(gen_peoples(), 20):
        email_tasks = [asyncio.create_task(send_email(person.email, person.email_msg))
                       for person in persons]
        await asyncio.gather(*email_tasks)


if __name__ == '__main__':
    asyncio.run(main())

