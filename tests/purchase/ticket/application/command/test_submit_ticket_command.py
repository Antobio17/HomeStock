import uuid
import unittest
from datetime import datetime
from unittest.mock import Mock
from src.purchase.ticket.domain.model.ticket import Ticket, STATUS_PENDING
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.purchase.ticket.domain.event.ticket_submitted import TicketSubmitted
from src.purchase.ticket.application.command.dto.submit_ticket_item import SubmitTicketItem
from src.purchase.ticket.application.command.submit_ticket_command import SubmitTicketCommand
from src.purchase.ticket.domain.exception.submit_ticket_exception import SubmitTicketException
from src.purchase.ticket.application.command.submit_ticket_command_handler import SubmitTicketCommandHandler
from src.purchase.ticket.infrastructure.domain.model.in_memory.in_memory_ticket_repository import InMemoryTickeyRepository 
from src.purchase.ticket.infrastructure.domain.query_model.in_memory.in_memory_submit_ticket_needle_data_query import InMemorySubmitTicketNeedleDataQuery

class TestSubmitTicketCommand(unittest.TestCase):

    def setUp(self):
        self.__message_publisher = Mock(spec=MessagePublisher)

    def test_submit_ticket_when_no_errors_then_success(self):
        needle_data_query = InMemorySubmitTicketNeedleDataQuery()
        in_memory_repository = InMemoryTickeyRepository()
        
        items = [
            SubmitTicketItem(
                description = 'Ticker Item 1',
                quantity = 2,
                amount = 25.0
            ),
            SubmitTicketItem(
                description = 'Ticker Item 2',
                quantity = 1,
                amount = 50.0
            )   
        ]
        command = SubmitTicketCommand(
            supermarket = 'supermarket', 
            reference = 'ABC-123',
            subtotal = 100.0,
            discount_amount = 0.0,
            taxes = {
                10.0: 5.0,
                4.0: 2.0
            },
            tax_amount = 7.0,
            total = 107.0,
            purchased_at = datetime.now(),
            items = items
        )
        command_handler = SubmitTicketCommandHandler(
            needle_data_query,
            in_memory_repository,
            self.__message_publisher
        )
        command_handler.handle(command)
        
        ticket = in_memory_repository.spy()

        self.assertIsInstance(ticket, Ticket)
        self.assertTrue(uuid.UUID(ticket.id))
        self.assertEqual(ticket.supermarket, command.supermarket)
        self.assertEqual(ticket.reference, command.reference)
        self.assertEqual(ticket.status, STATUS_PENDING)
        self.assertEqual(ticket.subtotal, command.subtotal)
        self.assertEqual(ticket.discount_amount, command.discount_amount)
        self.assertEqual(ticket.taxes, command.taxes)
        self.assertEqual(ticket.tax_amount, command.tax_amount)
        self.assertEqual(ticket.total, command.total)
        self.assertEqual(ticket.purchased_at, command.purchased_at)
        self.assertIsInstance(ticket.created_at, datetime)
        self.assertEqual(ticket.updated_at, None)
        self.__message_publisher.execute.assert_called_once_with(
            TicketSubmitted(
                ticket.id,
                ticket.supermarket,
                ticket.reference,
                STATUS_PENDING,
                [
                    {
                        'description': 'Ticker Item 1',
                        'quantity': 2,
                        'amount': 25.0
                    },
                    {
                        'description': 'Ticker Item 2',
                        'quantity': 1,
                        'amount': 50.0
                    }
                ],
                ticket.subtotal,
                ticket.discount_amount,
                ticket.taxes,
                ticket.tax_amount,
                ticket.total,
                ticket.purchased_at,
                ticket.created_at
            )
        )
        
    def test_submit_ticket_when_reference_already_exists_then_fail(self):
        needle_data_query = InMemorySubmitTicketNeedleDataQuery()
        needle_data_query.will_return(True)
        in_memory_repository = InMemoryTickeyRepository()
        
        command = SubmitTicketCommand(
            supermarket = 'supermarket', 
            reference = 'ABC-123',
            subtotal = 100.0,
            discount_amount = 0.0,
            taxes = {},
            tax_amount = 7.0,
            total = 107.0,
            purchased_at = datetime.now(),
            items = []
        )
        command_handler = SubmitTicketCommandHandler(
            needle_data_query,
            in_memory_repository,
            self.__message_publisher
        )
        with self.assertRaises(SubmitTicketException) as context:
            command_handler.handle(command)
        
        self.assertEqual(context.exception.message, f'Ticket with reference {command.reference} already submitted')
        self.assertEqual(context.exception.key_translate, f'ticketWithReference{command.reference}AlreadySubmitted')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()
        
    def test_submit_ticket_when_items_empty_then_fail(self):
        needle_data_query = InMemorySubmitTicketNeedleDataQuery()
        in_memory_repository = InMemoryTickeyRepository()
        
        command = SubmitTicketCommand(
            supermarket = 'supermarket', 
            reference = 'ABC-123',
            subtotal = 100.0,
            discount_amount = 0.0,
            taxes = {},
            tax_amount = 7.0,
            total = 107.0,
            purchased_at = datetime.now(),
            items = []
        )
        command_handler = SubmitTicketCommandHandler(
            needle_data_query,
            in_memory_repository,
            self.__message_publisher
        )
        with self.assertRaises(SubmitTicketException) as context:
            command_handler.handle(command)
        
        self.assertEqual(context.exception.message, f'Items list from ticket {command.reference} cannot be empty')
        self.assertEqual(context.exception.key_translate, f'itemsListFromTicket{command.reference}CannotBeEmpty')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()
        
    def test_submit_ticket_when_item_description_empty_then_fail(self):
        needle_data_query = InMemorySubmitTicketNeedleDataQuery()
        in_memory_repository = InMemoryTickeyRepository()
        
        items = [
            SubmitTicketItem(
                description = '',
                quantity = 2,
                amount = 25.0
            )   
        ]
        command = SubmitTicketCommand(
            supermarket = 'supermarket', 
            reference = 'ABC-123',
            subtotal = 100.0,
            discount_amount = 0.0,
            taxes = {},
            tax_amount = 7.0,
            total = 107.0,
            purchased_at = datetime.now(),
            items = items
        )
        command_handler = SubmitTicketCommandHandler(
            needle_data_query,
            in_memory_repository,
            self.__message_publisher
        )
        with self.assertRaises(SubmitTicketException) as context:
            command_handler.handle(command)
        
        self.assertEqual(context.exception.message, f'Item from ticket {command.reference} has no description')
        self.assertEqual(context.exception.key_translate, f'itemFromTicket{command.reference}HasNoDescription')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()
        
    def test_submit_ticket_when_item_numeric_negative_values_then_fail(self):
        needle_data_query = InMemorySubmitTicketNeedleDataQuery()
        in_memory_repository = InMemoryTickeyRepository()
        
        items = [
            SubmitTicketItem(
                description = 'Ticket Item 1',
                quantity = -2,
                amount = -25.0
            )   
        ]
        command = SubmitTicketCommand(
            supermarket = 'supermarket', 
            reference = 'ABC-123',
            subtotal = 100.0,
            discount_amount = 0.0,
            taxes = {},
            tax_amount = 7.0,
            total = 107.0,
            purchased_at = datetime.now(),
            items = items
        )
        command_handler = SubmitTicketCommandHandler(
            needle_data_query,
            in_memory_repository,
            self.__message_publisher
        )
        with self.assertRaises(SubmitTicketException) as context:
            command_handler.handle(command)
        
        self.assertEqual(context.exception.message, f'Item from ticket {command.reference} has invalid quantity or amount')
        self.assertEqual(context.exception.key_translate, f'itemFromTicket{command.reference}HasInvalidQuantityOrAmount')
        self.assertIsNone(in_memory_repository.spy())
        self.__message_publisher.execute.assert_not_called()