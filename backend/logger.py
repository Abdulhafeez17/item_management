import logging

def setup_logger():
    logger = logging.getLogger("item_app")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [user=%(user)s] %(message)s"
    )

    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

  
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)

    # Add both handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()