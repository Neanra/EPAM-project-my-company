import unittest
import warnings
from sqlalchemy import exc
from datetime import date

from sqlalchemy.sql.coercions import expect
from department_app import create_app, db
import department_app
from department_app.models.entities import Department, Employee
from decimal import Decimal

class BaseTestCase(unittest.TestCase):
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

    def _create_test_department(self):
        department = Department(name="Accounting")
        anna = Employee(first_name="Anna", last_name="Smith", 
                        date_of_birth = date.fromisoformat("2000-11-11"),
                        monthly_salary = "1000.24")
        bob = Employee(first_name="Bob", last_name="Smith", 
                        date_of_birth = date.fromisoformat("2000-10-10"),
                        monthly_salary = "900")
        anna.department = department
        bob.department = department
        db.session.add_all([department, anna, bob])
        db.session.commit()
        return department

class DepartmentTestCase(BaseTestCase):
    def test_to_dict(self):
        department = Department(id=1, name="IT")
        expected_dict = {"id":"1", "name":"IT"}
        self.assertEqual(department.to_dict(), expected_dict)

    def test_to_api_dict(self):
        department = self._create_test_department()
        expected_dict = {"id":department.id, "name":"Accounting", "employees_count":2,
                        "average_monthly_salary": 950.12}
        self.assertEqual(department.to_api_dict(), expected_dict)

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
        self.assertIsNone(department.id, None)
        self.assertEqual(department.name, "Accounting")

    def test_employee_count(self):
        department = self._create_test_department()
        self.assertEqual(department.employees_count, 2)

    def test_average_monthly_salary(self):
        department = self._create_test_department()
        self.assertEqual(department.average_monthly_salary, Decimal('950.12'))

    def test_average_monthly_salary_no_employees(self):
        department = Department(id=1, name="IT")
        self.assertIsNone(department.average_monthly_salary)

class EmployeeTestCase(BaseTestCase):
    def test_to_dict(self):
        anna = Employee(id=1, department_id=2010, first_name="Anna", last_name="Smith", 
                        date_of_birth = date.fromisoformat("2000-11-11"),
                        monthly_salary = "1000.24")
        expected_dict = {'id': "1", 
                'first_name': "Anna", 
                'last_name': "Smith",
                'date_of_birth': "2000-11-11", 
                'monthly_salary': "1000.24",
                'department_id': "2010"}
        self.assertEqual(anna.to_dict(), expected_dict)
