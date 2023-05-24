from datetime import datetime, timedelta
from src.settings import *
from src.utils.databasehandler import *


def check_timeout(user_id: int, login_tries: int, timeout: datetime, connection) -> str:
    if timeout == None:
        return None
    
    timeout_time = datetime.fromisoformat(timeout)
    current_time = datetime.now()

    if current_time > timeout_time:
        remove_timeout(user_id, connection)
    
    else:
        timeout_duration = timeout_time - current_time
        
        minutes = (timeout_duration.seconds % 3600) // 60
        seconds = timeout_duration.seconds % 60
        
        return f"{minutes}:{seconds}"


def clear_tries(user_id: int, connection):
    number_tries = 0
    update_login_tries(user_id, number_tries, None, connection)


def check_last_try(user_id: int, login_tries: int, last_try: datetime, connection) -> int:
    if last_try == None:
        return login_tries
    
    last_try = datetime.fromisoformat(last_try)
    current_time = datetime.now()

    since_last_try = current_time - last_try
    reset_tries = timedelta(minutes = 15)

    if since_last_try > reset_tries:
        login_tries = 0
        clear_tries(user_id, connection)
    
    return login_tries


def failed_login(user_id: int, login_tries: int, last_try: datetime, connection) -> int:
    login_tries = check_last_try(user_id, login_tries, last_try, connection)

    if login_tries < TRIES_TO_TIMEOUT - 1:
        login_tries += 1

        current_time = (datetime.now()).isoformat()
        update_login_tries(user_id, login_tries, current_time, connection)

    else:
        login_tries += 1

        timeout_until = (datetime.now() + timedelta(minutes = 15)).isoformat()
        timeout_user(user_id, timeout_until, connection)

    tries_left = TRIES_TO_TIMEOUT - login_tries

    return tries_left
