NOVA Chatbot — Full Feature Documentation (v1 2025 Edition)


🧠 1. Local LLaMA Chat Engine
Runs LLaMA .gguf models locally using llama.cpp or llama-cpp-python
Works offline for basic Q&A, conversation, and reasoning
No internet or OpenAI API is required
Responses are fast and context-aware (limited to system RAM & model size)

🔐 2. Privacy & Local Execution
All files, messages, and queries stay on your device
No cloud processing — your data is not sent to external servers
No telemetry, no tracking, no third-party logins

🔍 3. Online Research Mode
Scrapes online sources (like Google, Wikipedia, news, GitHub)
Can be activated by a command like !research <topic>
Fetches live content and summarizes it using the local model

📄 4. Document Analysis
Supports .pdf, .txt, .docx, .md files
Breaks documents into chunks and embeds them locally using sentence-transformers
Ask questions about a document like:
“What is the summary?” or “What does it say on page 3?”

💾 5. Memory System
Uses FAISS for vector-based local memory
Stores chat history, file embeddings, and research points
Search memory using similarity matching

🧩 6. Plugin Support
NOVA can load custom tools from the /plugins/ folder
Example plugins:
news_scraper.py
github_scraper.py
reddit_scraper.py
pdf_embedder.py
You can build your own tool using a simple run(query) function

⚙️ 7. Command-Based Operation
NOVA supports text commands like:
!research <topic> – trigger web research
!upload <file> – upload and embed documents
!memory search <query> – search previous embeddings
!clear – clear session memory

🖥️ 8. Works in VS Code or Terminal
Can be run directly using:
python main.py
Full development and usage experience inside Visual Studio Code

📦 9. Environment Configurable
Easily configured using .env file:
MODEL_PATH=models/llama-3-8b.Q4_K_M.gguf
ENABLE_MONGODB=false
VECTOR_STORE=faiss
ONLINE_MODE=true

🧪 10. Ideal For:
Students who want offline study help
Developers who want a customizable assistant
Researchers doing secure or sensitive work
Anyone who needs a private AI that can also browse the internet when needed
