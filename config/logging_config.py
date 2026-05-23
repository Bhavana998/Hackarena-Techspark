import logging
import sys
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log')
        ]
    )
    
    # Set third-party loggers to WARNING
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)