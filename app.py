"""
Streamlit UI for the Mem0 + LangChain interview prep assistant.
"""

import streamlit as st

from memory_agent import (
    chat,
    get_all_memories,
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="AI Interview Prep Coach",
    page_icon="🧠",
    layout="wide",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main title */

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 25px;
    }


    /* Chat input */

    div[data-testid="stChatInput"] {
        background: transparent !important;
    }

    div[data-testid="stChatInput"] > div {
        background: white !important;
        border-radius: 14px !important;
        border: 1px solid #777 !important;
    }

    textarea[data-testid="stChatInputTextArea"] {
        background: white !important;
        color: #111 !important;
        caret-color: #111 !important;
        border: none !important;
        box-shadow: none !important;
    }

    textarea[data-testid="stChatInputTextArea"]::placeholder {
        color: #666 !important;
        opacity: 1 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Session")

    user_id = st.text_input(
        "User ID",
        value="",
        placeholder="Enter your name",
    )

    user_id = user_id.strip()

    st.markdown("---")


    # --------------------------------------------------------
    # SHOW MEMORIES
    # --------------------------------------------------------

    if st.button(
        "🧠 Show stored memories",
        use_container_width=True,
    ):

        if not user_id:

            st.warning(
                "Please enter your User ID first."
            )

        else:

            memories = get_all_memories(
                user_id
            )

            if memories.get("error"):

                st.error(
                    memories["error"]
                )

            else:

                results = memories.get(
                    "results",
                    []
                )

                if not results:

                    st.info(
                        "No stored memories yet."
                    )

                else:

                    st.write(
                        "### 🧠 Stored Memories"
                    )

                    for item in results:

                        if isinstance(
                            item,
                            dict
                        ):

                            memory = item.get(
                                "memory"
                            )

                            if memory:

                                st.write(
                                    f"• {memory}"
                                )


    st.markdown("---")


    # --------------------------------------------------------
    # CLEAR TRANSCRIPT
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear transcript",
        use_container_width=True,
    ):

        st.session_state.pop(
            "messages",
            None
        )

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🧠 AI Interview Prep Coach
    </div>

    <div class="subtitle">
        Powered by LangChain + Mem0 + Groq —
        remembers you across sessions.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# DISPLAY CHAT
# ============================================================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.markdown(
            msg["content"]
        )


# ============================================================
# INPUT
# ============================================================

user_input = st.chat_input(
    "Tell me about your prep, or answer my question..."
)


# ============================================================
# CHAT
# ============================================================

if user_input:

    if not user_id:

        st.warning(
            "Please enter your User ID first."
        )

        st.stop()


    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )


    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    # --------------------------------------------------------
    # AI
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            reply = chat(
                user_id=user_id,
                user_message=user_input,
            )


        st.markdown(
            reply
        )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )