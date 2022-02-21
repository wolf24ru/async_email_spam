import asyncio
from email.message import EmailMessage

import aiosmtplib

async def send_hello_world():
    message = EmailMessage()
    message["From"] = "root@localhost"
    message["To"] = "somebody@example.com"
    message["Subject"] = "Hello World!"
    message.set_content("Sent via aiosmtplib")

    await aiosmtplib.send(message, hostname="localhost", port=1025)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(send_hello_world())
