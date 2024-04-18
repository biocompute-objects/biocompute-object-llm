# BioCompute Object Assistant

## Background

The BioCompute Object (BCO) project is a community-driven open standards framework for standardizing and sharing computations and analyses. With the exponential increase in both the quantity and complexity of biological data and the workflows used to analyze and transform the data, the need for standardization in documentation is imperative for experimental preservation, transparency, accuracy, and reproducability.

As with any documentation standard, the main hurdles to continued adoption are the overhead required to maintain the quality and accuracy of a BCO in parallel as the research evolves over time and retroactively documenting pre-existing research. With the recent improvements in large language models (LLMs), the feasibility and utility of an automated BCO creation assistant is an intriguing use case.  

## Approaches

For this proof of concept, two main approaches were explored: the [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview?context=with-streaming) and a Retrieval-Augmented Generation (RAG) pipeline using the Python [LlamaIndex](https://docs.llamaindex.ai/en/stable/) library. Each approach is described further in their respective directories. 

## Testing

For baseline testing, a hand-selected set of papers were used (found in the `papers/` directory). 

## Results
