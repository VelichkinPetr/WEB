# Данные: заявки с приоритетом и статусом.

# TICKETS = [
#  {
#   "id": int,
#   "title": str,
#   "description": str,
#   "priority": str,
#   "status": str
#  }
# ]

# Ограничения: 
# все поля - обязательные
# допустимые значения для поля "priority": "low", "medium", "high"
# допустимые значения для поля "status": "open", "in_progress", "closed"


# 1. Реализовать CRUD для тикетов.
# 2. Добавить фильтрацию:
# - GET /tickets?status=open
# - GET /tickets?priority=high
# 3. Добавить PUT /tickets/{id}/close — переводит статус в closed.
from typing import Dict, Any
from fastapi import FastAPI, status, HTTPException
from model import Ticket
from services import TicketService


app = FastAPI()
ticket_service = TicketService()


@app.post('/tickets', status_code=status.HTTP_200_OK)
def create_tickets(data: Dict[str, Any]):
    return ticket_service.create(data)

@app.get('/tickets', status_code=status.HTTP_200_OK)
def get_tickets(id: int = None, status: str = None, priority: str = None):

    if id is not None and (status is not None or priority is not None):
        raise HTTPException(status_code=400, detail='Do not use ID with other filters')
    
    if id is None and status is None and priority is None:
        return {
                'all tickets':ticket_service.get_all()
        }
    
    elif id is not None and status is None and priority is None:
                    return {
                            'ticket by id':ticket_service.get_by_id(id)
                    }
                
    elif id is None and status is not None and priority is None:
         return {
                'ticket by status':ticket_service.get_by_status(status)
        }
    
    elif id is None and status is None and priority is not None:
         return {
                'ticket by priority':ticket_service.get_by_priority(priority)
        }
    
    raise HTTPException(status_code=404, detail='Do not use STATUS with PRIORITY')

@app.put('/tickets/{id}/close', status_code=status.HTTP_200_OK)
def close_ticket(id: int):
    
    closed_ticket = ticket_service.put_close(id)

    if not closed_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket with id not found')
    
@app.put('/tickets/{id}', status_code=status.HTTP_200_OK)
def update_ticket(id: int, data: Dict[str, Any]):
    if not data.keys():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Update is empty')
    
    update_ticket = ticket_service.update(id, data)

    if not update_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket with id not found')
    
@app.delete('/tickets', status_code=status.HTTP_200_OK)
def delete_ticket(id: int = None):
    if ticket_service.is_empty():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Tickets BD is empty')
    if id is None:
        ticket_service.delete_all()
    else:
        if not ticket_service.delete_by_id(id): 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket with id not found')
