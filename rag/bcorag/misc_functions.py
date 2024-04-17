""" Miscellaneous helper functions.
"""

import sys
import json
import logging


def graceful_exit():
    """Gracefully exits the program with a 0 exit code."""
    print("Exiting...")
    logging.info("Exiting with status code 0.")
    logging.info(
        "---------------------------------- RUN END ----------------------------------"
    )
    sys.exit(0)


def load_json(filepath: str) -> dict:
    """Loads a JSON file and returns the deserialized data.

    Parameters
    ----------
    filepath : str
        File path to the JSON file to load.

    Returns
    -------
    dict
        The deserialized JSON data.
    """
    with open(filepath, "r") as f:
        return json.load(f)


def setup_root_logger(log_path: str, name: str = "bcorag") -> logging.Logger:
    """Configures the root logger.

    Parameters
    ----------
    log_path : str
        The filepath to the log handler.
    name : str (default: "bcorag")
        The name of the root logger.

    Returns
    -------
    logging.Logger
        The root logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=log_path, encoding="utf-8", mode="w")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def setup_document_logger(name: str, parent_logger: str = "bcorag") -> logging.Logger:
    """Configures a document specific logger.

    Parameters
    ----------
    name : str
        The name of the document to setup the logger for.
    parent_logger : str (default: "bcorag")
        Name of the parent logger to setup under.

    Returns
    -------
    logging.Logger
        The document logger.
    """
    document_logger_name = f"{parent_logger}.{name}"
    return logging.getLogger(document_logger_name)
