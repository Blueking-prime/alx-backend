#!/usr/bin/env python3
'''A basic flask app'''
from flask import Flask, render_template, request, g
from flask_babel import Babel
from pytz import timezone, UnknownTimeZoneError

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    '''Basic config class'''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.before_request
def before_request() -> None:
    '''Retreives user before displaying webpage'''
    g.user = get_user()


@babel.localeselector
def get_locale():
    '''Gets the best locale from our config'''
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    '''Gets the best timezone'''
    try:
        tzone = request.args.get('timezone')
        if tzone:
            return timezone(tzone)
        if g.user['timezone']:
            return timezone(g.user['timezone'])
    except UnknownTimeZoneError:
        pass
    finally:
        return timezone(app.config['BABEL_DEFAULT_TIMEZONE'])


@app.route('/', strict_slashes=False)
def index() -> str:
    '''Returns a basic homepage'''
    return render_template('6-index.html')


def get_user() -> object:
    '''Returns a user's details'''
    id = request.args.get('login_as')
    if id:
        id_n = int(id)
        if id_n in users:
            return users[id_n]

    return None


# babel.init_app(app, locale_selector=get_locale)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
