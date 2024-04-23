""" Miscellaneous helper functions.
"""

import sys
import json
import logging
import os


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


def write_json(output_path: str, data: dict | list) -> bool:
    """Writes JSON out to the output path. Will create the file if it doesn't exist.

    Parameters
    ----------
    output_path : str
        The output file path.
    data : dict or list
        The data to dump.

    Returns
    -------
    bool
        Whether the process was successful.
    """
    try:
        with open(output_path, "w") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        logging.error(f"Failed to dump JSON to output path '{output_path}'.\n{e}")
        return False


def check_dir(path: str):
    """Checks whether a directory creates and if it doesn't, create it. Note, this
    really only works for checking/creating the last level direcotry. Will fail if
    there are issues in the parent level directories in the path.

    Parameters
    ----------
    path : str
        Directory filepath to check.
    """
    if not os.path.isdir(path):
        os.mkdir(path)


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
