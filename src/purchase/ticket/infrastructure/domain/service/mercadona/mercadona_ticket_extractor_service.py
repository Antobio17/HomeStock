import pdfquery
from datetime import datetime
from src.purchase.ticket.domain.service.ticket_extractor_service import TicketExtractorService
from src.purchase.ticket.domain.service.dto.ticket_extractor_result import TicketExtractorResult
from src.purchase.ticket.domain.service.dto.ticket_extractor_item_result import TicketExtractorItemResult

MAX_PDF_ITERATIONS: int = 1000

class MercadonaTicketExtractorService(TicketExtractorService):
    
    def execute(self, file_path: str):
        pdf = pdfquery.PDFQuery(file_path)
        pdf.load()
        
        ticket_items = []
        items = pdf.pq('LTTextBoxHorizontal[index="7"] LTTextLineHorizontal')
        if len(items) == 0:
            items = pdf.pq('LTTextBoxHorizontal[index="8"] LTTextLineHorizontal')
            
        for item in items:
            quantity, description = item.text.split(' ', 1)
            ticket_items.append({'quantity': quantity, 'description': description})
            
        tax_rates = []    
        tax_amounts = []   
        index = 9
        purchased_by_weight_counter = 0
        is_by_weight_last_iteration = False
        items_iteration_finished = False
        while True:
            query = pdf.pq(f'LTTextBoxHorizontal[index="{index}"] LTTextLineHorizontal')
            if len(query) == 0:
                query = pdf.pq(f'LTTextBoxHorizontal[index="{index}"]')
            
            if is_by_weight_last_iteration:
                is_by_weight_last_iteration = False
                if query[0].text.replace(',', '').replace(' ', '').isnumeric():
                    items_iteration_finished = True
                    continue
                quantity, description = query[0].text.split(' ', 1)
                ticket_items.append({'quantity': quantity, 'description': description})
            if 'kg' in query[0].text and not items_iteration_finished:
                ticket_items[-1]['description'] += 'KG'
                ticket_items[-1]['quantity'] = query[0].text.replace(',', '.').replace('kg', '')
                purchased_by_weight_counter += 1
                is_by_weight_last_iteration = True
            if query[0].text.startswith('Importe'):
                for i, amount in enumerate(query[1:], start=0):
                    ticket_items[i]['amount'] = amount.text.replace(',', '.')
                for i in range(1, purchased_by_weight_counter + 1):
                    amount = pdf.pq(f'LTTextBoxHorizontal[index="{index+i}"]')
                    j = len(ticket_items) - purchased_by_weight_counter + i - 1
                    ticket_items[j]['amount'] = amount.text().replace(',', '.')
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
                TicketExtractorItemResult(
                    quantity = float(item['quantity']),
                    description = item['description'].rstrip(),
                    amount = float(item['amount'])            
                )
            )
        
        return TicketExtractorResult(
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