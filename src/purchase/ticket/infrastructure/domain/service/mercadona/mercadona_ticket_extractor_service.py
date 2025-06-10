import re
from pypdf import PdfReader
from datetime import datetime
from src.purchase.ticket.domain.service.ticket_extractor_service import TicketExtractorService
from src.purchase.ticket.domain.service.dto.ticket_extractor_result import TicketExtractorResult
from src.purchase.ticket.domain.service.dto.ticket_extractor_item_result import TicketExtractorItemResult

MAX_PDF_ITERATIONS: int = 1000

class MercadonaTicketExtractorService(TicketExtractorService):
    
    def execute(self, file_path: str):
        reader = PdfReader(file_path)
        complete_text = reader.pages[0].extract_text()
       
        ticket_items = []
        taxes = []
        skip_next = False
        items_start = False
        tax_resume_start = False
        pattern = re.compile(r'^(\d+)\s+(.+?)\s+(\d+,\d{2})(?:\s+(\d+,\d{2}))?$')

        lines = complete_text.split('\n')
        for index, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            
            if 'OP:' in line:
                line = line.replace('OP:', '').split(' ')
                purchased_at = datetime.strptime(f'{line[0]} {line[1]}', '%d/%m/%Y %H:%M')
                
            if 'FACTURA SIMPLIFICADA:' in line:
                reference = line.replace('FACTURA SIMPLIFICADA:', '').strip()  
                  
            if 'Descripción' in line:
                items_start = True
                
            if 'TOTAL (€)' in line:
                items_start = False
                
            if items_start and pattern.match(line):
                match = pattern.match(line)
                quantity = float(match.group(1))
                description = match.group(2).strip()
                amount = float(match.group(3).replace(',', '.'))
                ticket_items.append({
                    'quantity': quantity,
                    'description': description,
                    'amount': amount * quantity
                })
            
            if 'PARKING' in line:
                skip_next = True
                continue
            
            if items_start and not pattern.match(line) and 'Descripción' not in line:
                description = line.split(' ', 1)[-1]
                quantity = float(lines[index + 1].split(' ')[0].replace(',', '.'))
                amount = float(lines[index + 1].split(' ')[-1].replace(',', '.'))
                ticket_items.append({
                    'quantity': quantity,
                    'description': description,
                    'amount': amount
                })
                skip_next = True
            
            if tax_resume_start and 'TOTAL' in line:
                tax_resume_start = False
                tax_amount = float(line.split(' ')[-1].replace(',', '.'))
                subtotal = float(line.split(' ')[-2].replace(',', '.'))
                total = tax_amount + subtotal
                
            if tax_resume_start:
                line = line.split(' ')
                taxes.append({
                    line[0].replace('%', '').strip(): float(line[1].replace(',', '.'))
                })
                
            if 'IVA' in line:
                tax_resume_start = True
                
        submit_ticket_items = []
        for item in ticket_items:
            submit_ticket_items.append(
                TicketExtractorItemResult(
                    quantity = float(item['quantity']),
                    description = item['description'].rstrip(),
                    amount = float(item['amount'])            
                )
            )

        return TicketExtractorResult(
            supermarket = 'Mercadona',
            purchased_at = purchased_at,
            reference = reference,
            discount_amount = 0.0,
            taxes = taxes,
            subtotal = float(subtotal),
            tax_amount = float(tax_amount),
            total = total,
            items = submit_ticket_items   
        )