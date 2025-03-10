from dataclasses import dataclass

@dataclass
class SubmitTicketException(Exception):
    message: str
    key_translate: str