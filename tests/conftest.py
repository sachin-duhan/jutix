import pytest
from pathlib import Path
import shutil
import pandas as pd
from jutix.config.settings import settings
from jutix.core.analyzer import JMeterAnalyzer
from jutix.utils.logger import setup_logger

@pytest.fixture(scope="session")
def test_data_dir():
    """Return path to test data directory"""
    return Path(__file__).parent / "fixtures"

@pytest.fixture(scope="session")
def test_output_dir():
    """Return path to test output directory"""
    output_dir = Path(__file__).parent / "output"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    return output_dir

@pytest.fixture(scope="session")
def test_config_file(test_data_dir):
    """Return path to test config file"""
    return test_data_dir / "test_settings.toml"

@pytest.fixture(scope="session")
def sample_jtl_file(test_data_dir):
    """Return path to sample JTL file"""
    return test_data_dir / "sample_jtl.csv"

@pytest.fixture(scope="function")
def sample_df(sample_jtl_file):
    """Return sample DataFrame"""
    return pd.read_csv(sample_jtl_file, parse_dates=['timeStamp'])

@pytest.fixture(scope="function")
def test_logger(test_output_dir):
    """Return test logger"""
    return setup_logger("test", test_output_dir)

@pytest.fixture(scope="function")
def analyzer(test_output_dir, test_config_file):
    """Return configured analyzer instance"""
    # Configure settings with test config
    settings.load_file(test_config_file)
    return JMeterAnalyzer(str(test_output_dir)) 