from quart import Quart, Blueprint
from .views import blog
from .extensions import database
from .template_filters import pretty_date
from quart_cors import cors


def create_app(config_file='settings.py'):
    app = Quart(__name__)
    app = cors(app, allow_origin="*")
    app.debug = True
    app.register_blueprint(blog)
    app.config.from_pyfile(config_file)
    app.jinja_env.filters['humanize'] = pretty_date

    @app.before_serving
    async def create_db_pool():
        await database.connect()
        if database.is_connected:
            app.db = database
            app.logger.info("Connected!")
        else:
            app.logger.warn('Not connected to database.')
            
    @app.after_serving
    async def remove_db_pool():
        await app.db.disconnect()

    return app
