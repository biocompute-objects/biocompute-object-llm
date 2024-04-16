""" Simple CLI interface for choosing one of the pre-selected baseline testing paper. 
Will automatically grab any PDF file in the ../../papers/ directory. 
"""

import glob
import os
import json
from pick import pick
from bcorag import misc_functions as misc_fns
from typing import Tuple, Any

EXIT_OPTION = "Exit"

def initialize_picker(filetype: str = "pdf") -> dict | None:
    """Kicks off the initial pipeline step where the user picks their
    PDF file to index and chooser the data loader from a pre-set list.

    Parameters
    ----------
    filetype : str (default: pdf)
        The filetype to filter on, this project was build to handle PDF
        files so it is highly unlikely you will want to override this default.

    Returns
    -------
    dicdict or None
        Returns this dictionary:
        {
            "filename": <value>,
            "filepath": <value>,
            "loader": <value>,
            "embedding_model: <value>,
            "vector_store": <value>,
            "llm": <value>
        }
        or None if the user selects to exit at any point in the process.
    """

    return_data: dict[str, Any] = {
        "filename": None,
        "filepath": None,
        "loader": None,
        "embedding_model": None,
        "vector_store": None,
        "llm": None,
    }

    with open("./bcorag/conf.json", "r") as f:
        presets = json.load(f)

    target_file_information = _file_picker(presets["paper_directory"], filetype)
    if target_file_information is None:
        return None
    return_data["filename"] = target_file_information[0]
    return_data["filepath"] = target_file_information[1]

    return return_data


def _file_picker(path: str, filetype: str = "pdf") -> Tuple[str, str] | None:
    """Create the CLI menu to pick the PDF file from the papers directory.

    Parameters
    ----------
    path : str
        The path to the directory to display the CLI menu for.
    filetype : str (default: pdf)
        The filetype to filter on, this project was build to handle PDF
        files so it is highly unlikely you will want to override this default.

    Returns
    -------
    (str, str) or None
        Returns the name of the selected file or None if the user selects exit.
    """
    target_files = glob.glob(f"{path}*.{filetype}")
    pick_options = [os.path.basename(filename) for filename in target_files]
    pick_options.append(EXIT_OPTION)
    pick_title = "Please choose the PDF file to index: "
    option, _ = pick(pick_options, pick_title, indicator="->")
    option = str(option)
    if option == EXIT_OPTION: 
        return None
    return str(option), f"{path}{option}"

def _create_picker(
    title_keyword: str, option_list: list[str], default: str | None = None
) -> str | None:
    """Creates a general picker CLI based on a list of options and the
    functionality to optionally mark one option as the default.

    Parameters
    ----------
    title_keyword : str
        The keyword to use for the picker title.
    option_list : list[str]
        The list of options to display in the picker menu.
    default : str or None (default: None)
        The option to mark one option as the default.

    Returns
    -------
    str or None
        The chosen option of None if the user selected to exit.
    """
    pick_title = f"Please choose your selected {title_keyword}"
    pick_options = [
        f"{option} (default)" if option == default else option for option in option_list
    ]
    option, _ = pick(pick_options, pick_title, indicator="->")
    return str(option)
