from dataclasses import dataclass

@dataclass
class ValidateTicketException(Exception):
    message: str
    key_translate: str