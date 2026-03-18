# Queue Management System (QMS)

A minimal Queue Management System starter repository.

## Features

- Issue queue tickets by service type (e.g. billing, support)
- Call next ticket by service type or globally
- Mark called tickets as served
- View waiting tickets

## Project Structure

- `qms/queue_manager.py` – core queue logic
- `tests/test_queue_manager.py` – focused unit tests

## Run Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Example Usage

```python
from qms import QueueManager

manager = QueueManager()
manager.issue_ticket("billing")   # B001
manager.issue_ticket("support")   # S001

next_ticket = manager.call_next("billing")
manager.mark_served(next_ticket)
```
