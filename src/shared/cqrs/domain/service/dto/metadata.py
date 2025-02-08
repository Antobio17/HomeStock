from dataclasses import dataclass

@dataclass
class Metadata:
    message_id: str
    correlation_id: str
    causation_id: str