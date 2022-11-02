import datetime
import logging
import os

import structlog


def _convert_dates(obj):
    if isinstance(obj, datetime.date):
        # all datetimes are also dates
        return obj.isoformat()
    elif isinstance(obj, dict):
        # Assume dates won't be keys
        return {
            k: _convert_dates(v) for k, v in obj.items() if id(v) != id(obj)
        }
    elif isinstance(obj, list):
        return [_convert_dates(v) for v in obj if id(v) != id(obj)]
    return obj


def __dates_to_str_filter(_, __, event):
    return _convert_dates(event)


def __pretty_print_exception(_, __, event):
    exc = event.pop("exception", None)
    if exc is not None:
        event["exception"] = exc.splitlines()

    exc = event.pop("stack", None)
    if exc is not None:
        event["stack"] = exc.splitlines()

    return event


def __message_instead_of_event(_, __, event):
    exc = event.pop("event", None)
    if exc is not None:
        event["message"] = exc

    return event


def __add_log_level(_, method_name: str, event):
    event["levelname"] = method_name.upper()

    return event


def __common_processors():
    return [
        __dates_to_str_filter,
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        __pretty_print_exception,
    ]


def __json_processors():
    return [
        __add_log_level,
        __message_instead_of_event,
        structlog.processors.CallsiteParameterAdder(
            parameters=[structlog.processors.CallsiteParameter.THREAD]
        ),
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="asctime"),
        structlog.processors.JSONRenderer(sort_keys=True),
    ]


def __console_processors():
    return [
        structlog.dev.set_exc_info,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        structlog.dev.ConsoleRenderer(),
    ]


def __configure_logging():
    common = __common_processors()
    json = __json_processors()
    processors = [*common, *json]
    log_level = os.getenv("LOG_LEVEL", "INFO").lower()
    level = structlog._log_levels._NAME_TO_LEVEL.get(log_level, logging.INFO)
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def __use_console_renderer():
    common = __common_processors()
    console = __console_processors()
    structlog.configure(
        processors=[
            *common,
            *console,
        ]
    )


def get_logger(name: str = "AWS"):
    __configure_logging()

    # Debug flag and default logger level
    is_debug = os.getenv("DEBUG", "").lower() in ["yes", "true", "1"]
    if is_debug and os.getenv("LOG_LEVEL", "INFO").lower() == "debug":
        __use_console_renderer()

    return structlog.get_logger(name)


__all__ = ["get_logger"]
