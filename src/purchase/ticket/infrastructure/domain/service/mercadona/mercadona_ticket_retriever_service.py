import os
import email
import imaplib
from typing import Optional
from dataclasses import dataclass
from email.header import decode_header
from src.purchase.ticket.domain.service.ticket_retriever_service import TicketRetrieverService
from src.purchase.ticket.domain.exception.ticket_retriever_exception import TicketRetrieverException
from src.purchase.ticket.domain.query_model.ticket_retriever_needle_data_query import TicketRetrieverNeedleDataQuery

@dataclass
class MercadonaTicketRetrieverService(TicketRetrieverService):
    __ticket_retriever_needle_data_query: TicketRetrieverNeedleDataQuery
    __google_password_application: str

    def execute(self) -> Optional[str]:
        ticket_pool = self.__ticket_retriever_needle_data_query.get_ticket_pool('mercadona')
        if (ticket_pool is None):
            raise TicketRetrieverException(
                'Ticket pool for Mercadona is not configured', 
                'ticketPoolForMercadonaIsNotConfigured'
            )
            
        with imaplib.IMAP4_SSL('imap.gmail.com', 993) as mail:    
            mail.login(
                ticket_pool, 
                self.__google_password_application
            )
            
            mail.select('inbox')
            _, data = mail.search(None, '(UNSEEN FROM "ticket_digital@mail.mercadona.com")')
            for num in data[0].split():
                _, data = mail.fetch(num, '(RFC822)')
                _, bytes_data = data[0]
                email_message = email.message_from_bytes(bytes_data)
                
                for part in email_message.walk():
                    if part.get_content_type() != 'application/pdf':
                        continue
                    
                    filename = part.get_filename()
                    if filename is None:
                        continue
                        
                    decoded_filename = decode_header(filename)
                    filename = ''.join([str(text, charset or 'utf-8') if isinstance(text, bytes) else text for text, charset in decoded_filename])
                    
                    os.makedirs('/app/var/files/tickets/mercadona', exist_ok=True)
                    filepath = os.path.join('/app/var/files/tickets/mercadona', filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))   
                    
                    mail.store(num, '+FLAGS', '\\Seen')
                    return filepath
                          
        return None