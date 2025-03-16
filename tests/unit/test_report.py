import pytest
from pathlib import Path
import pandas as pd
from jutix.report import ReportGenerator

def test_report_initialization(test_output_dir, test_logger):
    """Test report generator initialization"""
    report_gen = ReportGenerator(test_output_dir, test_logger)
    assert report_gen is not None
    assert report_gen.output_dir == test_output_dir
    assert report_gen.logger == test_logger

def test_generate_report(test_output_dir, test_logger, sample_df):
    """Test report generation"""
    report_gen = ReportGenerator(test_output_dir, test_logger)
    
    # Create sample analysis results
    analysis_results = {
        'summary': {
            'total_requests': 100,
            'success_rate': 95.0,
            'avg_response_time': 200.0,
            'min_response_time': 100.0,
            'max_response_time': 300.0,
            'std_response_time': 50.0,
            'throughput': 10.0
        },
        'percentiles': {
            '50th': 150.0,
            '90th': 250.0,
            '95th': 275.0,
            '99th': 290.0
        },
        'errors': ['Test Error 1', 'Test Error 2']
    }
    
    # Generate report
    report_file = report_gen.generate_report(
        analysis_results,
        sample_df,
        title="Test Report"
    )
    
    # Check if report file exists
    assert report_file.exists()
    assert report_file.suffix == '.html'

def test_report_content(test_output_dir, test_logger, sample_df):
    """Test report content"""
    report_gen = ReportGenerator(test_output_dir, test_logger)
    
    analysis_results = {
        'summary': {
            'total_requests': 100,
            'success_rate': 95.0,
            'avg_response_time': 200.0,
            'throughput': 10.0
        },
        'percentiles': {
            '50th': 150.0,
            '90th': 250.0
        },
        'errors': ['Test Error']
    }
    
    report_file = report_gen.generate_report(
        analysis_results,
        sample_df,
        title="Test Report"
    )
    
    # Read report content
    content = report_file.read_text()
    
    # Check for key elements
    assert "Test Report" in content
    assert "Total Requests: 100" in content
    assert "Success Rate: 95.0%" in content
    assert "Test Error" in content

def test_report_with_plots(test_output_dir, test_logger, sample_df):
    """Test report generation with plots"""
    report_gen = ReportGenerator(test_output_dir, test_logger)
    
    analysis_results = {
        'summary': {
            'total_requests': 100,
            'success_rate': 95.0,
            'avg_response_time': 200.0,
            'throughput': 10.0
        },
        'percentiles': {
            '50th': 150.0,
            '90th': 250.0
        },
        'errors': []
    }
    
    report_file = report_gen.generate_report(
        analysis_results,
        sample_df,
        title="Test Report",
        include_plots=True
    )
    
    content = report_file.read_text()
    assert "Response Time Distribution" in content
    assert "Throughput Over Time" in content

def test_report_without_plots(test_output_dir, test_logger, sample_df):
    """Test report generation without plots"""
    report_gen = ReportGenerator(test_output_dir, test_logger)
    
    analysis_results = {
        'summary': {
            'total_requests': 100,
            'success_rate': 95.0,
            'avg_response_time': 200.0,
            'throughput': 10.0
        },
        'percentiles': {
            '50th': 150.0,
            '90th': 250.0
        },
        'errors': []
    }
    
    report_file = report_gen.generate_report(
        analysis_results,
        sample_df,
        title="Test Report",
        include_plots=False
    )
    
    content = report_file.read_text()
    assert "Response Time Distribution" not in content
    assert "Throughput Over Time" not in content

def test_empty_data_report(test_output_dir, test_logger):
    """Test report generation with empty data"""
    report_gen = ReportGenerator(test_output_dir, test_logger)
    empty_df = pd.DataFrame()
    
    analysis_results = {
        'summary': {
            'total_requests': 0,
            'success_rate': 0,
            'avg_response_time': 0,
            'throughput': 0
        },
        'percentiles': {},
        'errors': []
    }
    
    report_file = report_gen.generate_report(
        analysis_results,
        empty_df,
        title="Empty Report"
    )
    
    content = report_file.read_text()
    assert "No data available" in content 