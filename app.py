from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate

#from src import routes, utils as u
#from src.models import db
#from src.settings import Settings as S
#from src.tasks import make_celery
#import io


file_text = "def __init__(): self.number = 1"


    #@classmethod
    #def boot(cls):
    #    """Begin the application"""
    #    app = cls()
    #    app.run()
    #    return app
class Application:

    def __init__(self):
        #self.init_flask()
        self.flask_app = Flask(__name__, static_url_path='/static')
        self.init_routes()

    '''def init_flask(self):
        # Init Flask
        self.flask_app = Flask(__name__, static_url_path='/static')
        self.flask_app.config.from_object(S)

        # Register the public routes
        for blueprint in [routes.counter]:
            self.flask_app.register_blueprint(blueprint)

        # Init Celery
        self.celery = make_celery(self.flask_app)

        # Init Flask-SQLAlchemy
        self.db = db
        self.db.init_app(self.flask_app)

        # Init Flask-Migrate
        u.wait_for_service('postgres', 5432, timeout=30.0)
        self.migrate = Migrate(self.flask_app, self.db)'''

    def init_routes(self):

        @self.flask_app.route("/")
        def index():
            return render_template("base.html", file_text = "i == 1 or i%2 == 1")

        @self.flask_app.route("/process", methods=["POST"])
        def process_code():
            file_text = get_text()
            return redirect(url_for("index"))

        def get_text():
            return request.form["codeinput"]


if __name__ == "__main__":
    app = Application()
    app.flask_app.run()
