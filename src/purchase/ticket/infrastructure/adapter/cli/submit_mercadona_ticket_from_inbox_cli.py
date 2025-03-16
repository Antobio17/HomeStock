import os
import email
import imaplib
import pdfquery
from src import thread_local
from datetime import datetime
from email.header import decode_header
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.purchase.ticket.application.command.dto.submit_ticket_item import SubmitTicketItem
from src.purchase.ticket.application.command.submit_ticket_command import SubmitTicketCommand

MAX_PDF_ITERATIONS = 1000
PDF_SAVE_PATH = '/app/var/files/tickets/mercadona'

class SubmitMercadonaTicketFromInboxCli:
    
    def __init__(self):
        self.__command_bus = CommandBus()
        thread_local.schema_name = '114817124855698770001'
        
    def execute(self):
        pdfs = self.get_pdfs_from_inbox()
        for pdf in pdfs:
            subtmit_ticket_command = self.__extract_pdf(pdf)
            self.__command_bus.handle(subtmit_ticket_command)
    
    def __extract_pdf(self, pdf_path: str) -> SubmitTicketCommand:
        pdf = pdfquery.PDFQuery(pdf_path)
        pdf.load()
        
        # xml_path = os.path.join('/app/var', os.path.basename(pdf_path).replace('.pdf', '.xml'))
        # pdf.tree.write(xml_path, pretty_print=True, encoding='utf-8')
        
        ticket_items = []
        items = pdf.pq('LTTextBoxHorizontal[index="8"] LTTextLineHorizontal')
        for item in items:
            quantity, description = item.text.split(' ', 1)
            ticket_items.append({'quantity': quantity, 'description': description})
        
        tax_rates = []    
        tax_amounts = []   
        index = 9
        while True:
            query = pdf.pq(f'LTTextBoxHorizontal[index="{index}"] LTTextLineHorizontal')
            if len(query) == 0:
                index += 1
                continue
            
            if query[0].text.startswith('Importe'):
                for i, amount in enumerate(query[1:], start=0):
                    ticket_items[i]['amount'] = amount.text.replace(',', '.')
            if query[0].text.startswith('IVA'):
                for i, tax_rate in enumerate(query[1:-1], start=0):
                    tax_rates.append(tax_rate.text.replace('%', ''))
            if query[0].text.startswith('BASE IMPONIBLE'):
                subtotal = query[-1].text.replace(',', '.')
            if query[0].text.startswith('CUOTA'):
                for i, value in enumerate(query[1:-1], start=0):
                    tax_amounts.append(float(value.text.replace(',', '.')))
                tax_amount = query[-1].text.replace(',', '.')
                break
            
            index += 1
            if index > MAX_PDF_ITERATIONS:
                raise Exception('Max PDF iterations reached')
        
        taxes = {rate: amount for rate, amount in zip(tax_rates, tax_amounts)}
        purchased_at = pdf.pq('LTTextBoxHorizontal[index="2"] LTTextLineHorizontal')[-1].text
        reference = pdf.pq('LTTextBoxHorizontal[index="5"]').text().replace('FACTURA SIMPLIFICADA: ', '')
        total = float(subtotal) + float(tax_amount)
        
        submit_ticket_items = []
        for item in ticket_items:
            submit_ticket_items.append(
                SubmitTicketItem(
                    quantity = int(item['quantity']),
                    description = item['description'],
                    amount = float(item['amount'])            
                )
            )
        
        return SubmitTicketCommand(
            supermarket = 'Mercadona',
            purchased_at = datetime.strptime(purchased_at.strip(), '%d/%m/%Y %H:%M'),
            reference = reference,
            discount_amount = 0.0,
            taxes = taxes,
            subtotal = float(subtotal),
            tax_amount = float(tax_amount),
            total = total,
            items = submit_ticket_items   
        )
        
    def get_pdfs_from_inbox(self):
        with imaplib.IMAP4_SSL('imap.gmail.com', 993) as mail:
            pdf_paths = []
            
            mail.login(
                os.getenv('GOOGLE_EMAIL_TICKETS'), 
                os.getenv('GOOGLE_PASSWORD_APPLICATION')
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
                        print('No hay pdf del merdaona')
                        exit(0)
                        
                    decoded_filename = decode_header(filename)
                    filename = ''.join([str(text, charset or 'utf-8') if isinstance(text, bytes) else text for text, charset in decoded_filename])
                    
                    os.makedirs(PDF_SAVE_PATH, exist_ok=True)
                    filepath = os.path.join(PDF_SAVE_PATH, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))   
                        pdf_paths.append(filepath)
                                             
        return pdf_paths
                
    
if __name__ == '__main__':
    SubmitMercadonaTicketFromInboxCli().execute()