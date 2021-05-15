from decimal import Decimal
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()

from .models.entities import Department, Employee

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://department_app:sleep42@localhost/department_app"
    bootstrap.init_app(app)
    db.init_app(app)

    @app.route("/departments")
    def departments():
        departments = Department.query.all()
        departments.sort(key=lambda x: x.average_monthly_salary if x.average_monthly_salary else -1, reverse=True)
        return render_template("departments.html.jinja", departments=departments)

    @app.route("/departments/<int:id>")
    def view_department(id):
        department = Department.query.get(id)
        if not department:
            return "Department not found", 404
        return render_template("view_department.html.jinja", department=department)

    @app.route("/employees")
    def employees():
        employees = Employee.query.all()
        employees.sort(key=lambda x: x.full_name)
        return render_template("employees.html.jinja", employees=employees)

    return app 