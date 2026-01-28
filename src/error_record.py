# src/error_record.py
from dataclasses import dataclass

@dataclass
class ErrorRecord:
    error_code: str
    sheet: str
    title: str
    non_technical: str
    origin_field: str
    owner: str
    action: str = ""

    def as_text(self) -> str:
        parts = [
            f"Error code: {self.error_code}" if self.error_code else "",
            f"Category: {self.sheet}" if self.sheet else "",
            f"Title: {self.title}" if self.title else "",
            f"Non-technical explanation: {self.non_technical}" if self.non_technical else "",
            f"Origin field: {self.origin_field}" if self.origin_field else "",
            f"Owner / Responsible: {self.owner}" if self.owner else "",
            f"Recommended action: {self.action}" if self.action else "",
        ]
        return "\n".join(p for p in parts if p)
