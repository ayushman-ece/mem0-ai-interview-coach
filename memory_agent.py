import atexit
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

GROQ_MODEL = "openai/gpt-oss-20b"


# ============================================================
# ENVIRONMENT
# ============================================================

os.environ.setdefault(
    "MEM0_DIR",
    str(PROJECT_ROOT / ".mem0")
)

os.environ.setdefault(
    "MEM0_TELEMETRY",
    "False"
)

load_dotenv(
    dotenv_path=PROJECT_ROOT / ".env"
)


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


if not GROQ_API_KEY:
    raise RuntimeError(
        f"GROQ_API_KEY not found.\n"
        f"Check: {PROJECT_ROOT / '.env'}"
    )


if not GOOGLE_API_KEY:
    raise RuntimeError(
        f"GOOGLE_API_KEY not found.\n"
        f"Check: {PROJECT_ROOT / '.env'}"
    )


# ============================================================
# MEM0
# ============================================================

from mem0 import Memory


MEM0_CONFIG = {

    # Gemini handles Mem0 memory extraction
    # so Groq's 8K TPM limit does not affect Mem0.
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-3.5-flash-lite",
            "api_key": GOOGLE_API_KEY,
            "temperature": 0.1,
            "max_tokens": 256,
        },
    },

    # Gemini embeddings
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "models/gemini-embedding-001",
            "embedding_dims": 768,
            "api_key": GOOGLE_API_KEY,
        },
    },

    # Persistent Qdrant database
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "mem0_interview_prep",
            "embedding_model_dims": 768,
            "path": str(
                PROJECT_ROOT / "qdrant_data"
            ),
        },
    },
}


# ============================================================
# INTERVIEW COACH PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an AI interview prep coach.

Use the following memories about the candidate
to personalize your questions and feedback.

Avoid repeating topics already covered.

Focus on weak areas and the candidate's target role.

Be specific and concise.

Candidate memories:
{memories}

User request:
{question}
"""


# ============================================================
# LANGCHAIN + GROQ
# ============================================================

CHAIN = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT
            ),
            (
                "human",
                "{question}"
            ),
        ]
    )

    | ChatGroq(
        model=GROQ_MODEL,
        temperature=0.3,
        api_key=GROQ_API_KEY,
        max_tokens=400,
    )

    | StrOutputParser()
)


# ============================================================
# INITIALIZE MEM0
# ============================================================

try:

    MEMORY = Memory.from_config(
        MEM0_CONFIG
    )

    MEMORY_INIT_ERROR = None

except Exception as exc:

    MEMORY = None
    MEMORY_INIT_ERROR = exc


# ============================================================
# FORMAT MEMORIES
# ============================================================

def _format_memories(search_results):

    if isinstance(search_results, dict):

        items = search_results.get(
            "results",
            []
        )

    else:

        items = search_results


    memories = []

    for item in items:

        if isinstance(item, dict):

            memory = item.get(
                "memory"
            )

            if memory:

                memories.append(
                    f"- {memory}"
                )


    if not memories:

        return "(no prior memories yet)"


    return "\n".join(
        memories[:5]
    )


# ============================================================
# CLOSE MEMORY
# ============================================================

def _close_memory():

    global MEMORY

    if MEMORY is None:
        return

    try:

        MEMORY.vector_store.client.close()

    except Exception:
        pass

    try:

        MEMORY.close()

    except Exception:
        pass


atexit.register(
    _close_memory
)


# ============================================================
# CHAT
# ============================================================

def chat(
    user_id: str,
    user_message: str
) -> str:

    if MEMORY is None:

        return (
            "Setup error: could not initialize Mem0.\n\n"
            f"{MEMORY_INIT_ERROR}"
        )


    user_id = user_id.strip()
    user_message = user_message.strip()


    if not user_id:

        return "Please enter your User ID first."


    if not user_message:

        return "Please enter a message."


    try:

        # ----------------------------------------------------
        # SEARCH USER MEMORY
        # ----------------------------------------------------

        search_results = MEMORY.search(
            query=user_message,
            filters={
                "user_id": user_id
            },
            limit=5,
        )


        memories = _format_memories(
            search_results
        )


        # ----------------------------------------------------
        # ASK GROQ
        # ----------------------------------------------------

        reply = CHAIN.invoke(
            {
                "memories": memories,
                "question": user_message,
            }
        )


        # ----------------------------------------------------
        # SAVE CONVERSATION TO MEM0
        # ----------------------------------------------------

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


        return reply


    except Exception as exc:

        return f"Setup error: {exc}"


# ============================================================
# GET ALL MEMORIES
# ============================================================

def get_all_memories(user_id: str):

    if MEMORY is None:

        return {
            "error": str(
                MEMORY_INIT_ERROR
            ),
            "results": [],
        }


    try:

        # IMPORTANT:
        # Current Mem0 version requires filters.
        return MEMORY.get_all(
            filters={
                "user_id": user_id
            }
        )


    except Exception as exc:

        return {
            "error": str(exc),
            "results": [],
        }