from dataclasses import dataclass

@dataclass
class StartTicketValidationException(Exception):
    message: str
    key_translate: str