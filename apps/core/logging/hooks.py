import sys
import logging
import asyncio

def setup_exception_hooks():
    logger = logging.getLogger('root')

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

    # For asyncio
    def handle_asyncio_exception(loop, context):
        msg = context.get("exception", context["message"])
        logger.critical(f"Caught asyncio exception: {msg}", exc_info=context.get("exception"))

    return handle_asyncio_exception
