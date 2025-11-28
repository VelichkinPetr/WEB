from typing import Dict, Any

from model import Ticket


class TicketService:

    def __init__(self):
        self.list_tickets: list[Ticket] = []
        self.ticket_id = 1

    def create(self, data: Dict[str, Any]) -> Ticket:
        data['id'] = self.ticket_id

        new_ticket = Ticket(**data)
        self.list_tickets.append(new_ticket)
        self.ticket_id += 1
        return new_ticket
    
    def get_all(self) -> list[Ticket]:
        return self.list_tickets
    
    def get_by_id(self, id: int) -> list[Ticket]:
        return [ticket for ticket in self.list_tickets if ticket.id == id]
    
    def get_by_status(self, status: str) -> list[Ticket]:
        return [ticket for ticket in self.list_tickets if ticket.status == status]
    
    def get_by_priority(self, priority: str) -> list[Ticket]:
        return [ticket for ticket in self.list_tickets if ticket.priority == priority]
    
    def update(self, id: int, data: Dict[str, Any]) -> Ticket:
        for ticket in self.list_tickets:
            if ticket.id == id:
                if {'title'} <= data.keys():
                    ticket.title = data['title']
                
                if {'description'} <= data.keys():
                    ticket.description = data['description']
                    
                if {'priority'} <= data.keys():
                    ticket.priority = data['priority']

                if {'status'} <= data.keys():
                    ticket.status = data['status']
                return ticket
        
    def put_close(self, id: int) -> Ticket:
        for ticket in self.list_tickets:
            if ticket.id == id:
                ticket.status = 'closed'
                return ticket
            
    def delete_all(self):
        self.list_tickets.clear()

    def delete_by_id(self, id: int):
        for i,ticket in enumerate(self.list_tickets):
            if ticket.id == id:
                del self.list_tickets[i]
                return True
        return False
    
    def is_empty(self):
        return True if len(self.list_tickets) == 0 else False