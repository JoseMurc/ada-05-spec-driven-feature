"""Domain models for customer search."""

from dataclasses import dataclass


@dataclass
class Customer:
    """Represents a customer in the system.

    Attributes:
        cliente_id: Stable and unique customer identifier.
        nombre: Full name as free text (A-02).
        email: Email address of the customer.
    """

    cliente_id: str
    nombre: str
    email: str
