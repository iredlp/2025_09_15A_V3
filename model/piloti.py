from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Piloti:
    driverId: int
    driverRef: str
    number: int
    code: str
    forename: str
    surname: str
    dob: datetime
    nationality: str
    url: str

    oldest_driver_dob:Optional[int] = None  #valore opzionale
    #list_squadre:  list = field(default_factory=list)
    partecipazioni: list = field(default_factory=list)

   # popolarita: int = 0

    def __hash__(self):
        return hash(self. driverId)

    def __eq__(self, other):
        if isinstance(other, Piloti):
            return self. driverId== other. driverId
        return False

    def __repr__(self):
        return (f"{self.surname} ({self. driverId}) ")
                # if self.year is not None else 'N/D'})")