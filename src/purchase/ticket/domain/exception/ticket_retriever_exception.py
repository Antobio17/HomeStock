from dataclasses import dataclass

@dataclass
class TicketRetrieverException(Exception):
    message: str
    key_translate: str