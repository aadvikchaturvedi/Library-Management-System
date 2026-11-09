# Library Management System

A small library admin app: a Streamlit UI over a MySQL database for managing books, members and staff, issuing and returning books, and charging late fines. It's a single-process app; Streamlit calls a `LibraryDB` class that runs parameterized SQL through `mysql-connector-python`.

## What it does

| Section | Features |
|---|---|
| Dashboard | Metrics for total copies, issued copies, available copies and members; transactions table |
| Books | View, add, search by name (`LIKE`), update. Fields: name, quantity on shelf, issued quantity, shelf address, status |
| Members | View, add, update. Fields: name, contact number, address, age, gender, accumulated penalty |
| Staff | View, add, update. Fields: name, age, gender, role |
| Transactions | Issue a book to a member with a due date (1–60 days, default 14), return a book, view all transactions |

**Issue / return logic** (`src/backend/crud.py`):

- Issuing checks the book exists and has copies on the shelf, inserts a transaction, then moves one copy from `quantity` to `issuedQuantity`.
- Returning rejects already-returned transactions, computes a fine of 5 per day late, sets `returnDate` and `fine`, moves the copy back to the shelf, and adds the fine to the member's `penalty`.

## Architecture

```
app.py                     Streamlit entry: page config, sidebar routing, cached LibraryDB in session_state
src/
  components/              one Streamlit view per section (tabs + forms)
    sidebar.py dashboard.py books.py members.py staff.py transactions.py
  backend/
    crud.py                LibraryDB: connection + all SQL (CRUD, issue/return, dashboard counts)
    db_init.py             creates the database and the four tables
    dbSetup.py             older connection helper, not used by the app
  models/                  dataclasses passed between UI and DB layer
    book.py member.py staff.py transaction.py category.py library.py
```

Schema (from `db_init.py`): `books`, `members`, `staff`, and `transactions` (foreign keys to `books` and `members`).

## Running locally

Requires Python 3 and a running MySQL server.

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Configuration is read from environment variables (no `.env` loader is used, so export them in your shell):

| Variable | Default |
|---|---|
| `DB_HOST` | `localhost` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | empty |
| `DB_NAME` | `library_management` |

```bash
export DB_PASSWORD=<your-mysql-password>

# create the database and tables
python -m src.backend.db_init

# start the app (http://localhost:8501)
streamlit run app.py
```

## Limitations / next steps

- **Availability is computed two ways.** `quantity` is copies on the shelf (issuing decrements it, and the dashboard counts total copies as `quantity + issuedQuantity`), but the Issue form lists a book only if `quantity - issuedQuantity > 0`. A book with 2 on the shelf and 2 issued won't be offered for issue.
- `delete_book`, `delete_member` and `delete_staff` exist in `crud.py` but have no UI.
- The `Book` dataclass declares category, issuedBy and defaulters fields, and there are `Category` and `Library` models, but none of these have tables yet.
- No authentication: anyone who can reach the Streamlit app can edit data.
- Fines are added to `members.penalty` but there's no way to record a payment.
- `requirements.txt` lists FastAPI and SQLModel, which the code doesn't use.
- No tests.
