import os
import tempfile

import pytest
from database.database import Database, DepartmentTable, EmployeeTable, OrdersTable


@pytest.fixture
def temp_employee_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(b"id,name,age,salary,department_id\n")
        temp_file.write(b"1,John,30,50000,21\n")
        temp_file.write(b"2,Susan,25,42000,22\n")
        temp_file.close()
        yield temp_file.name
    os.remove(temp_file.name)


@pytest.fixture
def temp_department_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(b"id,department_name\n")
        temp_file.write(b"21,Engineering\n")
        temp_file.write(b"22,Marketing\n")
        temp_file.close()
        yield temp_file.name
    os.remove(temp_file.name)


@pytest.fixture
def temp_orders_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(b"id,total_amount,customer_id\n")
        temp_file.write(b"1,300,1\n")
        temp_file.write(b"2,150,2\n")
        temp_file.close()
        yield temp_file.name
    os.remove(temp_file.name)


@pytest.fixture
def database(temp_employee_file, temp_department_file, temp_orders_file):
    db = Database()
    db.tables.clear()
    emp_table = EmployeeTable()
    emp_table.FILE_NAME = temp_employee_file
    emp_table.load()
    dept_table = DepartmentTable()
    dept_table.FILE_NAME = temp_department_file
    dept_table.load()
    orders_table = OrdersTable()
    orders_table.FILE_NAME = temp_orders_file
    orders_table.load()
    db.add_table("employees", emp_table)
    db.add_table("departments", dept_table)
    db.add_table("orders", orders_table)

    return db


def test_insert_and_select(database):
    db = database
    db.insert_into("employees", "3 Michael 40 60000 23")
    db.insert_into("departments", "23 HR")
    db.insert_into("orders", "3 200 3")
    records = db.query("employees", field="id", min_id=2)
    assert len(records) == 2
    names = {record["name"] for record in records}
    assert "Michael" in names


def test_join(database):
    db = database
    joined = db.join_tables("employees", "departments", "department_id")
    assert len(joined) == 2
    dept_names = {record["department_name"] for record in joined}
    assert dept_names == {"Engineering", "Marketing"}


def test_aggregate(database):
    db = database
    avg_salary = db.aggregate("avg", "salary", db.query("employees"))
    max_salary = db.aggregate("max", "salary", db.query("employees"))
    min_salary = db.aggregate("min", "salary", db.query("employees"))
    assert avg_salary == "Average salary: 46000.0"
    assert max_salary == "Maximum salary: 50000"
    assert min_salary == "Minimum salary: 42000"


def test_duplicate_insert(database):
    db = database
    with pytest.raises(ValueError, match="Duplicate entry found"):
        db.insert_into("employees", "1 John 30 50000 21")


def test_invalid_aggregation(database):
    db = database
    with pytest.raises(ValueError, match="Unknown aggregation method 'sum'"):
        db.aggregate("sum", "salary", db.query("employees"))
    with pytest.raises(ValueError, match="Table is empty."):
        db.aggregate("avg", "salary", [])
    with pytest.raises(ValueError, match="Field 'nonexistent' not found."):
        db.aggregate("avg", "nonexistent", db.query("employees"))
    db.insert_into("employees", "4 13 John fortyfive 50000")
    with pytest.raises(
        ValueError, match="Cannot calculate average for non-numeric values."
    ):
        db.aggregate("avg", "age", db.query("employees"))


def test_aggregate_count(database):
    db = database
    count_result = db.aggregate("count", "id", db.query("employees"))
    assert count_result == "Count id: 2"


def test_errors(database):
    db = database
    with pytest.raises(ValueError, match="Table 'employees' is already registered."):
        db.add_table("employees", EmployeeTable())
    with pytest.raises(ValueError, match="Table 'unknown_table' does not exist."):
        db.insert_into("unknown_table", "asdasd")
    with pytest.raises(ValueError, match="Table 'unknown_table' does not exist."):
        db.query("unknown_table", field="id", value=123)


def test_load_with_duplicates():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(b"id,name,age,salary,department_id\n")
        temp_file.write(b"1,John,30,40000,2\n")
        temp_file.write(b"2,Jane,28,38000,3\n")
        temp_file.write(b"1,John,30,40000,2\n")
        temp_file.close()

    try:
        emp_table = EmployeeTable()
        emp_table.FILE_NAME = temp_file.name
        emp_table.load()

        assert len(emp_table.data) == 2
        assert any(emp["name"] == "John" for emp in emp_table.data)
        assert any(emp["name"] == "Jane" for emp in emp_table.data)

    finally:
        os.remove(temp_file.name)
