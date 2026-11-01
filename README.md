# Text to CLI Agent

An agent that takes an instruction in natural language (Hebrew or English) and returns a single command-line command for **Windows 11 / PowerShell**.

The code in this project is intentionally simple. The main work is **prompt engineering**: writing, testing, measuring, and improving the prompt over several iterations.

Examples:

| Natural-language instruction                         | Command    |
|------------------------------------------------------|------------|
| What is my computer's IP address?                    | `ipconfig` |
| Which processes are currently running on the system? | `tasklist` |

The agent only writes the command. It does not run it.

## How to run

Requirements: [uv](https://docs.astral.sh/uv/) and a Gemini API key from [Google AI Studio](https://aistudio.google.com/api-keys).

```
uv sync
```

Create a `.env` file in the project root (it is not committed to Git):

```
GEMINI_API_KEY=your_key_here
```

Run:

```
uv run cli-agent
```

The Gradio interface opens in your browser at [http://127.0.0.1:7860](http://127.0.0.1:7860).

## Project structure

```
src/cli_agent/
  __init__.py     # The code: loading the prompt, calling the LLM, Gradio UI
  prompt_v1.md    # Prompt, iteration 1
  prompt_v2.md    # Prompt, iteration 2
  prompt_v3.md    # Prompt, iteration 3
```

The active prompt is selected by the `PROMPT_FILE` variable in the code. Each version is kept in its own file, so the changes between iterations are visible.


## Configuration

- **Provider and model:** Google Gemini API (`google-genai` library).
- **Temperature:** 0, so the same instruction gives the same command and iterations can be compared fairly.
- **Target environment:** Windows 11, PowerShell.

## Prompt iterations

Each iteration changes the prompt, is tested, and is scored in the Google Sheet (one tab per iteration).

| Iteration | File | What changed |
|---|---|---|
| 1 | `prompt_v1.md` | A single-sentence prompt: convert the request into a command to run in the terminal. No target OS, no format rules. |
| 2 | `prompt_v2.md` | Added a role, a target of **Windows PowerShell**, an explicit output-format rule (no text around the command), and four few-shot examples. |
| 3 | `prompt_v3.md` | TODO: describe what changed (for example the safety rules and the handling of non-command requests). |


## Test scenarios and results

All scenarios and results are documented in a Google Sheet:

[https://docs.google.com/spreadsheets/d/1gIPDSFmup1T3tnVxdpPOsW3-dmMNhnNEl9SWr-VyTWo/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1gIPDSFmup1T3tnVxdpPOsW3-dmMNhnNEl9SWr-VyTWo/edit?usp=sharing)

Evaluation metrics in the sheet:

- **Valid / runs:** the command works.
- **Safe:** dangerous commands are not returned as-is.
- **Suitable for Windows 11, runnable in PowerShell.**

## Interesting failures and what I learned from them

### 1. Without an explicit definition, the model mixes operating systems

**What happened:** With the simple prompt, many of the answers were Linux commands (`ps aux`, `ls -la`, `df -h`, `rm`, `cp`), even though the computer runs Windows.

**Why it's a problem:** The commands don't run, even if they are valid on their own.


### 2. Extra text around the command
 
**What happened:** With an empty or very general prompt, the model answered with long explanations, several operating systems, and Markdown formatting instead of one command.