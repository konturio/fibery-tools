import logging
import structlog

logging.basicConfig(format="%(message)s", level=logging.INFO)

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(),
)


def get_logger(name: str | None = None) -> structlog.BoundLogger:
    """Return a structlog logger bound to *name*."""
    if name:
        return structlog.get_logger(name)
    return structlog.get_logger()
