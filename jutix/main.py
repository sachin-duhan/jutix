import sys
import argparse
from pathlib import Path
from loguru import logger
from jutix.core.analyzer import JMeterAnalyzer
from jutix.config.settings import settings, ROOT_DIR

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="JMeter JTL Analysis Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-i", "--input-dir",
        help="Directory containing JMeter log files",
        type=str,
        default=str(Path(ROOT_DIR) / settings.paths.input_dir)
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        help="Directory for analysis output",
        type=str,
        default=str(Path(ROOT_DIR) / settings.paths.output_dir)
    )
    
    parser.add_argument(
        "-c", "--config",
        help="Path to custom config file",
        type=str,
        default=None
    )
    
    parser.add_argument(
        "-e", "--env",
        help="Environment to use (development, production)",
        type=str,
        choices=["development", "production", "default"],
        default="default"
    )
    
    return parser.parse_args()

def setup_config(args):
    """Setup configuration based on arguments"""
    try:
        # Set environment
        if args.env != "default":
            settings.configure(FORCE_ENV_FOR_DYNACONF=args.env)
            logger.info(f"Using environment: {args.env}")
        
        # Load custom config if provided
        if args.config:
            config_path = Path(args.config)
            if config_path.exists():
                settings.load_file(config_path)
                logger.info(f"Loaded custom config from {config_path}")
            else:
                logger.warning(f"Config file not found: {config_path}")
        
        # Override paths from command line arguments
        if args.input_dir:
            settings.set("paths.input_dir", args.input_dir)
        if args.output_dir:
            settings.set("paths.output_dir", args.output_dir)
            
        # Log current configuration
        logger.debug("Current configuration:")
        logger.debug(f"Input directory: {settings.paths.input_dir}")
        logger.debug(f"Output directory: {settings.paths.output_dir}")
        logger.debug(f"Log level: {settings.log_settings.level}")
        logger.debug(f"Batch size: {settings.analysis.batch_size}")
        
    except Exception as e:
        logger.exception(f"Error setting up configuration: {e}")
        raise

def main():
    try:
        # Parse command line arguments
        args = parse_args()
        
        # Setup configuration
        setup_config(args)
        
        # Initialize and run analyzer
        analyzer = JMeterAnalyzer(settings.paths.output_dir)
        result = analyzer.generate_report()
        
        if result:
            logger.success(f"Report generated successfully. Open {result} to view the results.")
            sys.exit(0)
        else:
            logger.error("No data found in JTL files.")
            sys.exit(1)
            
    except Exception as e:
        logger.exception(f"Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 