# coding: utf-8

import logging
import threading

class Logger:
    _lock = threading.Lock()

    def __init__(self, log_file_path="sub.log"):
        self._logger = logging.getLogger("logger")
        self._stream_handler = logging.StreamHandler()
        self._file_handler = logging.FileHandler(filename=log_file_path)

        self._set_level()
        self._set_formatter()

    def _set_level(self):
        self._logger.setLevel(logging.INFO)
        self._stream_handler.setLevel(logging.INFO)
        self._file_handler.setLevel(logging.INFO)


    def _set_formatter(self):
        self._formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        self._file_handler.setFormatter(self._formatter)
        self._stream_handler.setFormatter(self._formatter)

        self._logger.addHandler(self._file_handler)
        self._logger.addHandler(self._stream_handler)


    def debug(self, args):
        with self._lock:
            self._logger.debug(args)

    def info(self, args):
        with self._lock:
            self._logger.info(args)

    def warning(self, args):
        with self._lock:
            self._logger.warning(args)

    def error(self, args):
        with self._lock:
            self._logger.error(args)

    def critical(self, args):
        with self._lock:
            self._logger.critical(args)

logger = Logger()
