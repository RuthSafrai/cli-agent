# Text to CLI Agent

An agent that takes an instruction in natural language (Hebrew or English) and returns a single command-line command.

The code in this project is intentionally simple. The main work is prompt engineering: writing, testing, measuring, and improving the prompt over several iterations.

Examples:

| Natural-language instruction | Command |
|---|---|
| What is my computer's IP address? | `ipconfig` |
| Which processes are currently running on the system? | `tasklist` |

The agent only writes the command. It does not run it.

## How to run

Requirements: [uv](https://docs.astral.sh/uv/) and a Gemini API key from Google AI Studio.

```bash
uv sync
```

Create a `.env` file in the project root (it is not committed to Git):

```
GEMINI_API_KEY=your_key_here
```

Run:

```bash
uv run cli-agent
```

The Gradio interface opens in your browser at http://127.0.0.1:7860.

## Project structure

```
src/cli_agent/
  __init__.py   # The code: loading the prompt, calling the LLM, Gradio UI
  prompt.md     # The prompt
```

## Test scenarios and results

All scenarios and results are documented in a Google Sheet, with a separate heading for each iteration:

https://docs.google.com/spreadsheets/d/1gIPDSFmup1T3tnVxdpPOsW3-dmMNhnNEl9SWr-VyTWo/edit?usp=sharing

Evaluation metrics in the sheet:

- Valid to run
- Safe
- Suitable for Windows 11, runnable in PowerShell

## Interesting failures and what I learned from them

### 1. Without an explicit definition, the model mixes operating systems

**What happened:** With the simple prompt, many of the answers were Linux commands (`ps aux`, `ls -la`, `df -h`, `rm`, `cp`), even though the computer runs Windows.

**Why it's a problem:** The commands don't run, even if they are valid on their own.

**Fix:** I added an explicit requirement that the command must be suitable for Windows 11.

### 2. A command that looks valid but doesn't actually run

**What happened:** For a question about free disk space, the model returned `wmic logicaldisk get caption,freespace,size`. In PowerShell on my machine, I got the error `wmic is not recognized`, because the tool has been deprecated.

**Why it's a problem:** The command passes a syntax check but fails at runtime.
