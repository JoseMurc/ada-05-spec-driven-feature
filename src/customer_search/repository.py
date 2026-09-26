"""Repository layer for accessing customer data."""

import json
from pathlib import Path

from customer_search.models import Customer

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "customers.json"


class CustomerRepository:
    """Repository for retrieving customers from storage.

    Reads raw data from storage without filtering, sorting, or normalizing.
    """

    def __init__(self, file_path: str | Path | None = None) -> None:
        """Initialize repository with target JSON file path.

        Args:
            file_path: Optional custom path to customers JSON file.
                       Defaults to project's data/customers.json.
        """
        if file_path is None:
            self.file_path = DEFAULT_DATA_PATH
        else:
            self.file_path = Path(file_path)

    def find_all(self) -> list[Customer]:
        """Retrieve all customers from the storage.

        Returns:
            List of Customer entities without filtering, sorting, or normalizing.
        """
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [
            Customer(
                cliente_id=item["cliente_id"],
                nombre=item["nombre"],
                email=item["email"],
            )
            for item in data
        ]
