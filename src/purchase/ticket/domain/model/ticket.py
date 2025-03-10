import uuid
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field

from src.shared.cqrs.domain.event.domain_event import DomainEvent
from src.purchase.ticket.domain.model.ticket_item import TicketItem
from src.purchase.ticket.domain.event.ticket_submitted import TicketSubmitted
from src.purchase.ticket.domain.exception.submit_ticket_exception import SubmitTicketException

STATUS_PENDING = "pending"
STATUS_VALIDATION_IN_PROGRESS = "validation_in_progress"
STATUS_INVALIDATION_IN_PROGRESS = "invalidation_in_progress"
STATUS_VALIDATED = "validated"
    
@dataclass
class Ticket:
    id: str
    supermarket: str
    reference: str
    status: str
    items: list[TicketItem]
    subtotal: float
    discount_amount: float
    taxes: dict[float, float]
    tax_amount: float
    total: float
    purchased_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    domain_events: list[DomainEvent] = field(default_factory=list)
    
    
    def record(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)
        
    def pull_domain_events(self) -> list[DomainEvent]:
        domain_events = self.domain_events
        self.domain_events = []
        return domain_events
    
    @staticmethod
    def submit(
        supermarket: str, 
        reference: str, 
        subtotal: float, 
        discount_amount: float, 
        taxes: dict[float, float], 
        tax_amount: float, 
        total: float, 
        purchased_at: datetime,
        items: list
    ) -> 'Ticket':
        if len(items) == 0:
            raise SubmitTicketException(
                f'Items list from ticket {reference} cannot be empty',
                f'itemsListFromTicket{reference}CannotBeEmpty'
            )

        ticket_id = str(uuid.uuid4())

        ticket_items = []
        for item in items:
            if item['description'] == '':
                raise SubmitTicketException(
                    f'Item from ticket {reference} has no description',
                    f'itemFromTicket{reference}HasNoDescription'
                )
            if item['quantity'] <= 0 or item['amount'] <= 0:
                raise SubmitTicketException(
                    f'Item {item["description"]} from ticket {reference} has invalid quantity or amount',
                    f'item{item["description"]}FromTicket{reference}HasInvalidQuantityOrAmount'
                )

            ticket_items.append(
                TicketItem(
                    str(uuid.uuid4()),
                    ticket_id,
                    item['description'],
                    item['quantity'],
                    item['amount'] / item['quantity'],
                    item['amount']
                )
            )

        ticket = Ticket(
            ticket_id,
            supermarket,
            reference,
            STATUS_PENDING,
            ticket_items,
            subtotal,
            discount_amount,
            taxes,
            tax_amount,
            total,
            purchased_at,
            created_at = datetime.now()
        )

        ticket.record(
            TicketSubmitted(
                ticket_id,
                supermarket,
                reference,
                STATUS_PENDING,
                items,
                subtotal,
                discount_amount,
                taxes,
                tax_amount,
                total,
                ticket.purchased_at,
                ticket.created_at
            )
        )

        return ticket
