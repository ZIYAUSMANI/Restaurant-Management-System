import logging
"""
    Create a logger that writes to a specific file.
    
    Args:
        log_file (str): Path to the log file for this module.
        logger_name (str): Name of the logger (optional).
        level (int): Logging level.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
def get_logger(log_file, logger_name=None, level=logging.ERROR):
    
    logger = logging.getLogger(logger_name or log_file)
    
    if not logger.hasHandlers():  
        logger.setLevel(level)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

