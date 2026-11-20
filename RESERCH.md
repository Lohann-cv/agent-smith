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
- How can I give feedback to the LLM and prevent silcent failures and Hallucinations ?
- What is an MCP and how can we use it ?
- How can you generate good sandbox manual dynamicly ? (With pydentic and JSON)
- How can you implement good security mecanisme ?
- What kind of great MCP tool could I implement ?
- What kind of LLM is the best to take ?
- How can you understand agent system, what are the, loop, tools and prompts of the greatest ?

#### List of free provider

**We must use at least 5 models across at least 2 providers, on the same set of at least 3 SWE-bench tasks**

- OpenRouter
- Together AI
- Groq
- Google IA Studio (Gemini)
- Mistral IA
- Cohere
- Fireworks AI
- Perplexity AI
- Anyscale 
