import unittest

from qms import QueueManager
from qms.queue_manager import TicketStatus


class QueueManagerTests(unittest.TestCase):
    def test_issue_ticket_uses_service_prefix_and_sequence(self):
        manager = QueueManager()

        t1 = manager.issue_ticket("billing")
        t2 = manager.issue_ticket("billing")

        self.assertEqual(t1.ticket_id, "B001")
        self.assertEqual(t2.ticket_id, "B002")
        self.assertEqual(t1.status, TicketStatus.WAITING)

    def test_call_next_for_specific_service(self):
        manager = QueueManager()
        manager.issue_ticket("billing")
        manager.issue_ticket("support")

        next_billing = manager.call_next("billing")

        self.assertIsNotNone(next_billing)
        self.assertEqual(next_billing.ticket_id, "B001")
        self.assertEqual(next_billing.status, TicketStatus.CALLED)
        self.assertEqual(len(manager.get_waiting_tickets("billing")), 0)

    def test_call_next_without_service_uses_first_available_queue(self):
        manager = QueueManager()
        manager.issue_ticket("support")
        manager.issue_ticket("billing")

        first = manager.call_next()
        second = manager.call_next()

        self.assertEqual(first.ticket_id, "S001")
        self.assertEqual(second.ticket_id, "B001")

    def test_mark_served_updates_ticket_status(self):
        manager = QueueManager()
        ticket = manager.issue_ticket("general")

        called = manager.call_next("general")
        manager.mark_served(called)

        self.assertEqual(called.ticket_id, ticket.ticket_id)
        self.assertEqual(called.status, TicketStatus.SERVED)


if __name__ == "__main__":
    unittest.main()
