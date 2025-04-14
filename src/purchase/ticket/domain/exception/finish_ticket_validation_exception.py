from dataclasses import dataclass

@dataclass
class FinishTicketValidationException(Exception):
    message: str
    key_translate: str