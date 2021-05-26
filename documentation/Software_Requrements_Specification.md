# Department application
## Vision
“Department application” is an application which allows users to record information about departments and employees of the company.
The application should provide:
+ Storing records about existing departments and employees;
+ Display the list of all departments and the average salary in each department;
+ Display the list of all employees with the links to their departments;
+ Display the list of employees working in a certain department;
+ Display the given department;
+ Display the given employee;
+ Updating an employee record (adding, removing);
+ Updating a department record (adding, removing);
+ Filter employees by birth date;
+ Provide API for CRUD operations with employees and departments.

## 1.Departments
### 1.1 Display the list of departments
The mode is designed to view the list of departments.
![departments](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/departments_list.png)

Main scenario:
+ User selects item “Departments”;
+ Application displays the list of departments.

The list displays the following columns:
+ Name (link to the department display page)
+ Average salary
+ Number of employees

### 1.2 Display deprtment
The mode is designed to view a certain department.
![department](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/department.png)

Main scenario:
+ User clicks the link on a certain department in the departments list view mode;
+ Application dispalys page with an information on a certain department.

The page displays the following information:
+ Name
+ Average salary
+ Number of employees
+ List of the employees working in this department with their name (link on the employee display page), date of bith and salary

### 1.3 Add department
![add department](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/add_department.png)

Main scenario:
+ User clicks the “Add department” button in the departments list view mode;
+ Application displays form to enter department data;
+ User enters department data and presses “Submit” button;
+ If any data is entered incorrectly, incorrect data message is displayed;
+ If entered data is valid, then the record is added to database;
+ If an error occurs, then error message is displayed;
+ If new department record is successfully added, then the new department page is displayed.

Cancel operation scenario:
+ User clicks the “Add department” button in the departments list view mode;
+ Application displays form to enter department data;
+ User enters department data and presses “Cancel” button;
+ Data don’t save in data base, then list of departments is displayed to the user.
+ If the user selects the menu item "Departments”, ”Employees” or "Search", the data will not be saved to the database and the corresponding form will be opened.

When adding a department, the following details are entered:
+ Name

### 1.4 Edit department
![edit department](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/edit_department.png)

Main scenario:
+ User clicks the “Edit department” button in the department display mode;
+ Application displays the form to enter department data prefilled with actual data;
+ User edits department data and presses “Submit” button;
+ If any data is entered incorrectly, incorrect data messages are displayed;
+ If entered data is valid, then edited data is added to database;
+ If an error occurs, then error message is displayed;
+ If order record is successfully edited, then the department display page is displayed.

Cancel operation scenario:
+ User clicks the “Edit department” button in the department view mode;
+ Application displays the form to enter department data prefilled with actual data;
+ User edits some data and presses “Cancel” button;
+ Data don’t save in data base, then the department display page is displayed.
+ If the user selects the menu item "Departments”, ”Employees” or "Search", the data will not be saved to the database and the corresponding form will be opened.

When editing a department, the following details are entered:
+ Name

### 1.5 Remove department
![remove department](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/remove_department.png)

Main scenario:
+ User clicks the “Delete department” button in the department display mode;
+ A confirmation page is displayed;
+ The user confirms the removal of the order;
+ Record is deleted from database;
+ If an error occurs, then the error message is displayed;
+ If department record is successfully deleted, then list of departments without deleted record and with confirmation message is displayed.

Cancel operation scenario:
+ User clicks the “Delete department” button in the department display mode;
+ A confirmation page is displayed;
+ User press “No” button;
+ The department display page is displayed;
+ If the user selects the menu item "Departments”, ”Employees” or "Search", the data will not be saved to the database and the corresponding form will be opened.

## 2 Employees
### 2.1 Display the list of employees
The mode is designed to view the list of departments.
![employees](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/employees_list.png)

Main scenario:
+ User selects an item “Employees”;
+ Application displays the list of employees.

The list displays the following columns:
+ Name (link to the employee display page)
+ Date of birth
+ Salary
+ Department (link to the department display page)

### 1.2 Display employee
The mode is designed to view a certain employee.
![employee](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/employee.png)

Main scenario:
+ User clicks the link on a certain employee in the employees list view mode;
+ Application dispalys page with an information on a certain employee.

The page displays the following information:
+ Name
+ Date of birth
+ Salary
+ Department (link to the department display page)

### 1.3 Add employee
![add employee](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/add_employee.png)

Main scenario:
+ User clicks the “Add new employee record” button in the employees list view mode;
+ Application displays form to enter employee data;
+ User enters employee data and presses “Submit” button;
+ If any data is entered incorrectly, incorrect data message is displayed;
+ If entered data is valid, then the record is added to database;
+ If an error occurs, then error message is displayed;
+ If new department record is successfully added, then the new employee page is displayed.

Cancel operation scenario:
+ User clicks the “Add new employee record” button in the employees list view mode;
+ Application displays form to enter employee data;
+ User enters some employee data and presses “Cancel” button;
+ Data don’t save in data base, then list of employees is displayed to the user;
+ If the user selects the menu item "Departments”, ”Employees” or "Search", the data will not be saved to the database and the corresponding form will be opened.

When adding an employee, the following details are entered:
+ First name
+ Last name
+ Date of birth
+ Salary
+ Department

### 1.4 Edit employee
![edit employee](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/edit_employee.png)

Main scenario:
+ User clicks the “Edit employee record” button in the employee view mode;
+ Application displays the form to enter employee data prefilled with actual data;
+ User edits employee data and presses “Submit” button;
+ If any data is entered incorrectly, incorrect data messages are displayed;
+ If entered data is valid, then edited data is added to database;
+ If an error occurs, then error message is displayed;
+ If order record is successfully edited, then the employee display page is displayed.

Cancel operation scenario:
+ User clicks the “Edit employee record” button in the employee view mode;
+ Application displays the form to enter employee data prefilled with actual data;
+ User edits some data and presses “Cancel” button;
+ Data don’t save in data base, then the employee display page is displayed.
+ If the user selects the menu item "Departments”, ”Employees” or "Search", the data will not be saved to the database and the corresponding form will be opened.

When editing an employee, the following details are entered:
+ First name
+ Last name
+ Date of birth
+ Salary
+ Department

### 1.5 Remove employee
![remove employee](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/remove_employee.png)

Main scenario:
+ User clicks the “Delete employee record” button in the employee display mode;
+ A confirmation page is displayed;
+ The user confirms the removal of the employee;
+ Record is deleted from database;
+ If an error occurs, then the error message is displayed;
+ If employee record is successfully deleted, then the list of employees without deleted record and with confirmation message is displayed.

Cancel operation scenario:
+ User clicks the “Delete employee record” button in the employee display mode;
+ A confirmation page is displayed;
+ User press “No” button;
+ The employee display page is displayed;
+ If the user selects the menu item "Departments”, ”Employees” or "Search", the data will not be saved to the database and the corresponding form will be opened.

## 3 Search
### 3.1 Search employees by birth date
The mode is designed to search employees by birth date.
![search](https://raw.githubusercontent.com/Neanra/EPAM-project-my-company/master/documentation/pictures/search.png)

Main scenario:
+ User selects an item “Search”;
+ Application displays the form to enter two dates that define the time frame;
+ User enters to and from dates and presses “Submit” button;
+ Application displays the list of employees born between the two dates;
+ If the user selects the menu item "Departments”, ”Employees” or "Search", the data will not be saved to the database and the corresponding form will be opened.

The list displays the following columns:
+ Name (link to the employee display page)
+ Date of birth
+ Salary
+ Department (link to the department display page)
