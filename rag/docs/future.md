# Future Direction

Planned future steps can be broken down into two categories: [Experimental](#experimental) and [Production](#production).

## Experimental

There are various experimental features and optimizations that still need to be explored.

**Supplementary Data Loaders**:

- The supplementary Github reader offers improved specificity in the generation of any workflow specific domains. However, the implementation of the Github loader still requires some manual human parsing of the paper in order to identify the relevant Github repository link.
  - Could we implement intelligent parsing of the paper during the ingestion process to automatically identify and include relavant Github repository URLs without user intervention?
  - Right now only one repository URL is supported, expand support to allow for an arbitrary amount of supplementary repositories.
- The only supplementary data loader supported right now is the _GithubRepositoryReader_, could explore other external data loaders to further increase generated output specificity.

**Large Language Model**:

- Right now the tool only supports OpenAI LLMs, we will explore various open source options such as Meta's [Llama 3](https://llama.meta.com/llama3/) model and the Technology Innovation Institute's [Falcon](https://falconllm.tii.ae/) model.

**Chunking Strategy**:

- Right now, the only supported chunking strategy employed splits documents into chunks of size 1,024 with an overlap of 20. 
- Various chunking strategies will be explored and optimized with various embedding models.

**Intelligent Metadata Filtering**:

- No metadata filtering is currently supported.
- Will explore various intelligent metadata filtering to filter the candidate set of Nodes before the semantic search is performed.

## Production

**Design**: For a production implementation of this tool, a microservices architecture could be designed to handle the various steps in the RAG pipeline such as indexing, information retrieval, and querying.

**Data Collection and Evaluation**: The tool's frontend interface could provide some way for the user to rate the output quality. This option could be as granular as a rating scale or as simple as a binary thumbs up or thumbs down. This will allow for the collection of a robust training set that could be used for on-the-fly reinforcement learning or training a proprietary BCO LLM.

**A/B Testing**: Users could be presented with various backend configurations at random and based on user feedback we could eventually determine the most reliable RAG configuration.
