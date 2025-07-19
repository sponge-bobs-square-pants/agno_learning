# agno_learning

![Python](https://img.shields.io/badge/python-3.13%2B-blue)
![Agno](https://img.shields.io/badge/Agno-1.7.5%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A modern, modular playground for building, experimenting with, and learning about agentic AI systems using the Agno framework, and state-of-the-art LLMs (Groq, OpenAI, etc). This project demonstrates best practices for agent design, tool integration, memory, state management, and human-in-the-loop workflows.

---

## WARNING:

- **THE READ ME FILE IS COMPLETELY GENERATED USING copilot. User discretion is advised.**

---

## 🚀 Features

- **Agentic AI Patterns**: Build and compose agents with tools, memory, and state.
- **Modular Design**: Each module demonstrates a key concept (Agents, Tools, Memory, State, HITL).
- **Toolkits**: Easily add, include, or exclude tools for agent customization.
- **Stateful Workflows**: Use custom state and conditional logic for advanced flows.
- **Memory**: Implement session, user, and summary memory for context retention.
- **Human-in-the-Loop**: Add user approval and feedback steps for safe, robust agents.
- **Modern LLMs**: Integrate with Groq, OpenAI, and more.
- **Best Practices**: Follows Agno 1.7.5+ standards and agentic design patterns.

---

## 📦 Project Structure

- `1. Agent/` — Agent examples, teams, and orchestration
- `2. Tools/` — Custom tools and toolkits for agent capabilities
- `3. Memory/` — Memory patterns: built-in, session, user, summary
- `4. State/` — Custom state schemas, stateful workflows, and tools
- `5. Human In the Loop/` — Human approval and feedback patterns
- `cache/` — Cached tool results and intermediate data
- `tmp/` — Temporary files and databases

Each module contains its own README with details and usage examples.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sponge-bobs-square-pants/agno_learning.git
   cd agno_learning
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or, if using Poetry
   poetry install
   ```
3. **Set up environment variables:**

   - Copy `.env.example` to `.env` and add your API keys (GROQ, OPENAI, etc).

4. **Run examples:**
   - Explore each module and run the Python scripts to see different agentic patterns in action.

---

## 📚 Modules Overview

- **Agent**: How to build single and multi-agent systems, including teams and role-based orchestration.
- **Tools**: How to create, include, or exclude tools and toolkits for agent customization.
- **Memory**: How to add memory to agents for context retention and smarter interactions.
- **State**: How to define and use custom state for advanced workflows.
- **Human In the Loop**: How to add user approval and feedback steps for critical actions.

---

## 🧑‍💻 Contributing

Contributions, issues, and feature requests are welcome! Please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [ZenQuotes](https://zenquotes.io/)
- [icanhazdadjoke](https://icanhazdadjoke.com/)
- [Useless Facts](https://uselessfacts.jsph.pl/)

---
