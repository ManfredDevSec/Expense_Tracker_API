import logging
import time
from django.utils import timezone


api_logger = logging.getLogger('expense_tracker')
security_logger = logging.getLogger('expense_tracker.security')
performance_logger = logging.getLogger('expense_tracker.performance')
user_logger = logging.getLogger('users')
expense_logger = logging.getLogger('expenses')
category_logger = logging.getLogger('categories')

class APILogger:
    @staticmethod
    def log_request(request, response=None, duration=None):
        user_info = "Anonymous"
        if request.user.is_authenticated:
            user_info = f"{request.user.username} ({request.user.id})"
        
        log_data = {
            'method': request.method,
            'path': request.path,
            'user': user_info,
            'query_params': dict(request.GET),
            'timestamp': timezone.now().isoformat(),
        }
        
        if response:
            log_data['status_code'] = response.status_code
            log_data['response_size'] = len(response.content) if hasattr(response, 'content') else 0
        
        if duration is not None:
            log_data['duration_ms'] = round(duration * 1000, 2)
            

            if duration > 1.0: 
                performance_logger.warning(f"Slow request: {duration:.2f}s - {log_data}")
        
        message = f"{request.method} {request.path} - User: {user_info} - Status: {response.status_code if response else 'N/A'}"
        
        if response and response.status_code >= 400:
            api_logger.warning(f"API Request Error: {log_data}")
        else:
            api_logger.info(f"API Request: {log_data}")
    
    @staticmethod
    def log_error(request, error, context=None):
        user_info = "Anonymous"
        if request.user.is_authenticated:
            user_info = f"{request.user.username} ({request.user.id})"
        
        error_data = {
            'method': request.method,
            'path': request.path,
            'user': user_info,
            'error': str(error),
            'error_type': type(error).__name__,
            'timestamp': timezone.now().isoformat(),
        }
        
        if context:
            error_data['context'] = context
        
        api_logger.error(f"API Error: {error_data}", exc_info=True)
    
    @staticmethod
    def log_security_event(event_type, user, details=None):
        user_info = "Anonymous"
        if user and user.is_authenticated:
            user_info = f"{user.username} ({user.id})"
        
        security_data = {
            'event_type': event_type,
            'user': user_info,
            'timestamp': timezone.now().isoformat(),
        }
        
        if details:
            security_data['details'] = details
        
        security_logger.warning(f"Security Event: {security_data}")

class UserLogger:
    @staticmethod
    def log_registration(user):
        user_logger.info(f"User registered: {user.username} ({user.id}) - Email: {user.email}")
        APILogger.log_security_event('USER_REGISTRATION', user)
    
    @staticmethod
    def log_login(user, method='password'):
        user_logger.info(f"User login: {user.username} ({user.id}) - Method: {method}")
    
    @staticmethod
    def log_login_failed(username, reason='invalid_credentials'):
        user_logger.warning(f"Failed login attempt: {username} - Reason: {reason}")
        APILogger.log_security_event('LOGIN_FAILED', None, {'username': username, 'reason': reason})
    
    @staticmethod
    def log_password_change(user):
        user_logger.info(f"Password changed: {user.username} ({user.id})")
        APILogger.log_security_event('PASSWORD_CHANGE', user)

class ExpenseLogger:
    @staticmethod
    def log_create(user, expense, amount, category):
        expense_logger.info(
            f"Expense created - User: {user.username} - "
            f"ID: {expense.id} - Amount: {amount} - Category: {category}"
        )
    
    @staticmethod
    def log_update(user, expense_id, changes=None):
        expense_logger.info(
            f"Expense updated - User: {user.username} - "
            f"ID: {expense_id} - Changes: {changes}"
        )
    
    @staticmethod
    def log_delete(user, expense_id):
        expense_logger.info(f"Expense deleted - User: {user.username} - ID: {expense_id}")
    
    @staticmethod
    def log_bulk_operation(user, operation, count):
        expense_logger.info(
            f"Bulk expense operation - User: {user.username} - "
            f"Operation: {operation} - Count: {count}"
        )

class CategoryLogger:
    @staticmethod
    def log_create(user, category):
        category_logger.info(f"Category created - User: {user.username} - Category: {category.name}")
    
    @staticmethod
    def log_delete(user, category_name):
        category_logger.info(f"Category deleted - User: {user.username} - Category: {category_name}")