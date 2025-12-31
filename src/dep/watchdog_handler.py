import os
import shutil
import uuid
from watchdog.events import FileSystemEventHandler
from dep.logger import get_logger

logger = get_logger(__name__)
class MoverHandler(FileSystemEventHandler):
    def __init__(self, source_dir, foldername_map_path):
        self.source_dir = source_dir
        self.foldername_map_path = foldername_map_path

    def on_modified(self, event):
        with os.scandir(self.source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = None
                if (
                    name.endswith(".jpg")
                    or name.endswith("jpeg")
                    or name.endswith(".png")
                ):
                    dest = self.foldername_map_path["image"]
                elif name.endswith(".exe"):
                    dest = self.foldername_map_path["app"]
                elif name.endswith(".zip") or name.endswith(".rar"):
                    dest = self.foldername_map_path["archiver"]
                elif name.endswith(".pdf"):
                    dest = self.foldername_map_path["pdf"]
                elif name.endswith(".xlsx") or name.endswith(".xls"):
                    dest = self.foldername_map_path["excel"]
                if dest:
                    self.__move_file(dest, entry, name)

    def __move_file(self, dest, entry, name):


        src_path = entry.path
        dest_path = f"{dest}/{name}"
        if os.path.exists(dest_path):
            unique_name = self.__make_unique(name)
            dest_path = f"{dest}/{unique_name}"
        
        logger.info(f"__move_file - src={src_path}, dest={dest_path}")
        
        shutil.move(src_path, dest_path)

        logger.info("__move_file - end")

    def __make_unique(self, origin_name):
        name, ext = os.path.splitext(origin_name)
        unique_id = uuid.uuid4().hex
        return f"{name}_{unique_id[10:]}{ext}"
