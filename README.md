# AI Agent

hey! so i built this little AI agent because i've been really interested in agentic AI lately and wanted to understand how it actually works under the hood.

**disclaimer:** this is just a fun project i made for learning. test it at your own risk lol

## what is this?

basically it's a coding assistant that uses Google's Gemini API (gemini-2.5-flash) and can actually *do* stuff instead of just talking about it. it has a feedback loop where the AI can use tools, see the results, and keep iterating until it completes a task.

## what can it do?

the agent has access to these tools:
- **list files** - browse directories and see what's there
- **read files** - get the contents of any file in the workspace
- **write files** - create or modify files
- **run python scripts** - execute python files and see their output

it's set up with a proper agentic loop (max 20 iterations) so it can chain these operations together. like you can ask it to "fix the bug in calculator" and it'll actually:
1. list files to find what's there
2. read the relevant code
3. run tests to see what's broken
4. write fixes
5. run tests again to verify

pretty cool stuff.

## how to use

you need a Gemini API key first. throw it in a `.env` file:
```
GEMINI_API_KEY=your_key_here
```

then just run:
```bash
uv run main.py "your prompt here"
```

add `--verbose` if you want to see all the token counts and function calls:
```bash
uv run main.py "what files are in the root?" --verbose
```

## project structure

```
functions/          # all the tool implementations + schemas
  get_files_info.py
  get_file_content.py
  write_file.py
  run_python_file.py
main.py            # the main agent loop
call_function.py   # helper for calling tools
prompts.py         # system prompt
```

## tech stuff

- uses Google's `genai` Python SDK
- function calling / tool use pattern
- conversation history maintained across iterations
- security checks to keep operations within the working directory
- proper error handling and timeouts

## why?

honestly just wanted to learn how these AI agents actually work. seeing the model iteratively use tools and maintain context across multiple steps is pretty fascinating. way different than just chatting with an LLM.

feel free to mess around with it or use it as a reference if you're learning about agentic AI too 👍
