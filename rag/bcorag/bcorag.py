""" Handles the RAG implementation using the llama-index library.
"""

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.llms.openai import OpenAI  # type: ignore
from llama_index.embeddings.openai import OpenAIEmbedding  # type: ignore
from dotenv import load_dotenv
import tiktoken
import os
import json
import bcorag.misc_functions as misc_fns
from bcorag.prompts import (
    QUERY_PROMPT,
    TOP_LEVEL_SCHEMA,
    USABILITY_DOMAIN,
    IO_DOMAIN,
    DESCRIPTION_DOMAIN,
    EXECUTION_DOMAIN,
    PARAMETRIC_DOMAIN,
    ERROR_DOMAIN,
)


class BcoRag:
    """Class to handle the RAG implementation."""

    def __init__(self, user_selections: dict[str, str], output_dir: str = "./output"):
        """Constructor.

        Parameters
        ---------
        user_selections : dict[str, str]
            The user configuration selections.
        output_dir : str (default: "./output")
            The directory to dump the outputs.

        Attributes
        ----------
        output_path : str
            Path to the specific document directory to dump the outputs.
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

        self.output_path = f"{output_dir}/{os.path.splitext(_file_name.lower().replace(' ', '_').strip())[0]}/"
        misc_fns.check_dir(self.output_path)
        self.debug = True if _mode == "debug" else False
        self.file_name = _file_name
        self.logger = misc_fns.setup_document_logger(
            self.file_name.lower().strip().replace(" ", "_")
        )
        self._display_info(user_selections, "User selections:")

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
        self.domain_map = {
            "usability": {
                "prompt": USABILITY_DOMAIN,
                "user_prompt": "[u]sability",
                "code": "u",
            },
            "io": {"prompt": IO_DOMAIN, "user_prompt": "[i]o", "code": "i"},
            "description": {
                "prompt": DESCRIPTION_DOMAIN,
                "user_prompt": "[d]escription",
                "code": "d",
            },
            "execution": {
                "prompt": EXECUTION_DOMAIN,
                "user_prompt": "[e]xecution",
                "code": "e",
            },
            "parametric": {
                "prompt": PARAMETRIC_DOMAIN,
                "user_prompt": "[p]arametric",
                "code": "p",
            },
            "error": {"prompt": ERROR_DOMAIN, "user_prompt": "[err]or", "code": "err"},
        }

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
        query_engine = self.index.as_query_engine(verbose=self.debug)
        query_prompt = QUERY_PROMPT.format(domain, self.domain_map[domain]["prompt"])
        response_object = query_engine.query(query_prompt)
        query_response = str(response_object)

        if self.debug:
            self._display_info(query_prompt, f"QUERY PROMPT for the {domain} domain:")
            self.token_counts["input"] += self.token_counter.prompt_llm_token_count  # type: ignore
            self.token_counts["output"] += self.token_counter.completion_llm_token_count  # type: ignore
            self.token_counts["total"] += self.token_counter.total_llm_token_count  # type: ignore
            self.token_counts["embedding"] += self.token_counter.total_embedding_token_count # type: ignore
            self._display_info(self.token_counts, "Updated token counts:")

        self._process_output(domain, query_response)

        return query_response

    def choose_domain(
        self, automatic_query: bool = False
    ) -> tuple[str, str] | str | None:
        """Gets the user input for the domain the user wants to generate.

        Parameters
        ----------
        automatic_query : bool (default: False)
            Whether to automatically query after the user chooses a domain. If set to
            True this is a shortcut to calling bcorag.perform_query(choose_domain()).

        Returns
        -------
        (str, str), str or None
            If automatic query is set to True will return a tuple containing the domain
            name and the query response. If automatic query is False will return the user
            chosen domain. None is returned if the user chooses to exit.
        """
        domain_prompt = (
            "Which domain would you like to generate? Supported domains are:"
        )
        for domain in self.domain_map.keys():
            domain_prompt += f"\n\t{self.domain_map[domain]['user_prompt']}"
        domain_prompt += "\n\tE[x]it\n"
        print(domain_prompt)
        domain_selection = None
        while True:
            domain_selection = input().strip().lower()
            for domain in self.domain_map.keys():
                if (
                    domain_selection == domain
                    or domain_selection == self.domain_map[domain]["code"]
                ):
                    domain_selection = domain
                    break
            else:
                if domain_selection == "exit" or domain_selection == "x":
                    if self.debug:
                        self._display_info(
                            "User selected 'exit' on the domain selection step."
                        )
                    return None
                else:
                    if self.debug:
                        self._display_info(
                            f"User entered unrecognized input '{domain_selection}' on domain chooser step."
                        )
                    print(
                        f"Unrecognized input {domain_selection} entered, please try again."
                    )
                    continue
            break
        if automatic_query:
            if self.debug:
                self._display_info(
                    f"Automatic query called on domain: '{domain_selection}'."
                )
            return domain_selection, self.perform_query(domain_selection)
        if self.debug:
            self._display_info(
                f"User chose '{domain_selection}' with no automatic query."
            )
        return domain_selection

    def _process_output(self, domain: str, response: str):
        """Attempts to serialize the response into a JSON object and dumps the raw text.

        Parameters
        ----------
        domain : str
            The domain the response is for.
        response : str
            The generated response to dump.
        """
        txt_file = f"{self.output_path}{domain}_domain.txt"
        json_file = f"{self.output_path}{domain}_domain.json"
        if response.startswith("```json\n"):
            response = response.replace("```json\n", "").replace("```", "")
        self._display_info(response, f"QUERY RESPONSE for the '{domain}' domain:")
        with open(txt_file, "w") as f:
            f.write(response)
        try:
            response_json = json.loads(response)
            if misc_fns.write_json(json_file, response_json):
                self.logger.info(
                    f"Successfully serialized JSON response for the '{domain}' domain."
                )
        except Exception as e:
            self.logger.error(
                f"Failed to serialize the JSON response for the '{domain}' domain. View raw output in the txt file located at '{txt_file}'.\n{e}"
            )

    def _display_info(self, info: dict | list | str | None, header: str | None = None):
        """If in debug mode, handles the debug info output to the log file.

        Parameters
        ----------
        info : dict, list, str or None
            The object to log.
        header : str or None (efault: None)
            The optional header to log before the info.
        """
        log_str = header if header is not None else ""
        if isinstance(info, dict):
            for key, value in info.items():
                log_str += f"\n\t{key}: '{value}'"
        elif isinstance(info, str):
            log_str += f"{info}" if header is None else f"\n{info}"
        self.logger.info(log_str)
