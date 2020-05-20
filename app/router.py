from .controllers import home, user, character

def routes(app):
    '''All Routes / Url
    This app uses an MVC pattern, hence all the url are routed here
    Just import your logics from the controllers package and route
    using the add_url_rule function

    :param app: Flask app instance
    :return: None
    '''

    # Common errors handled already for you. you can add more
    app.register_error_handler(403, home.error_pages)
    app.register_error_handler(404, home.error_pages)
    app.register_error_handler(500, home.error_pages)

    # Add your Url rules here
    app.add_url_rule('/', view_func=home.index)
    app.add_url_rule('/register', view_func=user.register, methods=['GET','POST'])
    app.add_url_rule('/login', view_func=user.login, methods=['GET','POST'])
    app.add_url_rule('/logout', view_func=user.logout)
    app.add_url_rule('/char/create', view_func=character.create, methods=['GET','POST'])
    app.add_url_rule('/char', view_func=character.show, methods=['GET','POST'])

