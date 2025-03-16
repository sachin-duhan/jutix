import pytest
from pathlib import Path
from jutix.core.data_loader import JTLDataLoader
import pandas as pd

def test_data_loader_initialization(test_data_dir, test_logger):
    """Test data loader initialization"""
    loader = JTLDataLoader(test_data_dir, test_logger)
    assert loader.output_dir == test_data_dir
    assert loader.logger == test_logger

def test_load_jtl_files_with_specific_file(test_data_dir, test_logger, sample_jtl_file):
    """Test loading specific JTL file"""
    loader = JTLDataLoader(test_data_dir, test_logger)
    df = loader.load_jtl_files([sample_jtl_file.name])
    
    assert not df.empty
    assert len(df) == 3  # Number of rows in sample file
    assert 'timeStamp' in df.columns
    assert 'elapsed' in df.columns
    assert 'success' in df.columns
    
    # Check data types
    assert df['elapsed'].dtype == 'float64'
    assert df['success'].dtype == 'bool'
    
    # Check success conversion
    assert df['success'].sum() == 2  # Two successful requests in sample
    
    # Check time columns
    assert 'second' in df.columns
    assert 'minute' in df.columns
    assert 'hour' in df.columns

def test_load_jtl_files_with_pattern(test_data_dir, test_logger):
    """Test loading files using pattern"""
    loader = JTLDataLoader(test_data_dir, test_logger)
    df = loader.load_jtl_files(['*.csv'])
    
    assert not df.empty
    assert len(df) > 0
    assert 'timeStamp' in df.columns

def test_load_jtl_files_with_exclude(test_data_dir, test_logger, sample_jtl_file):
    """Test excluding files"""
    loader = JTLDataLoader(test_data_dir, test_logger)
    df = loader.load_jtl_files(['*.csv'], [sample_jtl_file.name])
    
    assert df.empty  # Should be empty as we excluded the only sample file

def test_load_jtl_files_nonexistent(test_data_dir, test_logger):
    """Test loading nonexistent file"""
    loader = JTLDataLoader(test_data_dir, test_logger)
    df = loader.load_jtl_files(['nonexistent.csv'])
    
    assert df.empty

def test_load_jtl_files_data_validation(test_data_dir, test_logger, sample_jtl_file):
    """Test data validation after loading"""
    loader = JTLDataLoader(test_data_dir, test_logger)
    df = loader.load_jtl_files([sample_jtl_file.name])
    
    # Check numeric columns
    assert df['elapsed'].min() >= 0
    assert df['Latency'].min() >= 0
    assert df['Connect'].min() >= 0
    
    # Check response codes
    assert df['responseCode'].isin(['200', '500']).all()
    
    # Check timestamps are properly parsed
    assert pd.api.types.is_datetime64_any_dtype(df['timeStamp'])
    
    # Check success mapping
    assert df[df['responseCode'] == '200']['success'].all()
    assert not df[df['responseCode'] == '500']['success'].any() 