#!/usr/bin/env python3
'''A basic flask app'''
from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    '''Basic config class'''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    '''Gets the best locale from our config'''
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    '''Returns a basic homepage'''
    return render_template('4-index.html')


# babel.init_app(app, locale_selector=get_locale)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
