# Jutix - JMeter Log Analysis Tool

Jutix is a powerful tool for analyzing JMeter log files (.jtl) and generating comprehensive performance reports.

## Features

- Load and analyze multiple JTL files
- Generate various performance visualizations:
  - Response time distribution (box plots)
  - Response time density (violin plots)
  - Throughput over time
  - Response time percentiles
- Calculate key performance statistics
- Generate HTML reports with interactive visualizations
- Configurable through JSON configuration file

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd jutix

# Install the package
pip install -e .
```

## Usage

1. Basic usage with default configuration:
```bash
jutix /path/to/jtl/files
```

2. Using a custom configuration file:
```bash
# Create a config.json file with your settings
{
    "enabled_files": ["*.jtl"],
    "exclude_files": [],
    "metrics": ["responseTime", "latency", "errorCount"],
    "percentiles": [50, 90, 95, 99],
    "output_settings": {
        "base_dir": "analysis_output",
        "plots_dir": "plots",
        "logs_dir": "logs",
        "reports_dir": "reports"
    }
}

# Run jutix
jutix /path/to/jtl/files
```

## Output

The tool generates:
- Performance plots in PNG format
- Detailed HTML report with statistics and visualizations
- Analysis logs

## Project Structure

```
jutix/
├── core/
│   ├── analyzer.py       # Main analyzer class
│   ├── data_loader.py    # JTL file loading
│   └── report_generator.py # HTML report generation
├── config/
│   └── config_handler.py # Configuration management
├── utils/
│   └── logger.py        # Logging setup
├── visualization/
│   └── plotter.py       # Plotting functions
└── main.py              # CLI entry point
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 