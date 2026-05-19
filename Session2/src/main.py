import platform
import sys
import logging
import time
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def system_info():
    start_time = time.time()

    logging.info("Pipeline started")

    logging.info(f"System: {platform.system()}")
    logging.info(f"Node Name: {platform.node()}")
    logging.info(f"Release: {platform.release()}")
    logging.info(f"Machine: {platform.machine()}")
    logging.info(f"Python Version: {sys.version}")

    execution_time = round(time.time() - start_time, 2)

    logging.info(f"Execution time: {execution_time} seconds")
    logging.info("Pipeline finished")


if __name__ == "__main__":
    system_info()