from __future__ import annotations

import inspect
import logging
from logging import Handler, LogRecord
from pathlib import PurePath
from typing import Optional, Union


import loguru
from loguru import logger

LOG = loguru.logger

class InterceptHandler(logging.Handler):
    def emit(self, record: LogRecord) -> None:
        level = getattr(logger.level(record.levelname), 'name', record.levelno)
        
        frame, depth = getattr(inspect.currentframe(),"f_back",None),1
        while frame and frame.f_code.cofilename == logging.__file__:
            frame = frame.f_back
            depth += 1
            
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )

def setup(
    sink : Union[PurePath, str, Handler],
    debug : bool = False,
    colorize : bool = False,
    level: Optional[str] = None,
) -> None:
    if debug:
            default_level = "DEBUG"
            backtrace = True
            diagnose = True
    else:
        default_level = "INFO"
        backtrace = False
        diagnose = True
    if level is None:
        level = default_level

    LOG.remove()
    LOG.add(
        sink,
        level=level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> |"
            " <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> -"
            " <level>{message}</level>"
        ),
        filter=None,
        colorize=colorize,
        backtrace=backtrace,
        diagnose=diagnose,
        serialize=False,
        enqueue=False,
        catch=True,
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


__all__ = ("LOG", "setup")