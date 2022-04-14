from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate
from src.pylintTest import PylintTest
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
        self.pylintTest = PylintTest()
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
            return render_template("base.html", file_text = file_text, file_io="")

        @self.flask_app.route("/process", methods=["POST"])
        def process_code():
            file_text = request.form.get("codeinput")
            file_io, suggestions, score = analyze(file_text)
            fileDict = self.pylintTest.parseOutput()
            return render_template("base.html", file_text = file_text, file_io=file_io, suggestions=suggestions, score=score)

        def analyze(file_text):
            file_io = self.pylintTest.analyze(file_text)

            score_index =file_io.index('Your code has been rated at')
            len_string = len('Your code has been rated at')
            score = file_io[score_index+len_string:]

            dash_index =file_io.index("---------")

            file_io = file_io[:dash_index]

            suggestions =[]

            # Bad Indentation
            if "W0311" in file_io:
                suggestions.append("Indentation")
            # Invalid Name
            if "C0103" in file_io:
                suggestions.append("Naming Conventions")
            # Missing module docstring
            if "C0114" in file_io:
                suggestions.append("Docstrings")
            # Consider using enumerate
            if "C0200" in file_io:
                suggestions.append("Consider using enumerate")

            return file_io, suggestions, score

        @self.flask_app.route('/tutorials/')
        def tutorials():
            return render_template("tutorials.html")

        @self.flask_app.route('/dashboard/')
        def dashboard():
            return render_template("dashboard.html")


if __name__ == "__main__":
    app = Application()
    app.flask_app.run(debug=True)
