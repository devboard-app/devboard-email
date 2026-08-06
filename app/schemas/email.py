from pydantic import BaseModel, EmailStr


class SendEmailRequest(BaseModel):
    to: EmailStr
    subject: str
    template: str
    variables: dict={}

class SendEmailResponse(BaseModel):
    message: str ="Email sent successfuly"