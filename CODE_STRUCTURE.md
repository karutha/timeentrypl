# Code Structure

The TimeTracker application has been modularized for better maintainability.

## Directory Structure

```
time_entry/
├── app.py                  # Main application entry point
├── data_manager.py         # Data persistence layer
├── utils.py                # Shared utilities and styling
├── pages/                  # Page modules
│   ├── __init__.py
│   ├── time_entry.py      # Time Entry page
│   ├── summary.py         # Summary page
│   ├── users.py           # Users management page
│   ├── payments.py        # Payments tracking page
│   └── periods.py         # Periods management page
├── data/                   # JSON data files (gitignored)
└── .streamlit/            # Streamlit configuration
    └── config.toml
```

## Module Descriptions

### `app.py`
Main application entry point. Handles:
- Page configuration
- Navigation routing
- Applying custom styles

### `utils.py`
Shared utilities including:
- `apply_custom_styles()` - Applies custom CSS
- `format_duration()` - Formats hours as "Xh Ym"

### `data_manager.py`
Data persistence layer with functions for:
- User management (CRUD operations)
- Period management
- Time entry management
- Payment tracking

### `pages/` Directory
Each page module has a `render()` function that displays the page content:
- **time_entry.py** - Add and view time entries
- **summary.py** - Bi-weekly summary with cumulative totals
- **users.py** - Manage users (add, edit, delete)
- **payments.py** - Track payment status per period
- **periods.py** - Manage bi-weekly periods

## Benefits of Modularization

1. **Maintainability** - Each page is in its own file
2. **Readability** - Smaller, focused modules
3. **Reusability** - Shared utilities in `utils.py`
4. **Scalability** - Easy to add new pages
5. **Testing** - Easier to test individual modules
