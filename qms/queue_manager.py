from dataclasses import dataclass
from enum import Enum


class TicketStatus(str, Enum):
    WAITING = "waiting"
    CALLED = "called"
    SERVED = "served"


@dataclass
class Ticket:
    ticket_id: str
    service_type: str
    status: TicketStatus = TicketStatus.WAITING


class QueueManager:
    def __init__(self) -> None:
        self._queues: dict[str, list[Ticket]] = {}
        self._issued_count: dict[str, int] = {}

    def issue_ticket(self, service_type: str = "general") -> Ticket:
        service_key = service_type.strip().lower() or "general"
        self._issued_count[service_key] = self._issued_count.get(service_key, 0) + 1
        ticket = Ticket(
            ticket_id=f"{service_key[:1].upper()}{self._issued_count[service_key]:03d}",
            service_type=service_key,
        )
        self._queues.setdefault(service_key, []).append(ticket)
        return ticket

    def call_next(self, service_type: str | None = None) -> Ticket | None:
        if service_type is not None:
            queue = self._queues.get(service_type.strip().lower() or "general", [])
            if not queue:
                return None
            ticket = queue.pop(0)
            ticket.status = TicketStatus.CALLED
            return ticket

        for queue in self._queues.values():
            if queue:
                ticket = queue.pop(0)
                ticket.status = TicketStatus.CALLED
                return ticket
        return None

    def mark_served(self, ticket: Ticket) -> None:
        ticket.status = TicketStatus.SERVED

    def get_waiting_tickets(self, service_type: str | None = None) -> list[Ticket]:
        if service_type is not None:
            return list(self._queues.get(service_type.strip().lower() or "general", []))

        waiting: list[Ticket] = []
        for queue in self._queues.values():
            waiting.extend(queue)
        return waiting
