""" Logical entry point for the bcorag module.
Handles the actual pipeline steps for each step in the RAG pipeline. 
"""

from bcorag import misc_functions as misc_fns
from bcorag import pdf_picker as pp


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
    user_choices = pp.initialize_picker()
    if user_choices is None:
        misc_fns.graceful_exit()
    return user_choices
