import pytest
import pandas as pd
import numpy as np
from jutix.analyzer import JMeterAnalyzer

def test_analyzer_initialization(analyzer):
    """Test analyzer initialization"""
    assert analyzer is not None
    assert hasattr(analyzer, 'settings')
    assert hasattr(analyzer, 'logger')

def test_analyze_data(analyzer, sample_df):
    """Test data analysis"""
    results = analyzer.analyze_data(sample_df)
    
    assert isinstance(results, dict)
    assert 'summary' in results
    assert 'percentiles' in results
    assert 'errors' in results
    
    # Check summary stats
    summary = results['summary']
    assert 'total_requests' in summary
    assert 'success_rate' in summary
    assert 'avg_response_time' in summary
    assert 'throughput' in summary
    
    # Check percentiles
    percentiles = results['percentiles']
    assert '50th' in percentiles
    assert '90th' in percentiles
    assert '95th' in percentiles
    assert '99th' in percentiles

def test_error_analysis(analyzer, sample_df):
    """Test error analysis"""
    # Add some error data
    error_df = sample_df.copy()
    error_df.loc[0, 'success'] = False
    error_df.loc[0, 'responseMessage'] = 'Test Error'
    
    results = analyzer.analyze_data(error_df)
    errors = results['errors']
    
    assert len(errors) > 0
    assert 'Test Error' in str(errors)

def test_throughput_calculation(analyzer, sample_df):
    """Test throughput calculation"""
    results = analyzer.analyze_data(sample_df)
    throughput = results['summary']['throughput']
    
    assert throughput > 0
    assert isinstance(throughput, float)

def test_response_time_metrics(analyzer, sample_df):
    """Test response time metrics calculation"""
    results = analyzer.analyze_data(sample_df)
    
    # Check response time metrics
    assert results['summary']['avg_response_time'] > 0
    assert results['summary']['min_response_time'] > 0
    assert results['summary']['max_response_time'] > 0
    assert results['summary']['std_response_time'] > 0

def test_empty_dataframe(analyzer):
    """Test analysis with empty DataFrame"""
    empty_df = pd.DataFrame()
    results = analyzer.analyze_data(empty_df)
    
    assert results['summary']['total_requests'] == 0
    assert results['summary']['success_rate'] == 0
    assert results['summary']['throughput'] == 0

def test_data_filtering(analyzer, sample_df):
    """Test data filtering by timestamp"""
    # Add timestamps spanning multiple days
    sample_df['timeStamp'] = pd.date_range(start='2024-01-01', periods=len(sample_df), freq='H')
    
    # Filter for specific date
    filtered_results = analyzer.analyze_data(
        sample_df,
        start_time=pd.Timestamp('2024-01-01'),
        end_time=pd.Timestamp('2024-01-02')
    )
    
    assert filtered_results['summary']['total_requests'] <= len(sample_df) 