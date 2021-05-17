from decimal import Decimal
from flask import Flask, render_template, request, abort, redirect, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()

from .models.entities import Department, Employee

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://department_app:sleep42@localhost/department_app"
    app.config["SECRET_KEY"] = "g5g5h4jytj65j56j"
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

    @app.route("/departments/<int:id>/delete", methods=["GET","POST"])
    def delete_department(id):
        department = Department.query.get(id)
        if not department:
            return "Department not found", 404
        if request.method == "POST":
            try:
                for employee in department.employees:
                    db.session.delete(employee)
                db.session.delete(department)
                db.session.commit()
                flash("Department {} deleted successfully!".format(department.name))
                return redirect("/departments")
            except:
                flash("Department not deleted!")
                return redirect("/departments/{}".format(department.id))

            finally:
                return redirect("/departments")
        else:
            assert request.method == "GET"
            return render_template("delete_department.html.jinja", department=department)

    @app.route("/employees")
    def employees():
        employees = Employee.query.all()
        employees.sort(key=lambda x: x.full_name)
        return render_template("employees.html.jinja", employees=employees)

    @app.route("/employees/<int:id>")
    def view_employee(id):
        employee = Employee.query.get(id)
        if not employee:
            return "Employee not found", 404
        return render_template("view_employee.html.jinja", employee=employee)

    @app.route("/employees/<int:id>/delete", methods=["GET","POST"])
    def delete_employee(id):
        employee = Employee.query.get(id)
        if not employee:
            return "Employee not found", 404
        if request.method == "POST":
            try:
                db.session.delete(employee)
                db.session.commit()
                flash("Employee {} record deleted successfully!".format(employee.full_name))
                return redirect("/employees")
            except:
                flash("Employee record not deleted!")
                return redirect("/employees/{}".format(employee.id))
        else:
            assert request.method == "GET"
            return render_template("delete_employee.html.jinja", employee=employee)

    return app 