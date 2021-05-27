import unittest
import warnings
from sqlalchemy import exc
from datetime import date
from department_app import create_app, db
from department_app.models.entities import Department, Employee

class DepartmentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        warnings.simplefilter("ignore", category=exc.SAWarning)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_to_dict(self):
        department = Department(id=1, name="IT")
        expected_dict = {"id":"1", "name":"IT"}
        self.assertEqual(department.to_dict(), expected_dict)

    def test_to_dict_no_id(self):
        department = Department(name="23")
        expected_dict = {"id":"None", "name":"23"}
        self.assertEqual(department.to_dict(), expected_dict)

    def test_populate_from_dict(self):
        source_dict = {"name":"Sales and Marketing"}
        department = Department()
        department.populate_from_dict(source_dict)
        self.assertEqual(department.id, None)
        self.assertEqual(department.name, "Sales and Marketing")

    def test_populate_from_empty_dict(self):
        source_dict = {}
        department = Department(name="Accounting")
        department.populate_from_dict(source_dict)
        self.assertEqual(department.id, None)
        self.assertEqual(department.name, "Accounting")

    def test_employee_count(self):
        department = Department(name="Accounting")
        anna = Employee(first_name="Anna", last_name="Smith", 
                        date_of_birth = date.fromisoformat("2000-11-11"),
                        monthly_salary = "1000.23")
        bob = Employee(first_name="Bob", last_name="Smith", 
                        date_of_birth = date.fromisoformat("2000-10-10"),
                        monthly_salary = "900")
        anna.department = department
        bob.department = department
        db.session.add_all([department, anna, bob])
        db.session.commit()
        self.assertEqual(department.employees_count, 2)