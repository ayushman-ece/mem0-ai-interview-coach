# 🧠 AI Interview Prep Coach

An AI-powered interview preparation assistant built with **LangChain + Mem0 + Groq + Gemini + Qdrant + Streamlit**.

The goal of this project is to create a personalized AI interview coach that can remember information about a candidate across conversations and use those memories to provide personalized interview questions and feedback.

---

## 🚀 Project Overview

The AI Interview Prep Coach works as a personalized interview preparation assistant.

A user enters a **User ID** and starts chatting with the AI.

The system:

1. Receives the user's message through Streamlit.
2. Searches the user's previous memories using Mem0.
3. Retrieves relevant memories from Qdrant.
4. Sends the memories and current question to the AI coach.
5. Uses Groq through LangChain to generate the response.
6. Stores the new conversation in Mem0.
7. Keeps the memory persistent using Qdrant.
8. Allows the user to view their stored memories.

### Overall Architecture

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Streamlit    │
                    │       UI        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    LangChain    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      Groq       │
                    │  GPT-OSS-20B    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      Mem0       │
                    │ Long-term Memory│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Qdrant      │
                    │ Vector Database │
                    └─────────────────┘

              Gemini
                 │
        ┌────────┴────────┐
        ▼                 ▼
 Memory Extraction    Embeddings
```

---

# ✨ Features

## 🧠 1. AI Interview Coach

The application acts as an AI interview preparation coach.

It can:

- Ask interview questions
- Evaluate answers
- Give concise feedback
- Personalize questions
- Use previous candidate information
- Avoid repeating already covered topics
- Focus on weak areas
- Remember the candidate across sessions

---

## 👤 2. User-Based Memory

Each user can enter their own User ID.

Example:

```text
Ayushman
Rahul
Priya
Alex
```

Memories are associated with the User ID.

For example:

```text
User ID: Ayushman
```

The system searches memories belonging to Ayushman.

Another user:

```text
User ID: Rahul
```

will have a separate memory context.

---

# 💾 3. Persistent Memory

Mem0 manages the long-term memory layer.

Qdrant stores the vector representation of memories locally.

The persistent database is stored in:

```text
qdrant_data/
```

This allows memories to remain available after restarting the Streamlit application.

> ⚠️ Do not delete `qdrant_data/` if you want to keep the stored memories.

---

# 🔎 4. Memory Search

When a user asks something, the application searches for relevant memories.

The current Mem0 API uses:

```python
search_results = MEMORY.search(
    query=user_message,
    filters={
        "user_id": user_id
    },
    limit=5,
)
```

Only memories belonging to the current User ID are searched.

---

# 💾 5. Save Conversation

After generating an answer, the conversation is added to Mem0:

```python
MEMORY.add(
    [
        {
            "role": "user",
            "content": user_message,
        },
        {
            "role": "assistant",
            "content": reply,
        },
    ],
    user_id=user_id,
)
```

This allows future conversations to use information from previous conversations.

---

# 📚 6. Show Stored Memories

The sidebar contains:

```text
🧠 Show stored memories
```

When clicked, the application retrieves memories for the current User ID.

The memories are displayed in the Streamlit sidebar.

---

# 🗑️ 7. Clear Transcript

The application provides:

```text
🗑️ Clear transcript
```

This clears the current Streamlit conversation transcript.

### Important

Clearing the transcript does **not** delete Mem0 memories.

The memories remain stored in Qdrant.

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web UI |
| LangChain | LLM application framework |
| Groq | AI model provider |
| Mem0 | Long-term memory |
| Gemini | Memory extraction and embeddings |
| Qdrant | Vector database |
| python-dotenv | Environment variable management |
| uv | Python environment and dependency management |

---

# 🤖 AI Model

The interview coach uses:

```text
openai/gpt-oss-20b
```

through LangChain's `ChatGroq`.

The basic processing pipeline is:

```text
User Question
      +
Relevant Memories
      ↓
ChatPromptTemplate
      ↓
ChatGroq
      ↓
StrOutputParser
      ↓
AI Response
```

---

# 🧠 Mem0

Mem0 provides the long-term memory layer.

The application uses Mem0 to:

- Search previous memories
- Extract useful information
- Store conversations
- Retrieve user-specific memories
- Personalize future responses

---

# 🧬 Gemini Embeddings

Gemini is used for embeddings.

Configured embedding model:

```text
models/gemini-embedding-001
```

Embedding dimensions:

```text
768
```

Embeddings allow Qdrant to store and retrieve semantically related memories.

---

# 🗄️ Qdrant

Qdrant is used as the vector database.

Configuration:

```text
Collection:
mem0_interview_prep
```

Local storage:

```text
qdrant_data/
```

Qdrant allows the application to store and retrieve semantically related memories.

---

# 🔗 Complete Data Flow

When a user sends a message:

```text
User
 ↓
Streamlit
 ↓
chat()
 ↓
Mem0 Search
 ↓
Relevant Memories
 ↓
Prompt + Memories
 ↓
LangChain
 ↓
Groq GPT-OSS-20B
 ↓
AI Response
 ↓
Mem0.add()
 ↓
Qdrant
```

---

# 📁 Project Structure

```text
Model 2/
│
├── app.py
├── memory_agent.py
├── main.py
│
├── README.md
├── .gitignore
├── .env.example
│
├── pyproject.toml
├── uv.lock
│
├── .env
├── .venv/
├── .mem0/
└── qdrant_data/
```

---

# 📄 File Explanation

## `app.py`

This file contains the Streamlit user interface.

Main responsibilities:

- Configure Streamlit
- Create the application UI
- Accept User ID
- Display chat messages
- Accept user questions
- Call the `chat()` function
- Display AI responses
- Show stored memories
- Clear transcript

---

## `memory_agent.py`

This file contains the main AI and memory logic.

Responsibilities:

- Load environment variables
- Configure Mem0
- Configure Gemini
- Configure embeddings
- Configure Qdrant
- Configure LangChain
- Configure Groq
- Search memories
- Generate AI responses
- Store conversations
- Retrieve stored memories

---

## `main.py`

Additional Python file included in the project.

The main Streamlit application is launched through:

```powershell
uv run streamlit run app.py
```

---

## `.env`

Contains private API keys.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

### ⚠️ Never upload `.env` to GitHub.

---

## `.env.example`

Safe template for GitHub:

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

Other developers can copy:

```text
.env.example → .env
```

and then add their own API keys.

---

# 🔐 Environment Variables

The application loads environment variables using:

```python
load_dotenv(
    dotenv_path=PROJECT_ROOT / ".env"
)
```

Then:

```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

Required keys:

```text
GROQ_API_KEY
GOOGLE_API_KEY
```

---

# 🔒 Security

Never upload:

```text
.env
```

to GitHub.

Never expose:

```text
GROQ_API_KEY
GOOGLE_API_KEY
```

publicly.

The project uses environment variables so API keys are not hard-coded inside the Python source code.

If an API key is accidentally exposed, it should be revoked/rotated immediately.

---

# 🚫 Files That Should Not Be Uploaded

Do not commit these files/folders:

```text
.env
.venv/
.mem0/
qdrant_data/
```

These are local/private project data.

---

# 📋 `.gitignore`

Recommended `.gitignore`:

```gitignore
# Secrets
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtual environments
.venv/
venv/
env/
ENV/

# Mem0 local data
.mem0/

# Qdrant local database
qdrant_data/

# Jupyter
.ipynb_checkpoints/

# VS Code
.vscode/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Streamlit secrets
.streamlit/secrets.toml
```

---

# ▶️ How to Run

## Step 1 — Open the project

Open the `Model 2` directory in VS Code.

---

## Step 2 — Configure `.env`

Create:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

---

## Step 3 — Start Streamlit

From the `Model 2` directory:

```powershell
uv run streamlit run app.py
```

Streamlit will provide a URL such as:

```text
http://localhost:8501
```

Open that URL in your browser.

---

# 💻 Running From Any Directory

If the terminal is not already inside the project directory:

```powershell
cd "C:\Users\Lenovo\Desktop\llm 24-07-2026\Mem 0\Model 2"
uv run streamlit run app.py
```

This is the normal command used to start the application.

---

# ⚠️ Qdrant Lock Issue

Because Qdrant uses local persistent storage, only one active local Qdrant client should use the same `qdrant_data` folder at a time.

If this error appears:

```text
qdrant_data is already accessed by another instance of Qdrant client
```

it usually means another Streamlit/Python process is still running.

Stop old processes:

```powershell
taskkill /F /IM python.exe
taskkill /F /IM streamlit.exe
```

Then start the application:

```powershell
uv run streamlit run app.py
```

### Important

Normally you should **not** need to use `taskkill`.

Use only one Streamlit process at a time.

---

# 🧪 Example Usage

## Step 1

Enter:

```text
User ID: Ayushman
```

## Step 2

Ask:

```text
I am preparing for Python interviews.
```

The AI responds and Mem0 can store relevant information.

## Step 3

Ask another question later:

```text
What should I focus on next?
```

The system can retrieve relevant memories for the same User ID.

---

# 👥 Multiple Users

User A:

```text
User ID: Ayushman
```

User B:

```text
User ID: Rahul
```

The application uses the User ID when searching and storing memories.

Therefore:

```text
Ayushman
   ↓
Ayushman's memories

Rahul
   ↓
Rahul's memories
```

---

# 🧩 System Responsibilities

The project separates responsibilities between different technologies.

```text
Streamlit
    ↓
User Interface

LangChain
    ↓
Prompt + LLM pipeline

Groq
    ↓
Interview response generation

Mem0
    ↓
Long-term memory

Gemini
    ↓
Memory extraction + embeddings

Qdrant
    ↓
Persistent vector storage
```

---

# 🔄 Memory Lifecycle

## 1. User asks a question

```text
"I am preparing for Python interviews."
```

## 2. Search existing memories

Mem0 searches for relevant memories associated with the User ID.

## 3. Generate response

Relevant memories are passed into the interview coach prompt.

## 4. Save conversation

The user and assistant messages are stored in Mem0.

## 5. Future conversations

The stored memories can be retrieved later and used to personalize responses.

---

# 🎯 Learning Outcomes

This project demonstrates practical usage of:

- Python
- Streamlit
- LangChain
- Groq
- Gemini
- Mem0
- Qdrant
- Vector databases
- Embeddings
- Prompt engineering
- Long-term AI memory
- Environment variables
- API security
- AI application architecture

---

# 📚 Concepts Learned

## LLM

A Large Language Model is used to generate natural-language responses.

---

## Prompt

The system prompt tells the AI how it should behave as an interview coach.

---

## Memory

Mem0 allows the application to remember useful information across conversations.

---

## Embeddings

Embeddings convert text into numerical vectors that represent semantic meaning.

---

## Vector Database

Qdrant stores and retrieves vectors so relevant memories can be found.

---

## Retrieval

The application retrieves relevant memories before generating the next response.

---

## User ID

The User ID separates memory contexts between users.

---

# 🏗️ Architecture Pattern

The project follows a memory-augmented LLM architecture:

```text
                ┌───────────────┐
                │     User      │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   Streamlit   │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Memory Search │
                │     Mem0      │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │    Qdrant     │
                │ Vector Store  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   Relevant    │
                │   Memories    │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   LangChain   │
                │ Prompt Chain  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Groq GPT-OSS  │
                │      20B      │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │  AI Response  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   Mem0.add()  │
                └───────────────┘
```

---

# 🚀 Future Improvements

Possible future improvements include:

- Resume upload
- Resume-based interview questions
- Interview difficulty selection
- Interview scoring
- Topic-wise performance
- Progress tracking
- Interview history
- Voice interview mode
- Authentication
- User dashboard
- Cloud deployment
- Hosted Qdrant
- Advanced agent workflows
- Better memory management
- Multiple interview modes
- Company-specific interview preparation

---

# ⭐ Project Summary

**AI Interview Prep Coach** is a memory-enabled AI assistant built using:

```text
LangChain
+
Groq
+
Mem0
+
Gemini
+
Qdrant
+
Streamlit
```

The project demonstrates how an LLM application can be combined with long-term memory and vector search to create a personalized interview preparation experience.

The most important feature is **User-ID-based persistent memory**, allowing the AI coach to remember useful information and use it in future conversations.

---

# 👨‍💻 Run the Project

```powershell
cd "C:\Users\Lenovo\Desktop\llm 24-07-2026\Mem 0\Model 2"
uv run streamlit run app.py
```

---

## ❤️ Built for Learning

This project was built as a hands-on learning project to understand:

**LLMs → LangChain → Memory → Embeddings → Vector Databases → AI Applications**



## 🚀 Try the Live Application

Want to use the AI Interview Prep Coach directly?

👉 **[Open AI Interview Prep Coach](https://mem0-ai-interview-coach-rffnahrwuk5bwrbwq2fjuk.streamlit.app)**

You don't need to install Python, clone the repository, or set up any API keys.

### How to Use

1. Open the live application using the link above.
2. Enter your **User ID / Name** in the sidebar.
3. Start chatting with the AI Interview Prep Coach.
4. Use the **same User ID** when you return so your stored memories can be retrieved.
5. Ask interview questions, share your preparation progress, weaknesses, or answer practice questions.

🧠 The application uses **Mem0 persistent memory** to remember relevant information about each user and personalize future conversations.

> **Note:** Use the same User ID each time if you want the application to retrieve your previous memories.
