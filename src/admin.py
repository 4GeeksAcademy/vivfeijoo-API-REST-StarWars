import os
from flask_admin import Admin
from src.models import db, User, People, Planet, Favorite
from flask_admin.contrib.sqla import ModelView

class NoAuthModelView(ModelView):
    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        return self.handle_view(name, **kwargs)


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(NoAuthModelView(User, db.session))
    admin.add_view(NoAuthModelView(People, db.session))
    admin.add_view(NoAuthModelView(Planet, db.session))
    admin.add_view(NoAuthModelView(Favorite, db.session))
