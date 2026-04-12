from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta

@dataclass
class Transaction:
    id: Optional[int] = None
    bookId: Optional[int] = None
    memberId: Optional[int] = None
    issuedAt: datetime = field(default_factory=datetime.now)
    dueDate: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=14))
    returnDate: Optional[datetime] = None
    fine: int = 0
    