# Library Management System

A comprehensive web-based library management application built with Python, designed to help libraries efficiently manage books, members, staff, and transactions.

## Features

- **📚 Book Management**: Add, update, and delete books with categories and detailed information
- **👥 Member Management**: Register and manage library members with membership tracking
- **👔 Staff Management**: Manage library staff information and roles
- **📋 Dashboard**: Get an overview of library statistics and key metrics
- **💳 Transactions**: Track book checkouts, returns, and member activities
- **🎯 Sidebar Navigation**: Intuitive navigation for easy access to all features

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io) - Fast, interactive web framework
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - Modern REST API framework
- **Database**: MySQL - Relational database
- **ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) / [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- **Data Processing**: [Pandas](https://pandas.pydata.org/) - Data analysis library
- **API Documentation**: [Pydantic](https://docs.pydantic.dev/) - Data validation

## Project Structure

```
LibraryMangementSys/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
└── src/
    ├── backend/
    │   ├── crud.py          # Database CRUD operations
    │   ├── db_init.py       # Database initialization
    │   └── dbSetup.py       # Database setup configuration
    ├── components/          # Streamlit UI components
    │   ├── books.py         # Books management UI
    │   ├── dashboard.py     # Dashboard UI
    │   ├── members.py       # Members management UI
    │   ├── sidebar.py       # Sidebar navigation
    │   ├── staff.py         # Staff management UI
    │   └── transactions.py  # Transactions UI
    └── models/              # Data models
        ├── book.py
        ├── category.py
        ├── library.py
        ├── member.py
        ├── staff.py
        └── transaction.py
```

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server running locally or accessible remotely
- pip (Python package manager)

### Setup Steps

1. **Clone the repository** (if using version control):
   ```bash
   git clone <repository-url>
   cd LibraryMangementSys
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**:
   - Ensure MySQL is running
   - Update database configuration in `src/backend/dbSetup.py` with your MySQL credentials
   - Initialize the database:
     ```bash
     python -c "from src.backend.db_init import init_db; init_db()"
     ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

   The application will open in your default browser at `http://localhost:8501`

## Usage

### Main Dashboard
- Start by viewing the Dashboard to see library statistics and metrics
- Use the sidebar to navigate to different sections

### Managing Books
- Add new books with title, author, ISBN, and category
- View all books in the system
- Edit book details
- Delete books (with appropriate permissions)

### Managing Members
- Register new library members
- View active and inactive members
- Update member information
- Track member transaction history

### Managing Staff
- Add staff members to the library
- Update staff information
- Manage staff roles and permissions

### Viewing Transactions
- View all checkout and return transactions
- Filter transactions by date, member, or book
- Track transaction history

## Database Models

### Core Models
- **Book**: Stores book information (title, author, ISBN, category, availability)
- **Category**: Book categories for organization
- **Member**: Library member information
- **Staff**: Library staff information
- **Transaction**: Record of book checkouts and returns
- **Library**: Main library information and configuration

## Configuration

Key configuration files:
- `src/backend/dbSetup.py` - Database connection settings
- `app.py` - Streamlit page configuration and layout settings

Update database credentials in `dbSetup.py`:
```python
DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/library_db"
```

## Dependencies

Key packages included:
- `streamlit` - Web framework
- `fastapi` - REST API framework
- `sqlmodel` - SQL ORM
- `pandas` - Data analysis
- `mysql-connector-python` - MySQL driver
- `pydantic` - Data validation
- `requests` - HTTP library

See `requirements.txt` for the complete list.

## Features in Development

- User authentication and authorization
- Advanced search and filtering
- Reporting and analytics
- Email notifications for overdue books
- Fine calculation system

## Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check database credentials in `dbSetup.py`
- Ensure the database exists

### Import Errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python path and virtual environment activation

### Streamlit Issues
- Clear cache: Delete `.streamlit/cache_` directory
- Restart the application: `streamlit run app.py`

## Contributing

Contributions are welcome! Please:
1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please create an issue in the repository or contact the development team.

## Author

Developed as a Library Management System solution.

---

**Last Updated**: April 2026
