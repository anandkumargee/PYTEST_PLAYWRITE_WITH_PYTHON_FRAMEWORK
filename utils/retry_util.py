import time
import logging

def retry_operation(operation, max_retries=3, delay=1):
    logger = logging.getLogger("RetryUtil")
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Operation failed after {max_retries} attempts: {e}")
                raise
            logger.warning(f"Operation failed on attempt {attempt + 1}. Retrying in {delay} seconds...")
            time.sleep(delay)
