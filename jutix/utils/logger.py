from pathlib import Path
from loguru import logger
from jutix.config.settings import settings

def setup_logger(name: str, log_dir: Path) -> logger:
    """Setup logging configuration using loguru"""
    # Create log directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove default handler
    logger.remove()
    
    # Add file handler
    log_file = log_dir / 'analysis.log'
    logger.add(
        log_file,
        rotation=settings.log_settings.rotation,
        retention=settings.log_settings.retention,
        compression=settings.log_settings.compression,
        level=settings.log_settings.level,
        format=settings.log_settings.format,
        enqueue=True
    )
    
    # Add console handler
    logger.add(
        lambda msg: print(msg, end=""),
        level=settings.log_settings.level,
        format=settings.log_settings.format,
        colorize=True
    )
    
    # Create a contextualized logger
    contextualized_logger = logger.bind(context=name)
    
    # Log logger setup
    contextualized_logger.debug(f"Logger initialized for context: {name}")
    contextualized_logger.debug(f"Log directory: {log_dir}")
    contextualized_logger.debug(f"Log level: {settings.log_settings.level}")
    
    return contextualized_logger 