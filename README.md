# Multi-Agent-RAG

A powerful document question-answering system powered by Docling and LangGraph, featuring a multi-agent workflow for accurate and verified answers.

## Features

- **Multi-Agent Workflow**: Research, verification, and relevance checking agents
- **Document Processing**: Support for PDF, DOCX, TXT, and MD files
- **Hybrid Retrieval**: Combines dense and sparse retrieval for better results
- **Answer Verification**: Built-in fact-checking and verification
- **Modern Chat Interface**: Powered by Chainlit
- **Session Management**: Efficient document caching and state management

## Quick Start

### Prerequisites

- Python 3.10+ (recommended)
- [uv](https://github.com/astral-sh/uv) (for fast dependency management)

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd Multi-Agent-RAG
    ```

2. Install dependencies using `uv`:
    ```bash
    uv pip install -e .
    ```

    > If you don’t have `uv` installed, get it with:
    > ```bash
    > pip install uv
    > ```

### Running the Chainlit Interface

Start the Chainlit chat interface:
```bash
chainlit run chainlit.py
```

The interface will be available at [http://localhost:8000](http://localhost:8000).

## Usage

### Document Upload

1. Upload your documents (PDF, DOCX, TXT, MD) in the chat interface.
2. The system will process and index them automatically.
3. Documents are cached for efficient reuse.

### Asking Questions

1. Type your question in the chat.
2. The system will:
    - Check document relevance
    - Research the answer using retrieved documents
    - Verify the answer for accuracy
    - Provide both the answer and verification report


## Architecture

### Multi-Agent Workflow

1. **Relevance Checker**: Determines if documents can answer the question
2. **Research Agent**: Generates initial answers from retrieved documents
3. **Verification Agent**: Checks answer accuracy and provides verification report

### Document Processing

- **File Handler**: Processes various document formats
- **Chunking**: Splits documents into manageable chunks
- **Embedding**: Creates vector representations for retrieval

### Retrieval System

- **Hybrid Retriever**: Combines dense (vector) and sparse (BM25) retrieval
- **ChromaDB**: Vector database for document storage
- **Ensemble**: Merges results from multiple retrieval methods

## Configuration

Settings are managed through the `config/` directory:
- `constants.py`: System constants and file type definitions
- `settings.py`: Environment-specific settings

### Supported File Types

- PDF (`.pdf`)
- Word documents (`.docx`)
- Text files (`.txt`)
- Markdown files (`.md`)

## Development

### Project Structure

```
Multi-Agent-RAG/
├── agent/                 # Multi-agent workflow
│   ├── workflow.py        # Main workflow orchestration
│   ├── research_agent.py  # Research agent implementation
│   ├── verification_agent.py # Verification agent
│   └── relevance_checker.py  # Relevance checking
├── retriever/             # Document retrieval system
│   ├── builder.py         # Retriever construction
│   └── file_handler.py    # Document processing
├── config/                # Configuration files
├── utils/                 # Utility functions
├── chainlit.py            # Chainlit interface (entrypoint)
├── pyproject.toml         # Project dependencies
└── uv.lock                # uv dependency lockfile
```

### Adding New Agents

1. Create a new agent class in the `agent/` directory
2. Implement the required interface methods
3. Add the agent to the workflow in `agent/workflow.py`

### Extending Document Support

1. Add new file type to `constants.ALLOWED_TYPES`
2. Implement processing logic in `retriever/file_handler.py`
3. Update the interface validation

## Troubleshooting

### Common Issues

1. **Document Processing Errors**: Ensure files are not corrupted and in supported formats
2. **Memory Issues**: Large documents may require more memory allocation
3. **Retrieval Performance**: Consider adjusting chunk sizes or retrieval parameters

### Logging

The system uses structured logging. Check logs for detailed error information:
```bash
tail -f chainlit.log  # For Chainlit interface
```

## Acknowledgments

- Built with [Docling](https://github.com/docling-ai/docling)
- Powered by [LangGraph](https://github.com/langchain-ai/langgraph)
- Interface: [Chainlit](https://chainlit.io/)