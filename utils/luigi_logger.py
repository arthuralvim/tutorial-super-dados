from colorama import Back
from colorama import Fore
from colorama import Style
from pythonjsonlogger.jsonlogger import JsonFormatter
import logging


class LoggingColorMixin(object):

    def apply_color(self, msg, color, background=Back.BLACK):
        return f'{color}{background}{msg}{Style.RESET_ALL}'

    def format(self, record):
        msg = super().format(record)
        if record.levelno == logging.WARNING:
            msg = self.apply_color(msg, Fore.YELLOW)
        elif record.levelno == logging.ERROR:
            msg = self.apply_color(msg, Fore.RED)
        elif record.levelno == logging.CRITICAL:
            msg = self.apply_color(msg, Fore.RED, Back.YELLOW)
        elif record.levelno == logging.INFO:
            msg = self.apply_color(msg, Fore.GREEN)
        elif record.levelno == logging.DEBUG:
            msg = self.apply_color(msg, Fore.CYAN)
        else:
            msg = self.apply_color(msg, Fore.WHITE)
        return msg


class JsonColorFormatter(LoggingColorMixin, JsonFormatter):
    pass


class LuigiColorFormatter(LoggingColorMixin, logging.Formatter,):
    pass
