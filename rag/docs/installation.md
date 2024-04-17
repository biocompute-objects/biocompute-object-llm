# Installation and Setup

- [Prerequisites](#prerequisites)
- [Virtual Environment](#virtual-environment)
- [OpenAI API Key](#openai-api-key)

## Prerequisites

This directory requires at least Python 3.10 to setup. The code in this directory makes extensive use of an alternate way to indicate union types as `X | Y` instead of `Union[X, Y]`.

## Clone the repository

First, clone the repository to your machine: 

```bash
git clone git@github.com:biocompute-objects/biocompute-object-llm.git
```

This example uses the ssh method, replace with HTTPS URL as needed.

## Virtual Environment

Create a virtual environment from with the `rag/` directory:

```bash
cd rag/
virtualenv env
```

To activate the virtual environment on Windows:

```bash
env/Scripts/activate
```

To activate the virtual environment on MacOS/Linux:

```bash
source env/bin/activate 
```

Then install the `rag/` directory dependencies:

```bash
(env) pip install -r requirements.txt
```

## OpenAI API Key

Create your `.env` file and add your OpenAI API key. For example:

```.env
OPENAI_API_KEY=<KEY>
```

## Usage

The RAG approach can be run liek so: 

```bash
(env) python main.py
```

More documentation on usage can be found [here](./usage.md).
