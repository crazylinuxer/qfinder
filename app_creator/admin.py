from flask import Flask, redirect, request, session
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_babelex import Babel
from flask_security import (current_user, Security, logout_user,
                            SQLAlchemyUserDatastore, RoleMixin, UserMixin)

from repository import db
import repository


roles_users = db.Table(
    'admins_to_roles',
    db.Column('admin_id', db.Integer(), db.ForeignKey('admins.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


class Administrator(db.Model, UserMixin):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('admins', lazy='dynamic')
    )


class CommonAdmin(sqla.ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


class UserAdmin(CommonAdmin):
    column_exclude_list = ('password_hash',)
    form_excluded_columns = ('password_hash',)


def create_admin_page(app: Flask):
    babel = Babel(app)
    Security(app, SQLAlchemyUserDatastore(db, Administrator, Role))
    admin = Admin(app)

    @app.route('/admin/login', methods=["GET", "POST"])
    def admin_login():
        if current_user.is_authenticated:
            return redirect("/admin")
        return redirect('/login?next=/admin')

    @app.route('/admin/logout')
    def logout():
        if current_user.is_authenticated:
            logout_user()
        return redirect("/admin/login")

    @babel.localeselector
    def get_locale():
        if request.args.get('lang'):
            session['lang'] = request.args.get('lang')
        return session.get('lang', 'ru')

    admin.add_view(UserAdmin(repository.User, db.session))
    for table in (
            repository.Product, repository.ProductType, repository.ProductPicture, repository.Tag,
            repository.TagToProduct, repository.WishListItem, repository.Feedback, repository.CartItem
    ):
        admin.add_view(CommonAdmin(table, db.session))

    return admin
