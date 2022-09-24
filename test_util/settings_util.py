
def create_log_setting_form(value: bool):
    return {'log-setting': value}


def create_email_form(email: str):
    return {'email': email}


def create_delete_form(password: str):
    return {'password': password}


def create_change_password_form(password: str, confirmation: str):
    return {'password': password, 'confirm_password': confirmation}
