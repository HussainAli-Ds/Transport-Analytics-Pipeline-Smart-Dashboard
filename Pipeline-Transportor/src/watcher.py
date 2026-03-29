import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from extract import read_excel
from transform import clean_data
from load import insert_data
from config import INPUT_DIR, PROCESSED_DIR, FAILED_DIR
from utils import setup_logger

logger = setup_logger()


class FileHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".xlsx"):
            process_file(event.src_path)


def process_file(file_path):
    try:
        logger.info(f"Processing started: {file_path}")

        time.sleep(2)

        df = read_excel(file_path)
        clean_df = clean_data(df)

        if not clean_df.empty:
            insert_data(clean_df)
            logger.info(f"Inserted rows: {len(clean_df)}")

        shutil.move(
            file_path,
            os.path.join(PROCESSED_DIR, os.path.basename(file_path))
        )

        logger.info(f"SUCCESS: {file_path}")

    except Exception as e:
        logger.error(f"FAILED: {file_path} | Error: {e}")

        shutil.move(
            file_path,
            os.path.join(FAILED_DIR, os.path.basename(file_path))
        )


def start_watching():
    observer = Observer()
    handler = FileHandler()

    observer.schedule(handler, INPUT_DIR, recursive=False)
    observer.start()

    logger.info("Watching for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()