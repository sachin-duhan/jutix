import pytest
from pathlib import Path
from jutix.utils.logger import setup_logger

def test_logger_initialization(test_output_dir):
    """Test logger initialization"""
    logger = setup_logger("test", test_output_dir)
    assert logger is not None
    
    # Check log file creation
    log_file = test_output_dir / 'analysis.log'
    assert log_file.exists()

def test_logger_levels(test_output_dir):
    """Test different logging levels"""
    logger = setup_logger("test", test_output_dir)
    
    # Test all log levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Check log file contents
    log_file = test_output_dir / 'analysis.log'
    log_content = log_file.read_text()
    
    assert "Debug message" in log_content
    assert "Info message" in log_content
    assert "Warning message" in log_content
    assert "Error message" in log_content

def test_logger_context(test_output_dir):
    """Test logger context binding"""
    logger = setup_logger("test_context", test_output_dir)
    logger.info("Test message")
    
    log_file = test_output_dir / 'analysis.log'
    log_content = log_file.read_text()
    
    assert "test_context" in log_content

def test_logger_directory_creation(test_output_dir):
    """Test logger creates directory if not exists"""
    new_dir = test_output_dir / "nested" / "logs"
    logger = setup_logger("test", new_dir)
    
    assert new_dir.exists()
    assert (new_dir / 'analysis.log').exists()

def test_logger_exception_handling(test_output_dir):
    """Test logger exception handling"""
    logger = setup_logger("test", test_output_dir)
    
    try:
        raise ValueError("Test error")
    except Exception as e:
        logger.exception("Error occurred")
    
    log_file = test_output_dir / 'analysis.log'
    log_content = log_file.read_text()
    
    assert "Error occurred" in log_content
    assert "ValueError: Test error" in log_content
    assert "Traceback" in log_content 