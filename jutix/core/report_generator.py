import pandas as pd
from pathlib import Path
import logging

class ReportGenerator:
    def __init__(self, reports_dir: Path, logger: logging.Logger):
        self.reports_dir = reports_dir
        self.logger = logger

    def get_report_path(self, filename: str) -> str:
        """Get full path for report files"""
        return str(self.reports_dir / filename)

    def calculate_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate performance statistics by file"""
        stats_by_file = df.groupby('file').agg({
            'elapsed': ['count', 'mean', 'std', 'min', 'max'],
            'success': 'mean'
        }).round(2)
        
        stats_by_file.columns = ['Total Requests', 'Mean RT', 'Std RT', 'Min RT', 'Max RT', 'Success Rate']
        stats_by_file['Success Rate'] = (stats_by_file['Success Rate'] * 100).round(2)
        return stats_by_file

    def generate_html_report(self, stats_df: pd.DataFrame) -> str:
        """Generate HTML report with statistics and plots"""
        self.logger.info("Generating HTML report...")
        
        report = f"""
        <html>
        <head>
            <title>JMeter Performance Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                .stats {{ margin: 20px 0; }}
                .plots {{ display: flex; flex-direction: column; gap: 20px; }}
                .plot {{ margin: 10px 0; background-color: white; padding: 15px; border-radius: 8px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; }}
                h1, h2 {{ color: #333; }}
                img {{ max-width: 100%; height: auto; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>JMeter Performance Analysis Report</h1>
                <div class="stats">
                    <h2>Performance Statistics by Test File</h2>
                    {stats_df.to_html()}
                </div>
                
                <div class="plots">
                    <div class="plot">
                        <h2>Response Time Distribution (Box Plot)</h2>
                        <img src="../plots/response_time_boxplot.png" />
                    </div>
                    <div class="plot">
                        <h2>Response Time Density Distribution</h2>
                        <img src="../plots/response_time_violin.png" />
                    </div>
                    <div class="plot">
                        <h2>Throughput Over Time</h2>
                        <img src="../plots/throughput_over_time.png" />
                    </div>
                    <div class="plot">
                        <h2>Response Time Percentiles</h2>
                        <img src="../plots/response_time_percentiles.png" />
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        report_path = self.get_report_path('performance_report.html')
        with open(report_path, 'w') as f:
            f.write(report)
        
        self.logger.info(f"Report generated successfully. Open {report_path} to view the results.")
        return report_path 