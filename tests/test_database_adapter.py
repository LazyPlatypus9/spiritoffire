"""Unit tests for DatabaseAdapter abstract class"""

import pytest
from unittest.mock import MagicMock

from spiritoffire.adapters import DatabaseAdapter


class TestDatabaseAdapterAbstractClass:
    """Test DatabaseAdapter as an abstract base class"""

    def test_abstract_class_raises_error_on_instantiation(self):
        """Test that DatabaseAdapter cannot be instantiated directly"""
        with pytest.raises(TypeError):
            # Cannot instantiate abstract base class
            DatabaseAdapter[str](MagicMock(), "test_app")

    def test_abstract_methods_are_properly_declared(self):
        """Test that abstract methods are properly decorated"""
        # Verify both abstract methods are defined in the class
        assert "add" in DatabaseAdapter.__dict__
        assert "get_all" in DatabaseAdapter.__dict__
        assert callable(DatabaseAdapter.add)
        assert callable(DatabaseAdapter.get_all)

    def test_is_abstract(self):
        """Test that DatabaseAdapter is an abstract base class"""
        # Verify it's marked as abstract
        assert hasattr(DatabaseAdapter, "__abstractmethods__")
        abstract_methods = DatabaseAdapter.__abstractmethods__
        assert "add" in abstract_methods
        assert "get_all" in abstract_methods

    def test_has_type_parameter(self):
        """Test that DatabaseAdapter accepts type parameters"""
        # Can create generics without instantiation
        AdapterString = DatabaseAdapter[str]
        AdapterInt = DatabaseAdapter[int]
        AdapterDict = DatabaseAdapter[dict]
        assert AdapterString is not None
        assert AdapterInt is not None
        assert AdapterDict is not None


class TestConcreteImplementationPattern:
    """Test the pattern of creating concrete implementations"""

    class StringAdapter(DatabaseAdapter[str]):
        """Example concrete implementation"""

        def __init__(self, mongo_database, app_name: str):
            self.mongo_database = mongo_database
            self.app_name = app_name

        def add(self, item: str) -> str:
            return f"{item}_added"

        def get_all(self):
            yield "item1"
            yield "item2"

    def test_can_create_concrete_implementation(self):
        """Test that concrete implementations can be created"""
        adapter = self.StringAdapter(MagicMock(), "test_app")
        assert adapter is not None
        assert hasattr(adapter, "mongo_database")
        assert hasattr(adapter, "app_name")

    def test_concrete_implementation_add_returns_string(self):
        """Test that add returns string"""
        mock_db = MagicMock()
        adapter = self.StringAdapter(mock_db, "test_app")
        result = adapter.add("test")
        assert result == "test_added"
        assert isinstance(result, str)

    def test_concrete_implementation_get_all_yields(self):
        """Test that get_all yields items"""
        mock_db = MagicMock()
        adapter = self.StringAdapter(mock_db, "test_app")
        results = list(adapter.get_all())
        assert len(results) == 2
        assert results == ["item1", "item2"]


class TestDifferentTypeParameters:
    """Test DatabaseAdapter with various type parameters"""

    class IntAdapter(DatabaseAdapter[int]):
        def __init__(self, mongo_database, app_name: str):
            self.mongo_database = mongo_database
            self.app_name = app_name

        def add(self, item: int) -> str:
            return str(item * 2)

        def get_all(self):
            yield 1
            yield 2
            yield 3

    class FloatAdapter(DatabaseAdapter[float]):
        def __init__(self, mongo_database, app_name: str):
            self.mongo_database = mongo_database
            self.app_name = app_name

        def add(self, item: float) -> str:
            return f"{item * 1.5:.2f}"

        def get_all(self):
            yield 1.5
            yield 2.5

    def test_int_adapter_pattern(self):
        """Test int adapter pattern"""
        mock_db = MagicMock()
        adapter = self.IntAdapter(mock_db, "test")
        result = adapter.add(10)
        assert result == "20"
        result = list(adapter.get_all())
        assert result == [1, 2, 3]

    def test_float_adapter_pattern(self):
        """Test float adapter pattern"""
        mock_db = MagicMock()
        adapter = self.FloatAdapter(mock_db, "test")
        result = adapter.add(2.0)
        assert result == "3.00"
        result = list(adapter.get_all())
        assert result == [1.5, 2.5]


class TestGeneratorBehavior:
    """Test that get_all returns generators properly"""

    class CustomAdapter(DatabaseAdapter[dict]):
        def __init__(self, mongo_database, app_name: str):
            self.mongo_database = mongo_database
            self.app_name = app_name

        def add(self, item: dict) -> str:
            return str(hash(str(item)))

        def get_all(self):
            yield {"id": 1, "name": "Alice"}
            yield {"id": 2, "name": "Bob"}
            yield {"id": 3, "name": "Charlie"}

    def test_get_all_creates_generator(self):
        """Test that get_all returns a generator"""
        mock_db = MagicMock()
        adapter = self.CustomAdapter(mock_db, "test")
        result = adapter.get_all()
        # Can iterate multiple times because it's a generator
        first_pass = list(result)
        assert len(first_pass) == 3
        second_pass = list(result)
        assert len(second_pass) == 0

    def test_generator_yields_correct_types(self):
        """Test that generator yields dictionaries"""
        mock_db = MagicMock()
        adapter = self.CustomAdapter(mock_db, "test")
        results = list(adapter.get_all())
        assert all(isinstance(item, dict) for item in results)
        assert len(results) == 3


class TestMultipleIterators:
    """Test handling of multiple generators"""

    class MultiItemAdapter(DatabaseAdapter[str]):
        def __init__(self, mongo_database, app_name: str):
            self.mongo_database = mongo_database
            self.app_name = app_name

        def add(self, item: str) -> str:
            return item

        def get_all(self):
            yield "first"
            yield "second"
            yield "third"
            yield "fourth"

    def test_many_items_generator(self):
        """Test adapter yielding many items"""
        mock_db = MagicMock()
        adapter = self.MultiItemAdapter(mock_db, "test")
        results = list(adapter.get_all())
        assert len(results) == 4
        assert results == ["first", "second", "third", "fourth"]

    def test_can_process_each_item(self):
        """Test that each item can be processed"""
        mock_db = MagicMock()
        adapter = self.MultiItemAdapter(mock_db, "test")
        results = list(adapter.get_all())
        capitalized = [item.upper() for item in results]
        assert capitalized == ["FIRST", "SECOND", "THIRD", "FOURTH"]


class TestAdapterStoragePattern:
    """Test common pattern of storing database reference"""

    class StoredAdapter(DatabaseAdapter[str]):
        def __init__(self, mongo_database, app_name: str):
            self.mongo_database = mongo_database
            self.collection = mongo_database.get_database(app_name)
            self.app_name = app_name

        def add(self, item: str) -> str:
            return f"{item}:{self.app_name}"

        def get_all(self):
            yield "sample"

    def test_adapter_stores_database_reference(self):
        """Test that adapter can store database reference"""
        mock_db = MagicMock()
        adapter = self.StoredAdapter(mock_db, "my_app")
        assert adapter.collection is not None
        assert adapter.app_name == "my_app"

    def test_adapter_uses_stored_reference(self):
        """Test that adapter uses stored database reference"""
        mock_db = MagicMock()
        adapter = self.StoredAdapter(mock_db, "test_app")
        result = adapter.add("test_item")
        # Verify the app_name was used in the result
        assert "test_app" in result
