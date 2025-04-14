import uuid
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field

from src.shared.cqrs.domain.event.domain_event import DomainEvent
from src.purchase.ticket.domain.model.ticket_item import TicketItem
from src.purchase.ticket.domain.event.ticket_submitted import TicketSubmitted
from src.purchase.ticket.domain.exception.submit_ticket_exception import SubmitTicketException
from src.purchase.ticket.domain.event.ticket_validation_started import TicketValidationStarted
from src.purchase.ticket.domain.exception.start_ticket_validation_exception import StartTicketValidationException

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
    items: dict[str, TicketItem]
    subtotal: float
    discount_amount: float
    taxes: dict[str, float]
    tax_amount: float
    total: float
    purchased_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    domain_events: list[DomainEvent] = field(default_factory = list)
    
    
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
        taxes: dict[str, float], 
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

        ticket_items = {}
        for item in items:
            if item['description'] == '':
                raise SubmitTicketException(
                    f'Item from ticket {reference} has no description',
                    f'itemFromTicket{reference}HasNoDescription'
                )
            if item['quantity'] <= 0 or item['amount'] < 0:
                raise SubmitTicketException(
                    f'Item from ticket {reference} has invalid quantity or amount',
                    f'itemFromTicket{reference}HasInvalidQuantityOrAmount'
                )

            ticket_item_id = str(uuid.uuid4())
            ticket_items[ticket_item_id] = TicketItem(
                ticket_item_id,
                ticket_id,
                item['description'],
                item['quantity'],
                item['amount'] / item['quantity'],
                item['amount']
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

    def start_validation(
        self,
        reference: str, 
        subtotal: float, 
        discount_amount: float, 
        taxes: dict[str, float], 
        tax_amount: float, 
        total: float, 
        purchased_at: datetime,
        items: list
    ) -> None:
        if self.status != STATUS_PENDING:
            raise StartTicketValidationException(
                'Ticket can not start validating process due to incorrect status',
                'ticketCanNotStartValidatingProcessDueToIncorrectStatus'
            )
            
        self.__validate_totals(
            subtotal,
            discount_amount,
            taxes,
            tax_amount,
            total,
            items 
        )
        
        self.items = {}
        for item in items:
            if item['description'] == '':
                raise StartTicketValidationException(
                    f'Item from ticket {reference} has no description',
                    f'itemFromTicket{reference}HasNoDescription'
                )
            if item['quantity'] <= 0 or item['amount'] < 0:
                raise StartTicketValidationException(
                    f'Item from ticket {reference} has invalid quantity or amount',
                    f'itemFromTicket{reference}HasInvalidQuantityOrAmount'
                )
            
            ticket_item_id = str(uuid.uuid4())
            ticket_item = TicketItem(
                ticket_item_id,
                self.id,
                item['description'],
                item['quantity'],
                item['amount'] / item['quantity'],
                item['amount'],
                item['product_id'],
                item['format_id']
            )
            self.items[ticket_item_id] = ticket_item
        
        self.reference = reference
        self.subtotal = subtotal
        self.discount_amount = discount_amount
        self.taxes = taxes
        self.tax_amount = tax_amount
        self.total = total
        self.purchased_at = purchased_at
        self.status = STATUS_VALIDATION_IN_PROGRESS
        self.updated_at = datetime.now()
        
        self.record(
            TicketValidationStarted(
                self.id,
                reference,
                STATUS_PENDING,
                items,
                subtotal,
                discount_amount,
                taxes,
                tax_amount,
                total,
                self.purchased_at,
                self.updated_at
            )
        )
        
    def finish_validation(
        self,
        items: dict[str, str]
    ):
        self.status = STATUS_VALIDATED

        for ticket_item_id, item in self.items.items():
            format_id = items.get(ticket_item_id, None)
            if format_id is None:
                continue
            
            item.assign_format_id(format_id)
        
        
        
        
    @staticmethod
    def __validate_totals(
        subtotal: float, 
        discount_amount: float, 
        taxes: dict[str, float], 
        tax_amount: float, 
        total: float, 
        items: list
    ) -> None:
        if round(sum(taxes.values()), 2) != tax_amount:
            raise StartTicketValidationException(
                'Tax amount value not match with tax ammount from taxes summation',
                'taxAmountValueNotMatchWithTaxAmountFromTaxesSummation'
            )
        if round(subtotal - discount_amount + tax_amount, 2) != round(total, 2):
            raise StartTicketValidationException(
                'Total value not match with subtotal operations',
                'totalValueNotMatchWithSubtotalOperations'
            )
        if round(sum(float(item['amount']) for item in items), 2) != round(total, 2):
            raise StartTicketValidationException(
                'Total value not match with total items summation',
                'totalValueNotMatchWithTotalItemsSummation'
            )