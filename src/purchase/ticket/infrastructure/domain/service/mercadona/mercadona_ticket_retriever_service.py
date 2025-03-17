import os
import email
import imaplib
from dataclasses import dataclass
from email.header import decode_header
from src.purchase.ticket.domain.service.ticket_retriever_service import TicketRetrieverService

@dataclass
class MercadonaTicketRetrieverService(TicketRetrieverService):
    __google_password_application: str

    def execute(self):
        with imaplib.IMAP4_SSL('imap.gmail.com', 993) as mail:
            pdf_paths = []
            
            mail.login(
                os.getenv('GOOGLE_EMAIL_TICKETS'), 
                self.__google_password_application
            )
            
            mail.select('inbox')
            _, data = mail.search(None, 'ALL')
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
                        pdf_paths.append(filepath)
                                             
        return pdf_paths