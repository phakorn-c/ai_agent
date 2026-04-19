# AI Coding Agent (Toy Project)

> **WARNING: This is a toy/educational project only!** Do NOT use this agent as-is in production or with sensitive codebases. Even tools like Cursor and Claude Code have security limitations. This is for learning purposes only.

## Overview

This is a minimal AI coding agent built from scratch that demonstrates the core concepts behind agentic coding tools like **Cursor**, **Zed's Agentic Mode**, or **Claude Code**. The agent can:

- Read files in a sandboxed working directory
- List directory contents
- Write or overwrite files
- Execute Python files

The agent operates in a loop, making function calls to explore and modify code, then formulating a response based on the results.

## Architecture

The agent follows an iterative loop pattern, where the LLM makes decisions, executes tools, and refines its understanding until it can provide a final answer.

```
┌─────────────┐     ┌──────────┐     ┌──────────────────────┐
│  User Input │────▶│    LLM   │────▶│  Function Decision   │
└─────────────┘     └──────────┘     └──────────────────────┘
                                              │
                                              ▼
                              ┌──────────────────────────────┐
                              │    Execute Tool (e.g.,       │
                              │    read file, run code)      │
                              └──────────────────────────────┘
                                              │
                                              ▼
                              ┌──────────────────────────────┐
                              │   Return Result to LLM       │
                              └──────────────────────────────┘
                                              │
                                              ▼
                         ┌─────────────────────────────────────────┐
                         │  Can the LLM answer now?                │
                         │  • Yes → Generate Final Response        │
                         │  • No  → Loop back for more info        │
                         │    (max 20 iterations)                  │
                         └─────────────────────────────────────────┘
```

### Core Components

| Component | Purpose |
|-----------|---------|
| `main.py` | Entry point - manages the agent loop, handles LLM communication |
| `prompts.py` | System prompt defining the agent's capabilities |
| `call_function.py` | Aggregates function schemas for the LLM |
| `functions/` | Individual tool implementations |
| `config.py` | Configuration (e.g., `MAX_CHARS` for file reading) |

### Tools/Functions

The agent has access to 4 core functions, each with proper schema definitions for Google's Gemini API:

1. **`get_files_info`** - Lists files and directories with size info
2. **`get_file_content`** - Reads file contents (truncates at 10,000 chars for safety)
3. **`write_file`** - Creates or overwrites files
4. **`run_python_file`** - Executes Python files with optional arguments

## Security Model

### Sandboxing

All file operations are sandboxed to a **working directory** (`./calculator` by default). The agent CANNOT:

- Access files outside the working directory
- Execute files outside the working directory
- Traverse to parent directories (e.g., `../`)
- Access absolute paths

### Path Validation

Each function validates paths using `os.path.commonpath()`:

```python
working_dir_abs = os.path.abspath(working_directory)
target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
valid_target_file = (
    os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
)
```

This ensures the resolved path stays within the sandbox.

### Execution Limits

- Python execution has a 30-second timeout
- File reads are truncated at 10,000 characters
- Maximum 20 iterations per request (prevents infinite loops)

## Key Learnings

### 1. Function Calling Architecture

The agent uses **function calling** (also called "tools" in some APIs) where the LLM decides which function to call and with what arguments. The results are fed back to the LLM to inform its next decision.

### 2. ReAct Pattern (Reasoning + Acting)

The agent follows a simplified ReAct pattern:
- **Reason**: The LLM decides what action to take based on current state
- **Act**: The agent executes the function call
- **Observe**: The result is added to the conversation history
- **Repeat** until task complete or max iterations reached

### 3. Security is Hard

Even with path validation, there are attack vectors:
- **Path traversal**: Need careful normalization and validation
- **Code execution**: Running arbitrary Python is inherently dangerous
- **Resource exhaustion**: Need timeouts and limits
- **Prompt injection**: The LLM could be manipulated to call functions maliciously

### 4. State Management

The conversation history (`messages`) maintains context across iterations. Each function call and result is appended, allowing the LLM to build understanding incrementally.

### 5. Tool Schemas

Google's Gemini API requires explicit schema definitions for each function:

```python
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory...",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path...",
            ),
        },
    ),
)
```

## Usage

### Prerequisites

- Python 3.14+
- Gemini API key
- UV (package manager)

### Setup

```bash
# Install dependencies
uv sync

# Set your API key
export GEMINI_API_KEY="your-key-here"
# Or create a .env file with GEMINI_API_KEY=...
```

### Running the Agent

```bash
# Basic usage
uv run python main.py "List all files in the calculator directory"

# With verbose output (shows function calls and token usage)
uv run python main.py --verbose "What does the calculator do?"
```

### Example Interaction

```bash
$ uv run python main.py --verbose "Read the calculator code and explain what it does"
 - Calling function: get_files_info
 -> result: files listed...
 - Calling function: get_file_content
 -> result: file contents...

The calculator is a simple arithmetic evaluator that...
Prompt tokens: 245
Response tokens: 189
```

## Project Structure

```
ai_agent/
├── main.py                    # Entry point and agent loop
├── prompts.py                 # System prompt
├── call_function.py           # Function schema aggregation
├── config.py                  # Configuration
├── pyproject.toml             # Dependencies
├── .env                       # API key (gitignored)
├── functions/
│   ├── call_function.py       # Function dispatcher
│   ├── get_files_info.py      # List directory contents
│   ├── get_file_content.py    # Read files
│   ├── write_file.py          # Write files
│   └── run_python_file.py     # Execute Python
├── calculator/                # Example sandboxed project
│   ├── main.py
│   ├── pkg/
│   │   └── calculator.py
│   └── tests.py
└── test_*.py                  # Unit tests for functions
```

## Testing

Individual functions have test files to verify sandboxing and error handling:

```bash
# Test file reading
uv run test_get_file_content.py

# Test directory listing
uv run test_get_files_info.py

# Test file writing
uv run test_write_file.py

# Test Python execution
uv run test_run_python_file.py
```

## Limitations & Warnings

### What This Agent CANNOT Do (Safely)

- Work with real codebases without extensive security review
- Handle multi-file refactorings reliably
- Guarantee code correctness
- Protect against all prompt injection attacks
- Handle complex dependencies

## Comparison to Production Tools

| Feature | This Toy | Cursor/Claude Code |
|---------|----------|-------------------|
| Security | Basic path validation | Multiple sandbox layers, permission prompts |
| Context | Single conversation | Persistent, multi-session |
| Tools | 4 basic functions | Dozens of specialized tools |
| Error handling | Basic | Sophisticated retry and recovery |
| Code understanding | None | AST parsing, semantic analysis |
| Safety | ⚠️ Minimal | ✅ Extensive guardrails |

## Further Learning

To build a production-quality agent, I need to study:

1. **Sandboxing techniques**: Docker containers, Firecracker microVMs
2. **Static analysis**: AST parsing, type checking, code verification
3. **Planning algorithms**: ReAct, Reflexion, Tree of Thoughts
4. **Safety mechanisms**: Human-in-the-loop, permission systems
5. **Context management**: Vector databases, code embeddings
6. **Testing strategies**: Self-healing code, verification loops

## Acknowledgments

Built as a learning project while studying AI engineering concepts. Inspired by:
- [Cursor](https://cursor.sh/) - The AI Code Editor
- [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
- [Zed](https://zed.dev/) - The Agentic Editor

## License

Educational use only. See WARNING at the top of this file.

---

**Remember**: This is a learning exercise. Real AI coding agents require significant safety engineering before they can be trusted with production code.
