from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
    email : List[EmailStr]
    
conf = ConnectionConfig(
    MAIL_USERNAME="username",
    MAIL_PASSWORD="",
    MAIL_FROM="auddwd19@naver.com",
    MAIL_PORT = 587,
    MAIL_SERVER="mail server",
    MAIL_FROM_NAME="JH Hwang",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
    
)

app = FastAPI()

@app.post("/email")
async def simple_send(email : EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)
    
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})






def run():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    run()