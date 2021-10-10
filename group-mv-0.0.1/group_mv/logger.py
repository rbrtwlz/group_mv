import os 
import io
import logging
import contextlib

def _create_logger():
    "Creates a logger"
    logger = logging.Logger("group_mv_logger", level=logging.DEBUG)
    handler = logging.FileHandler(os.environ["LOGFILE"], 'a+')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-10s - %(message)s'))
    logger.addHandler(handler)
    return logger


class Logger(object):

    log = None

    @classmethod
    def get_instance(cls):
        if cls.log is None:
            cls.log = _create_logger()
        return cls.log

    @classmethod
    def log_decorator(cls, func):
        "Decorater for logging the outputs, return values and exceptions of `func`"
        def wrapper(*args, **kwargs):
            log = cls.get_instance()
            outp = io.StringIO()
            try:
                with contextlib.redirect_stdout(outp):
                    value = func(*args, **kwargs)
                for msg in outp.getvalue().strip().split("\n"):
                    log.info(f"Output {func.__name__}: {msg}")
                if value is not None:
                    log.info(f"Return {func.__name__}: {value}")
            except Exception as e: 
                log.error(f"Exception {func.__name__}: {type(e).__name__}: {e}", ) #exc_info=True)
                raise
            return value
        return wrapper

     

