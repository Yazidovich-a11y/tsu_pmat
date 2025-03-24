import csv
import math
import os
from abc import ABC, abstractmethod


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):

    def __init__(self):
        self.tables = {}

    def add_table(self, name, table):
        if name in self.tables:
            raise ValueError(f"Table '{name}' is already registered.")
        self.tables[name] = table

    def fetch_table(self, name):
        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist.")
        return self.tables[name]

    def insert_into(self, name, record):
        self.fetch_table(name).insert(record)

    def query(self, name, field=None, value=None, min_id=0, max_id=math.inf):
        table_data = self.fetch_table(name).data if isinstance(name, str) else name

        filtered_data = [
            row
            for row in table_data
            if min_id <= int(row.get("id", math.inf)) <= max_id
        ]

        return [
            row for row in filtered_data if value is None or row.get(field) == value
        ]

    def join_tables(self, left, right, key):
        left_data = self.fetch_table(left).data if isinstance(left, str) else left
        right_data = self.fetch_table(right).data if isinstance(right, str) else right

        result = []
        right_map = {row["id"]: row for row in right_data}

        for row in left_data:
            if row[key] in right_map:
                merged = row.copy()
                merged.update(right_map[row[key]])
                merged[key] = merged.pop("id")
                result.append(merged)

        return result

    def aggregate(self, operation, field, table):
        if not table:
            raise ValueError("Table is empty.")

        if not all(field in row for row in table):
            raise ValueError(f"Field '{field}' not found.")

        values = [row[field] for row in table]

        if operation == "avg":
            try:
                numeric_values = list(map(float, values))
            except ValueError:
                raise ValueError("Cannot calculate average for non-numeric values.")
            return f"Average {field}: {sum(numeric_values) / len(numeric_values)}"

        elif operation == "min":
            return f"Minimum {field}: {min(values)}"
        elif operation == "max":
            return f"Maximum {field}: {max(values)}"
        elif operation == "count":
            return f"Count {field}: {len(values)}"

        raise ValueError(f"Unknown aggregation method '{operation}'")


class AbstractTable(ABC):  # pragma: no cover

    @abstractmethod
    def insert(self, record):
        pass

    @abstractmethod
    def load(self):
        pass


class CSVTable(AbstractTable):

    FIELDS = ()
    FILE_NAME = ""

    def __init__(self):
        self.data = []
        self._keys = set()
        self.load()

    def insert(self, record):
        entry = dict(zip(self.FIELDS, record.split()))
        entry_key = self.get_key(entry)

        if entry_key in self._keys:
            raise ValueError(f"Duplicate entry found: {entry_key}")

        self.data.append(entry)
        self._keys.add(entry_key)
        self.save()

    def save(self):
        with open(self.FILE_NAME, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if not os.path.exists(self.FILE_NAME):
            return

        with open(self.FILE_NAME, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entry_key = self.get_key(row)
                if entry_key in self._keys:
                    print(f"Warning: Skipping duplicate entry {entry_key}")
                else:
                    self.data.append(row)
                    self._keys.add(entry_key)


class EmployeeTable(CSVTable):

    FIELDS = ("id", "name", "age", "salary", "department_id")
    FILE_NAME = "employees.csv"

    def get_key(self, entry):
        return int(entry["id"]), int(entry["department_id"])


class DepartmentTable(CSVTable):

    FIELDS = ("id", "department_name")
    FILE_NAME = "departments.csv"

    def get_key(self, entry):
        return int(entry["id"])


class OrdersTable(CSVTable):

    FIELDS = ("id", "total_amount", "customer_id")
    FILE_NAME = "orders.csv"

    def get_key(self, entry):
        return int(entry["id"])
