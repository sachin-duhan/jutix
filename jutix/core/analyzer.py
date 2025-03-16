from pathlib import Path
from datetime import datetime
from typing import Optional

from jutix.config.config_handler import ConfigHandler
from jutix.utils.logger import setup_logger
from jutix.core.data_loader import JTLDataLoader
from jutix.visualization.plotter import JMeterPlotter
from jutix.core.report_generator import ReportGenerator
from jutix.config.settings import settings

class JMeterAnalyzer:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.config_handler = ConfigHandler()
        
        # Create temporary logger for initialization
        self.logger = setup_logger(str(id(self)), Path("logs"))  # Temporary logs directory
        
        try:
            # Setup directories
            self.setup_directories()
            
            # Recreate logger with proper log directory
            self.logger = setup_logger(str(id(self)), self.logs_dir)
            
            # Initialize components with input directory from settings
            self.data_loader = JTLDataLoader(settings.paths.input_dir, self.logger)
            self.plotter = JMeterPlotter(self.plots_dir, self.logger)
            self.report_generator = ReportGenerator(self.reports_dir, self.logger)
            
            self.logger.info(f"Initialized JMeterAnalyzer with output directory: {output_dir}")
            self.logger.info(f"Using input directory: {settings.paths.input_dir}")
            
        except Exception as e:
            self.logger.exception(f"Error during initialization: {e}")
            raise

    def setup_directories(self):
        """Setup output directories based on config"""
        output_settings = self.config_handler.get_output_settings()
        
        # Create timestamp for unique run folder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.run_dir = Path(output_settings['base_dir']) / timestamp
        
        # Create all necessary directories
        self.plots_dir = self.run_dir / output_settings['plots_dir']
        self.logs_dir = self.run_dir / output_settings['logs_dir']
        self.reports_dir = self.run_dir / output_settings['reports_dir']
        
        # Create directories
        for dir_path in [self.run_dir, self.plots_dir, self.logs_dir, self.reports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Created directory: {dir_path}")

    def generate_report(self) -> Optional[str]:
        """Generate comprehensive analysis report"""
        try:
            config = self.config_handler.config
            # Load data
            df = self.data_loader.load_jtl_files(
                config['enabled_files'],
                config.get('exclude_files', [])
            )
            
            if df.empty:
                self.logger.error("No data found in JTL files")
                return None

            # Generate plots
            self.plotter.generate_all_plots(df)
            
            # Calculate statistics and generate report
            stats_df = self.report_generator.calculate_statistics(df)
            report_path = self.report_generator.generate_html_report(stats_df)
            
            return report_path
            
        except Exception as e:
            self.logger.exception(f"Error during analysis: {e}")
            raise 