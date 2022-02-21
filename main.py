import asyncio
import sqlite3
import aiosmtplib

from email.message import EmailMessage


class Person:
    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email
        self.email_masg = f'''Уважаемый {self.name}!
        Спасибо, что пользуетесь нашим сервисом объявлений.'''


# генератор людей
def gen_pipel():
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
    # print(email)
    await aiosmtplib.send(message, hostname="127.0.0.1", port=1025)


async def email_send():
    email_tasks = [asyncio.create_task(send_email(person.email, person.email_masg))
                   for person in gen_pipel()]
    print(email_tasks)
    await asyncio.wait(email_tasks)
    # email_tasks = [asyncio.create_task(send_email(person.email, person.email_masg))
    #                for person in gen_pipel()]
    # email_send = asyncio.gather(*email_tasks)
    # # for _email in email_send:
    # #     yield _email


async def main():
    email_tasks = [asyncio.create_task(send_email(person.email, person.email_masg))
                   for person in gen_pipel()]
    print(email_tasks)
    await asyncio.gather(*email_tasks)

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(email_send())
    # loop.close()

# генератор людей для отправки
if __name__ == '__main__':
    asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # email_tasks = [asyncio.create_task(send_email(person.email, person.email_masg))
    #                for person in gen_pipel()]
    # email_tasks = [send_email(person.email, person.email_masg)
    #                for person in gen_pipel()]

    # loop.run_until_complete(asyncio.gather(*email_tasks))
    # loop.run_until_complete(email_send())
    # loop.close()
