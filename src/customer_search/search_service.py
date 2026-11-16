"""Search service coordinating customer search rules."""

from dataclasses import dataclass

from customer_search.messages import NO_RESULTS_MESSAGE
from customer_search.models import Customer
from customer_search.normalization import normalize_query, normalize_text
from customer_search.repository import CustomerRepository


@dataclass
class CustomerView:
    """Projected view of customer containing only allowed fields (FR-10)."""

    cliente_id: str
    nombre: str
    email: str


@dataclass
class SearchResult:
    """Search result response data contract."""

    items: list[CustomerView]
    total: int
    status: str
    message: str | None = None


class SearchService:
    """Service encapsulating customer search business rules."""

    def __init__(self, repository: CustomerRepository | None = None) -> None:
        """Initialize SearchService with customer repository.

        Args:
            repository: Optional repository instance. Defaults to CustomerRepository.
        """
        self.repository = repository or CustomerRepository()

    def search(self, query: str, domain: str = "") -> SearchResult:
        """Search customers by name or email.

        Applies normalization, substring matching, deduplication, deterministic
        ordering, truncation to 50, and field projection. An optional email-domain
        filter (FR-16, SR-15) further restricts matches to customers whose
        normalized email ends with the normalized domain; a blank domain leaves
        search behavior unchanged (VR-05).

        Args:
            query: Raw search query string.
            domain: Optional email-domain filter. Blank or whitespace-only values
                are treated as "no filter applied" (VR-05, A-13).

        Returns:
            SearchResult containing projected items, total count, status, and message.
        """
        stripped_query = query.strip()
        if not stripped_query:
            # EH-01: Empty or whitespace query does not query repository
            return SearchResult(items=[], total=0, status="EMPTY_QUERY", message=None)

        all_customers = self.repository.find_all()
        normalized_query = normalize_query(stripped_query)
        normalized_domain = normalize_query(domain)

        matched: list[tuple[int, Customer]] = []
        for customer in all_customers:
            norm_name = normalize_text(customer.nombre)
            norm_email = normalize_text(customer.email)

            tier: int | None = None
            if norm_name == normalized_query or norm_email == normalized_query:
                tier = 1
            elif norm_name.startswith(normalized_query) or norm_email.startswith(normalized_query):
                tier = 2
            elif normalized_query in norm_name or normalized_query in norm_email:
                tier = 3

            if tier is not None and normalized_domain and not norm_email.endswith(normalized_domain):
                # SR-15: non-blank domain filter restricts matches by email suffix.
                tier = None

            if tier is not None:
                matched.append((tier, customer))

        if not matched:
            return SearchResult(items=[], total=0, status="NO_RESULTS", message=NO_RESULTS_MESSAGE)

        # Deterministic sorting (SR-07):
        # 1. Match priority tier (1: exact, 2: prefix, 3: substring)
        # 2. Alphabetical by name (normalized first, then raw)
        # 3. Customer ID tie-breaker
        matched.sort(
            key=lambda item: (
                item[0],
                normalize_text(item[1].nombre),
                item[1].nombre,
                item[1].cliente_id,
            )
        )

        total = len(matched)
        projected_items = [
            CustomerView(
                cliente_id=c.cliente_id,
                nombre=c.nombre,
                email=c.email,
            )
            for _, c in matched[:50]
        ]

        return SearchResult(
            items=projected_items,
            total=total,
            status="OK",
            message=None,
        )
