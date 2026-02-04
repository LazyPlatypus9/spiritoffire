"""Unit tests for MongoDatabase class."""

from unittest.mock import MagicMock, patch

import pytest

from spiritoffire.core.mongo_database import MongoDatabase


class TestMongoDatabaseInit:
    """Tests for MongoDatabase initialization."""

    def test_init_with_credentials(self):
        """Test initialization with username and password."""
        db = MongoDatabase(
            username="testuser",
            password="testpass",
            host="localhost",
            port="27017",
        )
        assert db.username == "testuser"
        assert db.password == "testpass"
        assert db.host == "localhost"
        assert db.port == "27017"
        assert db.client is None

    def test_init_without_credentials(self):
        """Test initialization without username and password."""
        db = MongoDatabase(
            username="",
            password="",
            host="localhost",
            port="27017",
        )
        assert db.username == ""
        assert db.password == ""
        assert db.client is None

    def test_init_with_only_username(self):
        """Test initialization with only username (treated as insecure)."""
        db = MongoDatabase(
            username="testuser",
            password="",
            host="localhost",
            port="27017",
        )
        assert db.username == "testuser"
        assert db.password == ""
        assert db.client is None

    def test_init_with_only_password(self):
        """Test initialization with only password (treated as insecure)."""
        db = MongoDatabase(
            username="",
            password="testpass",
            host="localhost",
            port="27017",
        )
        assert db.username == ""
        assert db.password == "testpass"
        assert db.client is None


class TestMongoDatabaseSecureConnection:
    """Tests for secure MongoDB connection."""

    def test_secure_connection_format(self):
        """Test secure connection string format with credentials."""
        with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
            mock_client_instance = MagicMock()
            mock_client.return_value = mock_client_instance

            db = MongoDatabase(
                username="testuser",
                password="testpass",
                host="localhost",
                port="27017",
            )

            result = db.get_client()

            expected_uri = "mongodb://testuser:testpass@localhost:27017"
            mock_client.assert_called_once_with(expected_uri)
            # Note: get_client() returns the client but doesn't store it
            # client is only stored when get_database() is called
            assert result == mock_client_instance

    def test_secure_connection_logged(self):
        """Test that secure connection logs info message."""
        with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
            with patch("spiritoffire.core.mongo_database.logger") as mock_logger:
                mock_client.return_value = MagicMock()

                db = MongoDatabase(
                    username="testuser",
                    password="testpass",
                    host="localhost",
                    port="27017",
                )

                db.get_client()

                mock_logger.info.assert_called_once_with(
                    "Using secure connection for Mongo..."
                )
                mock_logger.warning.assert_not_called()

    def test_insecure_connection_logged(self):
        """Test that insecure connection logs warning message."""
        with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
            with patch("spiritoffire.core.mongo_database.logger") as mock_logger:
                mock_client.return_value = MagicMock()

                db = MongoDatabase(
                    username="",
                    password="",
                    host="localhost",
                    port="27017",
                )

                db.get_client()

                mock_logger.info.assert_not_called()
                mock_logger.warning.assert_called_once_with(
                    "Using insecure connection for Mongo!!"
                )


class TestMongoDatabaseConnectionStrings:
    """Tests for various connection string formats."""

    def test_connection_string_with_ip(self):
        """Test connection string with IP address."""
        with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
            mock_client_instance = MagicMock()
            mock_client.return_value = mock_client_instance

            db = MongoDatabase(
                username="admin",
                password="secret",
                host="192.168.1.100",
                port="54321",
            )

            db.get_client()

            expected_uri = "mongodb://admin:secret@192.168.1.100:54321"
            mock_client.assert_called_once_with(expected_uri)

    def test_connection_string_different_port(self):
        """Test connection string with different port."""
        with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
            mock_client_instance = MagicMock()
            mock_client.return_value = mock_client_instance

            db = MongoDatabase(
                username="admin",
                password="secret",
                host="localhost",
                port="80",
            )

            db.get_client()

            expected_uri = "mongodb://admin:secret@localhost:80"
            mock_client.assert_called_once_with(expected_uri)


class TestMongoDatabaseGetDatabase:
    """Tests for get_database method."""

    def test_get_database_creates_client(self):
        """Test that get_database creates client if needed."""
        with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
            mock_client_instance = MagicMock()
            mock_client.return_value = mock_client_instance

            db = MongoDatabase(
                username="testuser",
                password="testpass",
                host="localhost",
                port="27017",
            )

            result = db.get_database("test_db")

            mock_client.assert_called_once()
            assert db.client is not None

    def test_get_database_stores_client(self):
        """Test that get_database stores the client internally."""
        with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
            mock_client_instance = MagicMock()
            mock_client.return_value = mock_client_instance

            db = MongoDatabase(
                username="testuser",
                password="testpass",
                host="localhost",
                port="27017",
            )

            db.get_database("test_db")

            # Should store the client internally
            assert db.client is not None
            assert db.client == mock_client_instance

    def test_get_database_reuses_client(self):
        """Test that client is reused for subsequent calls."""
        with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
            mock_client_instance = MagicMock()
            mock_client.return_value = mock_client_instance

            db = MongoDatabase(
                username="testuser",
                password="testpass",
                host="localhost",
                port="27017",
            )

            # First call
            db.get_database("first_db")
            # Second call
            db.get_database("second_db")

            # Client should only be created once
            assert mock_client.call_count == 1

    def test_get_database_multiple_retrievals(self):
        """Test retrieving multiple databases from same client."""
        with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
            mock_client_instance = MagicMock()
            mock_client.return_value = mock_client_instance

            db = MongoDatabase(
                username="testuser",
                password="testpass",
                host="localhost",
                port="27017",
            )

            db.get_database("db1")
            db.get_database("db2")
            db.get_database("db3")

            # Client should be created once
            assert mock_client.call_count == 1


class TestMongoDatabaseAttributes:
    """Tests for class attributes."""

    def test_client_attribute_exists(self):
        """Test that client attribute exists."""
        db = MongoDatabase(
            username="testuser",
            password="testpass",
            host="localhost",
            port="27017",
        )
        assert hasattr(db, "client")
        assert db.client is None

    def test_attributes_accessible(self):
        """Test that all class attributes are accessible after initialization."""
        db = MongoDatabase(
            username="user",
            password="pass",
            host="host",
            port="port",
        )
        assert db.username == "user"
        assert db.password == "pass"
        assert db.host == "host"
        assert db.port == "port"
        assert isinstance(db.client, type(None))


class TestMongoDatabaseEdgeCases:
    """Tests for edge cases and various combinations."""

    def test_uri_construction_variations(self):
        """Test various username, password, host, and port combinations."""
        test_cases = [
            {
                "name": "standard connection with localhost",
                "username": "admin",
                "password": "password",
                "host": "localhost",
                "port": "27017",
                "expected": "mongodb://admin:password@localhost:27017",
            },
            {
                "name": "connection with IP address",
                "username": "admin",
                "password": "password",
                "host": "192.168.1.100",
                "port": "27017",
                "expected": "mongodb://admin:password@192.168.1.100:27017",
            },
            {
                "name": "custom port",
                "username": "admin",
                "password": "password",
                "host": "localhost",
                "port": "8888",
                "expected": "mongodb://admin:password@localhost:8888",
            },
            {
                "name": "secure connection no password",
                "username": "admin",
                "password": "",
                "host": "localhost",
                "port": "27017",
                "expected": "mongodb://localhost:27017",
                "is_insecure": True,
            },
            {
                "name": "secure connection no username",
                "username": "",
                "password": "password",
                "host": "localhost",
                "port": "27017",
                "expected": "mongodb://localhost:27017",
                "is_insecure": True,
            },
        ]

        for test_case in test_cases:
            with patch("spiritoffire.core.mongo_database.MongoClient") as mock_client:
                with patch("spiritoffire.core.mongo_database.logger") as mock_logger:
                    mock_client.return_value = MagicMock()

                    db = MongoDatabase(
                        username=test_case["username"],
                        password=test_case["password"],
                        host=test_case["host"],
                        port=test_case["port"],
                    )

                    result = db.get_client()

                    mock_client.assert_called_once_with(test_case["expected"])

                    if test_case.get("is_insecure"):
                        mock_logger.warning.assert_called_once_with(
                            "Using insecure connection for Mongo!!"
                        )
                        mock_logger.info.assert_not_called()
                    else:
                        mock_logger.info.assert_called_once_with(
                            "Using secure connection for Mongo..."
                        )
                        mock_logger.warning.assert_not_called()

                    mock_client.reset_mock()
                    mock_logger.reset_mock()
