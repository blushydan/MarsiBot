import logging

from util.config import LogPath


class CustomFormatter(logging.Formatter):
    """Customizable logging formatter. Can be used in `bot.run()`"""

    white = "\x1b[37m"
    grey = "\x1b[38;5;224m"
    green = "\x1b[32m"
    blurple = "\x1b[38;5;68m"
    cyan = "\x1b[36m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    purple = "\x1b[35m"
    desaturated_purple = "\x1b[38;5;96m"
    bold_red = "\x1b[1;31m"
    reset = "\x1b[0m"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    # Debug string added milliseconds
    debug_format_str = "{time_color}%(asctime)s.%(msecs)03d{r} {module_color}%(module)s{r} {name_color}%(name)s:{r} {level_color}%(levelname)s{r} {message_color}%(message)s{r}"
    # Error string added line number and function name
    error_format_str = "{time_color}%(asctime)s{r} {module_color}%(module)s{r} {name_color}%(name)s:{r} {level_color}%(levelname)s{r} {message_color}in{r} {name_color}%(funcName)s{r} {message_color}on line{r} {name_color}%(lineno)d{r}. {message_color}%(message)s{r}"
    default_format_str = "{time_color}%(asctime)s{r} {module_color}%(module)s{r} {name_color}%(name)s:{r} {level_color}%(levelname)s{r} {message_color}%(message)s{r}"

    FORMATS = {
        logging.DEBUG: debug_format_str.format(
            time_color=green,
            module_color=purple,
            name_color=grey,
            level_color=green,
            message_color=green,
            r=reset
        ),
        logging.INFO: default_format_str.format(
            time_color=green,
            module_color=purple,
            name_color=grey,
            level_color=cyan,
            message_color=white,
            r=reset
        ),
        logging.WARNING: default_format_str.format(
            time_color=green,
            module_color=purple,
            name_color=grey,
            level_color=yellow,
            message_color=yellow,
            r=reset
        ),
        logging.ERROR: error_format_str.format(
            time_color=green,
            module_color=purple,
            name_color=grey,
            level_color=red,
            message_color=red,
            r=reset
        ),
        logging.CRITICAL: default_format_str.format(
            time_color=green,
            module_color=purple,
            name_color=grey,
            level_color=bold_red,
            message_color=bold_red,
            r=reset
        ),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.date_fmt)
        return formatter.format(record)


class Logger(logging.Logger):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self, name, level=logging.DEBUG, file_path=LogPath.main):
        super().__init__(name, level)
        self.setLevel(level)
        self.formatter = CustomFormatter()
        self.file_handler = logging.FileHandler(file_path)
        self.file_handler.setFormatter(self.formatter)
        self.addHandler(self.file_handler)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.addHandler(self.stream_handler)
