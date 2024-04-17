""" Handles the RAG implementation using the llama-index library.
"""

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.llms.openai import OpenAI  # type: ignore
from llama_index.embeddings.openai import OpenAIEmbedding  # type: ignore
from dotenv import load_dotenv
import tiktoken
import bcorag.misc_functions as misc_fns
from bcorag.prompts import QUERY_PROMPT, USABILITY_DOMAIN


class BcoRag:
    """Class to handle the RAG implementation."""

    def __init__(self, user_selections: dict[str, str]):
        """Constructor.

        Parameters
        ---------
        user_selections : dict[str, str]

        Attributes
        ----------
        debug : bool
            Whether in debug mode or not.
        file_name : str
            The file name that is being indexed.
        logger : logging.Logger
            The document specific logger.
        embed_model : OpenAIEmbedding
            The embedding model instance.
        documents : list[Documents]
            The list of documents (containers for the data source).
        index : VectorStoreIndex
            The vector indexer instance.
        domain_map : dict
            Mapping for each domain to its standardized prompt.
        token_counter : TokenCountingHandler or None
            The token counter handler or None if mode is production.
        token_counts : dict or None
            The token counts or None if mode is production.
        """
        _llm_model_name = user_selections["llm"]
        _embed_model_name = user_selections["embedding_model"]
        _file_name = user_selections["filename"]
        _file_path = user_selections["filepath"]
        _vector_store = user_selections["vector_store"]
        _loader = user_selections["loader"]
        _mode = user_selections["mode"]

        load_dotenv()

        self.debug = True if _mode == "debug" else False
        self.file_name = _file_name
        self.logger = misc_fns.setup_document_logger(
            self.file_name.lower().strip().replace(" ", "_")
        )

        # setup embedding model
        self.embed_model = OpenAIEmbedding(model=_embed_model_name)
        Settings.embed_model = self.embed_model

        # setup llm model
        Settings.llm = OpenAI(model=_llm_model_name)

        # handle data loader
        if _loader == "SimpleDirectoryReader":
            self.documents = SimpleDirectoryReader(input_files=[_file_path]).load_data()
        # handle indexing
        if _vector_store == "VectorStoreIndex":
            self.index = VectorStoreIndex.from_documents(self.documents)

        # domain mapping
        self.domain_map = {"usability": USABILITY_DOMAIN}

        # handle additional output for debugging mode
        if self.debug:
            self.token_counter: TokenCountingHandler | None = TokenCountingHandler(
                tokenizer=tiktoken.encoding_for_model(_llm_model_name).encode
            )
            Settings.callback_manager = CallbackManager([self.token_counter])
            self.token_counts: dict | None = {
                "embedding": self.token_counter.total_embedding_token_count,
                "input": 0,
                "output": 0,
                "total": 0,
            }
        else:
            self.token_counter = None
            self.token_counts = None

    def perform_query(self, domain: str) -> str:
        """Performs a qeury for a specific BCO domain.

        Parameters
        ----------
        domain : str
            The domain being queried for.

        Returns
        -------
        str
            The generated domain.
        """
        query_engine = self.index.as_query_engine()
        query_prompt = QUERY_PROMPT.format(domain, self.domain_map[domain])
        if self.debug:
            self._print_debug_info()
        # TODO: implement query logic, conditional debug logging and replace temporary return
        return query_prompt

    def _print_debug_info(self):
        """If in debug mode, handles the debug info output to the log file."""
        # TODO
        self.logger.info("test")
