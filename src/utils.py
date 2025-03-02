import logging
import sys
import os
from enum import Enum
from datetime import datetime


class LogLevel(Enum):
    """Enum for log levels."""

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Logger:
    """Flexible logging utility for the application."""

    def __init__(self, name="github-code-quality", level=LogLevel.INFO):
        self.logger = logging.getLogger(name)
        self.configure(level)

    def configure(self, level=LogLevel.INFO):
        """Configure the logger with handlers and formatting."""
        # Clear existing handlers to avoid duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Set level
        self.logger.setLevel(level.value)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level.value)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(console_handler)

    def get_file_handler(self, log_file="app.log"):
        """Create a file handler for logging to a file."""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)

        # Create file handler
        file_path = os.path.join("logs", log_file)
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(self.logger.level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)

        return file_handler

    def enable_file_logging(self, log_file=None):
        """Enable logging to a file."""
        if log_file is None:
            # Default to a timestamped log file
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            log_file = f"app-{timestamp}.log"

        file_handler = self.get_file_handler(log_file)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)


# Create a singleton instance for easy access
_logger = Logger()


def log(message, level=LogLevel.INFO):
    """Simple logging function that uses the singleton logger."""
    if level == LogLevel.DEBUG:
        _logger.debug(message)
    elif level == LogLevel.INFO:
        _logger.info(message)
    elif level == LogLevel.WARNING:
        _logger.warning(message)
    elif level == LogLevel.ERROR:
        _logger.error(message)
    elif level == LogLevel.CRITICAL:
        _logger.critical(message)


def enable_file_logging(log_file=None):
    """Enable file logging on the singleton logger."""
    _logger.enable_file_logging(log_file)


def set_log_level(level):
    """Set the log level on the singleton logger."""
    _logger.configure(level)
