from department_app import db
from decimal import Decimal, InvalidOperation
from datetime import date

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

    def to_dict(self):
        return {'id': str(self.id), 'name': self.name if self.name else ''}

    def to_api_dict(self):
        return {'id': self.id, 'name': self.name if self.name else '', 
                'average_monthly_salary': float(self.average_monthly_salary) if self.average_monthly_salary
                                            else None,
                'employees_count': self.employees_count}

    def populate_from_dict(self, d):
        if 'name' in d:
            if not isinstance(d['name'], str):
                raise TypeError("Name must be a string")
            if len(d['name']) < 1:
                raise ValueError("Name must not be empty")
            self.name = d['name']


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

    def to_dict(self):
        return {'id': str(self.id), 
                'first_name': self.first_name if self.first_name else '', 
                'last_name': self.last_name if self.last_name else '',
                'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else '', 
                'monthly_salary': str(self.monthly_salary) if self.monthly_salary is not None else '',
                'department_id': str(self.department_id) if self.department_id is not None else ''}

    def to_api_dict(self):
        return {'id': self.id, 
                'first_name': self.first_name, 
                'last_name': self.last_name,
                'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None, 
                'monthly_salary': float(self.monthly_salary) if self.monthly_salary is not None else None,
                'department_id': self.department_id}

    def populate_from_dict(self, d):
        if 'first_name' in d and len(d['first_name']) < 1:
            raise ValueError("First name must not be empty")
        if 'last_name' in d and len(d['last_name']) < 1:
            raise ValueError("Last name must not be empty")
        if 'date_of_birth' in d:
            try:
                date_of_birth = date.fromisoformat(d['date_of_birth'])
            except ValueError:
                raise ValueError("Date format is invalid. Should be YYYY-MM-DD")
            if date_of_birth >= date.today() or date_of_birth < date.fromisoformat('1900-01-01'):
                raise ValueError("Date is not in range between 1900-01-01 and today")
        else:
            date_of_birth = self.date_of_birth
        try:
            salary = Decimal(d['monthly_salary'])
        except (ValueError, InvalidOperation):
            raise ValueError("Salary must be a decimal number")
        except KeyError:
            salary = self.monthly_salary
        try:
            id = int(d['department_id'])
        except ValueError:
            raise ValueError("Department is not valid")
        except KeyError:
            id = self.department_id
        self.first_name = d.get('first_name', self.first_name)
        self.last_name = d.get('last_name', self.last_name)
        self.date_of_birth = date_of_birth
        self.monthly_salary = salary
        self.department_id = id