from unittest.mock import patch, MagicMock
from src.utils import Logger, log, LogLevel, enable_file_logging, set_log_level


def test_logger_init():
    """Test logger initialization."""
    logger = Logger(name="test-logger")
    assert logger.logger.name == "test-logger"


@patch("logging.Logger.addHandler")
@patch("logging.StreamHandler")
def test_logger_configure(mock_stream_handler, mock_add_handler):
    """Test logger configuration."""
    # Setup mock
    mock_handler = MagicMock()
    mock_stream_handler.return_value = mock_handler

    # Create and configure logger
    logger = Logger(name="test-logger")
    logger.configure(LogLevel.DEBUG)

    # Verify handler was added
    mock_add_handler.assert_called_with(mock_handler)
    assert logger.logger.level == LogLevel.DEBUG.value


@patch("logging.FileHandler")
@patch("os.makedirs")
def test_logger_get_file_handler(mock_makedirs, mock_file_handler):
    """Test getting a file handler."""
    # Setup mock
    mock_handler = MagicMock()
    mock_file_handler.return_value = mock_handler

    # Create logger and get file handler
    logger = Logger(name="test-logger")
    handler = logger.get_file_handler("test.log")

    # Verify directories were created and handler was configured
    mock_makedirs.assert_called_with("logs", exist_ok=True)
    mock_file_handler.assert_called_once()
    assert handler == mock_handler


@patch("src.utils.Logger.get_file_handler")
@patch("logging.Logger.addHandler")
def test_logger_enable_file_logging(mock_add_handler, mock_get_file_handler):
    """Test enabling file logging."""
    # Setup mock
    mock_handler = MagicMock()
    mock_get_file_handler.return_value = mock_handler

    # Create logger and enable file logging
    logger = Logger(name="test-logger")
    logger.enable_file_logging("test.log")

    # Verify handler was added
    mock_get_file_handler.assert_called_with("test.log")
    mock_add_handler.assert_called_with(mock_handler)


@patch("src.utils._logger.debug")
@patch("src.utils._logger.info")
@patch("src.utils._logger.warning")
@patch("src.utils._logger.error")
@patch("src.utils._logger.critical")
def test_log_function(mock_critical, mock_error, mock_warning, mock_info, mock_debug):
    """Test the log function with different levels."""
    # Call log with different levels
    log("Debug message", LogLevel.DEBUG)
    log("Info message", LogLevel.INFO)
    log("Warning message", LogLevel.WARNING)
    log("Error message", LogLevel.ERROR)
    log("Critical message", LogLevel.CRITICAL)

    # Verify each level was called
    mock_debug.assert_called_with("Debug message")
    mock_info.assert_called_with("Info message")
    mock_warning.assert_called_with("Warning message")
    mock_error.assert_called_with("Error message")
    mock_critical.assert_called_with("Critical message")


@patch("src.utils._logger.enable_file_logging")
def test_enable_file_logging_function(mock_enable):
    """Test the enable_file_logging function."""
    # Call the function
    enable_file_logging("test.log")

    # Verify the logger's method was called
    mock_enable.assert_called_with("test.log")


@patch("src.utils._logger.configure")
def test_set_log_level_function(mock_configure):
    """Test the set_log_level function."""
    # Call the function
    set_log_level(LogLevel.ERROR)

    # Verify the logger's method was called
    mock_configure.assert_called_with(LogLevel.ERROR)
