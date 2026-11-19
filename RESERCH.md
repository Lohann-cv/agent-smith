*This documents is the glosary of all of my recherche on the agent simth project*

# Agent Smith

**The goal of the project:** We'll be creating an IA agent that will be able to:
- Write executable Python code
- Call tools directly from code
- Observe execution results
- Iterate until the task is solved

It'll operate through a loop: **Thought --> Code --> Observation**
And we'll aply this framework to two differents benchmarks:
- MBPP: algorithmic Python problems
- SWE-bench: real-world bug fixig in production repositories
The agent must be **Safe, controlled, reproductible and measurable**.

##### What is a Code Agent ?

It's an IA system that is able to reason about a given task, generate executable code, execute that code in a controlled environment, use tools, to interact with files, test and repositories.
It's using code-base tool calling.
It allow:
- Persistent variables between steps
- Conditional logic and loops
- Complex multi-step reasoning

It opereate through a series of steps:
1. Agent/Orchestrator: Call LLM, extracts code, feeds to sandbox, reads observation and repeats
2. Code Extraction: The step between the LLM <--> and sandbox
3. Sandbox: The place where code is safly executed
4. final_answer(): A built in sandbox construct
5. MCP Server(s): run as separated process(es). Only our MCP are allowed. (All execution appen init).

**We cannot use lib that re-implements agent orchestration (llama-index, smolagents, langgraph, crewai, autogen)**

### QnA

- How can you implement a sandbox ?
- How can you implement models and track their usage ?
- How can you implement tools and makes them work independently of the loop ? (To not stop the loop I gess)
- How can you implement an agent loop ? (Thought --> Code --> Observation).
- How can you implement multi-agent infrastructure?
- How can you make an instraction layer and make it produce different format such as:
    * Python code block
    * XML tool calls
    * JSON/Hermes tool calls
    * ReAct format
- How can I execute code inside the sandbox ? And make it solve benchmark tasks ?
- About system prompt:
    * How can I implement it ?
    * What kind of tool can I give it to ?
    * How can I recode Claud Opuse 9.42  ?
