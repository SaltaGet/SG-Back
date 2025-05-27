from fastapi import APIRouter
from src.schemas.user_schema.email_contact import EmailContact
from src.services.email_service import EmailService

email_router = APIRouter(prefix='/email', tags=['Email'])

@email_router.post('/send_email')
async def send_email(
    contact: EmailContact
):
    return await EmailService().send_contact(contact)