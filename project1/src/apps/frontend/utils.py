def get_form_errors(form):
    errors_list = [''.join(e) for e in form.errors.values()]
    return {'error': ''.join(errors_list)}


def is_valid_password(password, password_repeat):
    return password and password_repeat and password == password_repeat
