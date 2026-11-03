"""User-facing text formatting of search results for the presentation layer."""

from customer_search.search_service import SearchResult


def format_output(result: SearchResult) -> str:
    """Format SearchResult into user-facing text output.

    Translates each status (OK, EMPTY_QUERY, NO_RESULTS) into the appropriate
    channel presentation. Shared by the one-shot CLI and InteractiveSession.
    """
    if result.status == "EMPTY_QUERY":
        return "Consulta vacía. Ingrese un término de búsqueda para consultar clientes."

    if result.status == "NO_RESULTS":
        return result.message or "No se encontraron clientes."

    # Status: OK
    lines = [
        f"Total de coincidencias: {result.total}",
        f"Mostrando {len(result.items)} resultados:",
        "-" * 40,
    ]
    for item in result.items:
        lines.append(f"[{item.cliente_id}] {item.nombre} <{item.email}>")
    return "\n".join(lines)
