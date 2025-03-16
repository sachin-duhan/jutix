import pytest
from pathlib import Path
from jutix.utils.config import load_settings, get_settings

def test_load_settings(test_config_file):
    """Test loading settings from config file"""
    settings = load_settings(test_config_file)
    assert settings is not None
    
    # Check if all required sections are present
    assert hasattr(settings, 'enabled_files')
    assert hasattr(settings, 'metrics')
    assert hasattr(settings, 'paths')
    assert hasattr(settings, 'analysis')
    assert hasattr(settings, 'logging')
    assert hasattr(settings, 'report')

def test_settings_values(test_config_file):
    """Test specific settings values"""
    settings = load_settings(test_config_file)
    
    # Check metrics settings
    assert 'responseTime' in settings.metrics
    assert 'latency' in settings.metrics
    
    # Check analysis settings
    assert settings.analysis.batch_size > 0
    assert settings.analysis.max_workers > 0
    assert settings.analysis.timeout > 0
    
    # Check logging settings
    assert settings.logging.level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    assert settings.logging.rotation is not None
    assert settings.logging.retention is not None
    assert isinstance(settings.logging.compression, str)

def test_get_settings(test_config_file):
    """Test get_settings function"""
    # First load settings
    load_settings(test_config_file)
    
    # Then get settings
    settings = get_settings()
    assert settings is not None
    assert hasattr(settings, 'enabled_files')

def test_invalid_config_file():
    """Test loading invalid config file"""
    with pytest.raises(Exception):
        load_settings("nonexistent_file.toml")

def test_settings_immutability(test_config_file):
    """Test settings immutability"""
    settings = load_settings(test_config_file)
    original_batch_size = settings.analysis.batch_size
    
    # Attempt to modify settings
    with pytest.raises(Exception):
        settings.analysis.batch_size = 999
    
    # Verify value hasn't changed
    assert settings.analysis.batch_size == original_batch_size 