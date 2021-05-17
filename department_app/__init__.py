from decimal import Decimal
from flask import Flask, render_template, request, abort, redirect, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import date

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

    @app.route("/")
    def index():
        return redirect("/departments")

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

    @app.route("/departments/new/edit", methods=["GET", "POST"])
    @app.route("/departments/<int:id>/edit", methods=["GET", "POST"])
    def edit_department(id=None):
        department = Department() if id is None else Department.query.get(id)
        response_code = 200
        if not department:
            return "Department not found", 404
        if request.method == "POST":
            try:
                department.populate_from_dict(request.form)
                db.session.add(department)
                db.session.commit()
                return redirect("/departments/{}".format(department.id))
            except ValueError as e:
                flash(str(e))
                response_code = 400
            except:
                flash("Database insertion failed!")
                db.session.rollback()
                response_code = 400
        return render_template("edit_department.html.jinja", department=department, 
                                form=department.to_dict()), response_code

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

    @app.route("/employees/new/edit", methods=["GET", "POST"])
    @app.route("/employees/<int:id>/edit", methods=["GET", "POST"])
    def edit_employee(id=None):
        employee = Employee() if id is None else Employee.query.get(id)
        departments = Department.query.all()
        today = date.today().isoformat()
        response_code = 200
        if not employee:
            return "Employee not found", 404
        if request.method == "POST":
            try:
                employee.populate_from_dict(request.form)
                db.session.add(employee)
                db.session.commit()
                return redirect("/employees/{}".format(employee.id))
            except ValueError as e:
                flash(str(e))
                response_code = 400
            except:
                flash("Database insertion failed!")
                db.session.rollback()
                response_code = 400
        return render_template("edit_employee.html.jinja", employee=employee, 
                            departments=departments, today=today, form=employee.to_dict()), response_code

    return app 