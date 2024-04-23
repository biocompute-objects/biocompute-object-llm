""" Logical entry point for the bcorag module.
Handles the actual pipeline steps for each step in the RAG pipeline. 
"""

from bcorag import misc_functions as misc_fns
from bcorag import option_picker as op
from bcorag.bcorag import BcoRag


def initalize_step() -> dict | None:
    """Initializes the RAG pipeline by letting the user choose all of
    the initial pipeline options, including which PDF to index, which
    data loader to use, which embedding model to use, and which index
    store to use.

    Returns
    -------
    dict or None
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
    user_choices = op.initialize_picker()
    return user_choices

def retrieve_bco_rag(options: dict) -> BcoRag:
    """ Handles the RAG setup using the options selected by the user
    in the initialization step.

    Parameters
    ----------
    options : dict
        The user choices dictionary returned by the initialize_step.

    Returns
    -------
    BcoRag
        An instance of the BcoRag.
    """
    return BcoRag(options)
