from department_app import db
from decimal import Decimal

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    employees = db.relationship("Employee", backref='department')
    
    @property
    def average_monthly_salary(self):
        count = len(self.employees)
        if not count:
            return None
        return Decimal(sum([employee.monthly_salary for employee in self.employees]) / count).quantize(Decimal('0.01'))
    @property
    def employees_count(self):
        return len(self.employees)

    def __repr__(self):
        return '<Department {}>'.format(self.name)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    monthly_salary = db.Column(db.Numeric(10,2), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    full_name = db.column_property(last_name + " " + first_name)

    def __repr__(self):
        return '<Employee {}>'.format(self.full_name)

