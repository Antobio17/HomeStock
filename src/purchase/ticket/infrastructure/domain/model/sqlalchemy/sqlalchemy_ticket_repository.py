import json
from dataclasses import dataclass
from typing import Optional, Type, List
from sqlalchemy.exc import NoResultFound
from src.purchase.ticket.domain.model.ticket import Ticket
from src.purchase.ticket.domain.model.ticket_item import TicketItem
from src.purchase.ticket.domain.model.ticket_repository import TicketRepository
from src.purchase.ticket.infrastructure.domain.model.sqlalchemy.persistence.model import TicketModel
from src.purchase.ticket.infrastructure.domain.model.sqlalchemy.persistence.model_item import TicketItemModel
from src.shared.database.infrastructure.domain.manager.sqlalchemy.sqlalchemy_transaction_manager import SqlalchemyTransactionManager

@dataclass
class SqlalchemyTicketRepository(TicketRepository):
    __transaction_manager: SqlalchemyTransactionManager

    @staticmethod
    def __to_model(ticket: Ticket) -> TicketModel:
        return TicketModel(
            id = ticket.id,
            supermarket = ticket.supermarket,
            reference = ticket.reference,
            status = ticket.status,
            subtotal = ticket.subtotal,
            discount_amount = ticket.discount_amount,
            taxes = ticket.taxes,
            tax_amount = ticket.tax_amount,
            total = ticket.total,
            purchased_at = ticket.purchased_at,
            created_at = ticket.created_at,
            updated_at = ticket.updated_at
        )
        
    @staticmethod
    def __to_model_item(ticket_item: TicketItem) -> TicketModel:
        return TicketItemModel(
            id = ticket_item.id,
            ticket_id = ticket_item.ticket_id,
            description = ticket_item.description,
            quantity = ticket_item.quantity,
            unit_price = ticket_item.unit_price,
            amount = ticket_item.amount,
            product_id = ticket_item.product_id,
            format_id = ticket_item.format_id
        )

    def find_by_id(self, ticket_id: str) -> Optional[Ticket]:
        try:
            result: Type[TicketModel] = (
                self.__transaction_manager.session.query(TicketModel)
                    .filter_by(id=str(ticket_id))
                    .one()
            )
            items: List[TicketItemModel] = (
                self.__transaction_manager.session.query(TicketItemModel)
                    .filter_by(ticket_id=str(ticket_id))
                    .all()
            )
        except NoResultFound:
            return None
        
        ticket_items = []
        for item in items:
            ticket_items.append(
                TicketItem(
                    id = item.id,
                    ticket_id = item.ticket_id,
                    description = item.description,
                    quantity = item.quantity,
                    unit_price = item.unit_price,
                    amount = item.amount,
                    product_id = item.product_id,
                    format_id = item.format_id
                )
            )
                
        return Ticket(
            id = result.id,
            supermarket = result.supermarket,
            reference = result.reference,
            status = result.status,
            items = ticket_items,
            discount_amount = result.discount_amount,
            taxes = result.taxes,
            tax_amount = result.tax_amount,
            total = result.total,
            purchased_at = result.purchased_at,
            created_at = result.created_at,
            updated_at = result.updated_at
        )

    def save(self, ticket: Ticket) -> None:
        for item in ticket.items:
            self.__transaction_manager.session.merge(self.__to_model_item(item))
        self.__transaction_manager.session.merge(self.__to_model(ticket))