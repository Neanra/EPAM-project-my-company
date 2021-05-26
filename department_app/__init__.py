"""
@author: Julia Issajeva

This package is a flask web service and application that allows to create and maintain
records for departments and employees of a company.
"""

from decimal import Decimal
from flask import Flask, render_template, request, abort, redirect, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy import and_

bootstrap = Bootstrap()
db = SQLAlchemy()

from .models.entities import Department, Employee

def create_app():
    """
    Initializes and returns flask application instance for department app.
    
    Returns: Flask application instance.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://department_app:sleep42@localhost/department_app"
    app.config["SECRET_KEY"] = "g5g5h4jytj65j56j"
    bootstrap.init_app(app)
    db.init_app(app)

    @app.route("/")
    def index():
        """Redirects user to departments listing page."""
        return redirect("/departments")

    @app.route("/search")
    def search():
        """Displays employee search form."""
        today = date.today().isoformat()
        return render_template("search.html.jinja", today=today)

    @app.route("/departments")
    def departments():
        """Displays departments list."""
        departments = Department.query.all()
        departments.sort(key=lambda x: x.average_monthly_salary if x.average_monthly_salary else -1, reverse=True)
        return render_template("departments.html.jinja", departments=departments)

    @app.route("/departments/<int:id>")
    def view_department(id):
        """Displays department."""
        department = Department.query.get(id)
        if not department:
            return "Department not found", 404
        return render_template("view_department.html.jinja", department=department)

    @app.route("/departments/<int:id>/delete", methods=["GET","POST"])
    def delete_department(id):
        """Deletes department by id."""
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
        """Displays and processes edit department form for new or existing department."""
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
        """Displays employees list possibly filtered by birth date."""
        from_date = request.args.get("from_date", default=None)
        to_date = request.args.get("to_date", default=None)
        employees = Employee.query.all()
        if from_date and to_date:
            employees = Employee.query.filter(and_(Employee.date_of_birth >= date.fromisoformat(from_date),\
            Employee.date_of_birth <= date.fromisoformat(to_date))).all()
        else:
            employees = Employee.query.all()
        employees.sort(key=lambda x: x.full_name)
        return render_template("employees.html.jinja", employees=employees)

    @app.route("/employees/<int:id>")
    def view_employee(id):
        """Displays employee."""
        employee = Employee.query.get(id)
        if not employee:
            return "Employee not found", 404
        return render_template("view_employee.html.jinja", employee=employee)

    @app.route("/employees/<int:id>/delete", methods=["GET","POST"])
    def delete_employee(id):
        """Deletes employee"""
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
        """Displays and processes edit employee form for new or existing employee."""
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
        
    @app.route("/api")
    def api():
        """Returns links to supported root endpoints."""
        return jsonify({"links":{"departments":"/api/departments", "employees":"/api/employees"}})
    
    @app.route("/api/departments", methods=["GET"])
    def departments_api():
        """Returns a listing of all departments."""
        departments = Department.query.all()
        departments.sort(key=lambda x: x.average_monthly_salary if x.average_monthly_salary else -1, reverse=True)
        result = []
        for department in departments:
            result.append({"content": department.to_api_dict(), 
                           "links": {"self": "/api/departments/{}".format(department.id)}})
        return jsonify(result)
    
    @app.route("/api/departments/<int:id>")
    def view_department_api(id):
        """Returns a single department record."""
        department = Department.query.get(id)
        if not department:
            return jsonify({"error":"Department not found"}), 404
        return jsonify({"content": department.to_api_dict(), 
                        "links": {"self": "/api/departments/{}".format(department.id)}})
    
    @app.route("/api/departments/<int:id>", methods=["PUT"])
    @app.route("/api/departments", methods=["POST"])
    def edit_department_api(id=None):
        """Creates or modifies department record based on client request."""
        department = Department() if id is None else Department.query.get(id)
        if not department:
            return jsonify({"error":"Department not found"}), 404
        try:
            request_dict = request.get_json(force=True)
            if request_dict is None:
                return jsonify({"error":"Invalid json"}), 400
            department.populate_from_dict(request_dict)
            db.session.add(department)
            db.session.commit()
            return jsonify({"content": department.to_api_dict(), 
                        "links": {"self": "/api/departments/{}".format(department.id)}})
        except (ValueError, TypeError) as e:
            return jsonify({"error":str(e)}), 400
        except:
            db.session.rollback()
            return jsonify({"error":"Database insertion failed!"}), 400
    
    @app.route("/api/departments/<int:id>", methods=["DELETE"])
    def delete_department_api(id):
        """Deletes department record based by the given id."""
        department = Department.query.get(id)
        if not department:
            return jsonify({"error":"Department not found"}), 404
        try:
            for employee in department.employees:
                db.session.delete(employee)
            db.session.delete(department)
            db.session.commit()
            return jsonify({})
        except:
            db.session.rollback()
            return jsonify({"error":"Department record not deleted!"}), 400

    @app.route("/api/employees")
    def employees_api():
        """Returns a listing of all employees."""
        employees = Employee.query.all()
        employees.sort(key=lambda x: x.full_name)
        result = []
        for employee in employees:
            result.append({"content": employee.to_api_dict(),
                           "links": {"self": "/api/employees/{}".format(employee.id),
                                     "department": "/api/departments/{}".format(employee.department_id)}})
        return jsonify(result)

    @app.route("/api/employees/<int:id>")
    def view_employee_api(id):
        """Returns a single employee record."""
        employee = Employee.query.get(id)
        if not employee:
            return jsonify({"error":"Employee not found"}), 404
        return jsonify({"content": employee.to_api_dict(),
                        "links": {"self": "/api/employees/{}".format(employee.id),
                                  "department": "/api/departments/{}".format(employee.department_id)}})

    @app.route("/api/employees/<int:id>", methods=["PUT"])
    @app.route("/api/employees", methods=["POST"])
    def edit_employee_api(id=None):
        """Creates or modifies employee record based on client request."""
        employee = Employee() if id is None else Employee.query.get(id)
        if not employee:
            return jsonify({"error":"Employee not found"}), 404
        try:
            request_dict = request.get_json(force=True)
            if request_dict is None:
                return jsonify({"error":"Invalid json"}), 400
            employee.populate_from_dict(request_dict)
            db.session.add(employee)
            db.session.commit()
            return jsonify({"content": employee.to_api_dict(), 
                            "links": {"self": "/api/employees/{}".format(employee.id), 
                            "department": "/api/departments/{}".format(employee.department_id)}})
        except (ValueError, TypeError) as e:
            return jsonify({"error":str(e)}), 400
        except:
            db.session.rollback()
            return jsonify({"error":"Database insertion failed!"}), 400    

    @app.route("/api/employees/<int:id>", methods=["DELETE"])
    def delete_employee_api(id):
        """Deletes employee record based by the given id."""
        employee = Employee.query.get(id)
        if not employee:
            return jsonify({"error":"Employee not found"}), 404
        try:
            db.session.delete(employee)
            db.session.commit()
            return jsonify({})
        except:
            db.session.rollback()
            return jsonify({"error":"Employee record not deleted!"}), 400

    return app 