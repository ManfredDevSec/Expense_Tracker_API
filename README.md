# Expense_Tracker_API
A backend API for tracking expenses, assigning categories, and generating simple reports

Core Features:
	•	User registration & login
	•	CRUD for expenses (amount, date, category, notes)
	•	CRUD for categories
	•	Filtering by date range, category, and amount
	•	Pagination on list endpoints
	•	Monthly and yearly summary endpoints
	•	Input validation + clear error messages
	•	Basic logging

# Steps to set up the project:
1. Clone the repo
2. Create a python environment
3. Install requirements : pip install -r requirements.txt
4. Create a .env in the project root and add the env vars: DEBUG, SECRET_KEY
5. Run "python manage.py makemigrations && python manage.py migrate"

## Repository structure

- server/: Django project settings, ASGI/WSGI and URL routing
- users/: User model, authentication endpoints
- expenses/: Expenses tracking
- categories/: Category for expenses, has a foreign key to an expense


# ENDPOINTS.
Note: All endpoints require header- Content-Type: application/json

## Users

- POST api/auth/register/ : For user registration
		json example:
		{
			"first_name": "",
			"last_name": "",
			"email": "",
			"username": "",
			"password": "",
			"password2": ""
		}

- POST api/auth/login/ : For user login
		json example:
		{
			"username": "",
			"password": ""
		}

- POST, PATCH, GET api/auth/profile/ : For the users profile details
	Headers: Authorization : Bearer <access_token>

- POST api/auth/change-password/ : Allows the user change password
	Headers: Authorization : Bearer <access_token>
	json data:
		{
		"old_password" : "somepassword",
		"new_password" : "securepass",
		"new_password2" : "securepass"
	}

- POST api/auth/token-pair/ : To obtain the token pairs, i.e access and refresh tokens
	json data:
		{
		"username": "",
		"password": ""
	}

- api/auth/refresh-token/ : Accepts and refresh token and generates an access token
	json data:
		{
		"refresh": ""
	}

## Expenses
Methods required : POST, GET, PATCH, DELETE
Note: All endpoints require Authorization and Content-Type headers

- POST api/expenses/     For creating an expense
	json data:
		{
		"amount" : 3000,
		"category" : "food"
	}

- PATCH api/expenses/<expense_uuid>/  For edit an expense using the uuid

- GET api/expenses/    For getting all expenses

- DELETE api/expenses/<expense_uuid>/   To delete an expense

# Expense Filters
- List filter options : GET /api/expenses/expenses/filter_options/

- Date Range : GET /api/expenses/expenses/?start_date=2025-11-01&end_date=2025-11-30

- Amount Range : GET /api/expenses/expenses/?min_amount=50&max_amount=200

- Category : GET /api/expenses/expenses/?category=<category_uuid>

- Year/Month : GET /api/expenses/expenses/?year=2025&month=11

# Expense Ordering
- Ascending : GET /api/expenses/expenses/?ordering=amount

- Descending : GET /api/expenses/expenses/?ordering=-amount

- Multiple : GET /api/expenses/expenses/?ordering=date,-amount

# Expense Search
- Description : GET /api/expenses/expenses/?description=grocery

- General search : GET /api/expenses/expenses/search/?q=grocery

## Categories 
- Get categories : GET /api/categories/

- Create category : POST /api/categories/
	json fields = {"name", "description"}

- Update category : PATCH /api/categories/<category_uuid>/

