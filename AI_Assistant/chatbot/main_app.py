import streamlit as st
from rag_funtionality import rag_func
from datetime import datetime

# --- Setup ---
st.set_page_config(page_title="Friendship AI Assistant", layout="wide")

# Custom logo/icon path
BOT_ICON = "assets/FRN_Logo.jpg"
USER_ICON = "https://cdn-icons-png.flaticon.com/512/1077/1077012.png"

# --- Chat history state ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello there, Welcome to Friendship. How can I help you today?",
            "time": datetime.now().strftime("%I:%M %p")
        }
    ]

# --- Render Chat Message ---
def render_message(role, content, time=None):
    with st.container():
        cols = st.columns([1, 12])
        bubble_color = "#e6f0ff" if role == "assistant" else "#cceeff"
        name_color = "#0033cc" if role == "assistant" else "#004466"
        name_label = "Friendship AI Assistant" if role == "assistant" else "You"
        avatar = BOT_ICON if role == "assistant" else USER_ICON

        with cols[0]:
            st.image(avatar, width=40)
        with cols[1]:
            st.markdown(
                f"""
                <div style='padding: 12px 18px; background-color: {bubble_color}; border-radius: 12px;
                            color: #000000; font-size: 16px; margin-bottom: 12px; position: relative;'>
                    <strong style="color:{name_color};">{name_label}:</strong><br>
                    {content}
                    {"<div style='font-size:12px; color:#777; margin-top:4px; text-align:right;'>"+time+"</div>" if time else ""}
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Display Messages ---
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"], msg.get("time"))
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

# --- Chat Input ---
user_input = st.chat_input("Type your message here...")

if user_input:
    now = datetime.now().strftime("%I:%M %p")

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input, "time": now})
    render_message("user", user_input, now)

    # Bot response
    with st.spinner("Friendship AI is thinking..."):
        response = rag_func(user_input)
        now_bot = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({"role": "assistant", "content": response, "time": now_bot})
        render_message("assistant", response, now_bot)




# import streamlit as st
# from rag_funtionality import rag_func

# # --- Setup ---
# st.set_page_config(page_title="Friendship AI Assistant", layout="wide")

# # Custom logo/icon path (make sure this file exists)
# BOT_ICON = "assets/FRN_Logo.jpg"  # Your custom assistant icon
# USER_ICON = "https://cdn-icons-png.flaticon.com/512/1077/1077012.png"  # Generic user avatar (can change this too)

# # --- Chat history state ---
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Hello there, Welcome to Friendship. How can I help you today?"}
#     ]

# # --- Custom Chat Message Renderer ---

# def render_message(role, content):
#     with st.container():
#         cols = st.columns([1, 12])
#         if role == "assistant":
#             with cols[0]:
#                 st.image(BOT_ICON, width=40)
#             with cols[1]:
#                 st.markdown(
#                     f"""
#                     <div style='padding: 12px 18px; background-color: #e6f0ff; border-radius: 12px; color: #000000; font-size: 16px; margin-bottom: 12px;'>
#                         <strong style="color:#0033cc;">Friendship AI Assistant:</strong><br>{content}
#                     </div>
#                     """,
#                     unsafe_allow_html=True
#                 )
#         elif role == "user":
#             with cols[0]:
#                 st.image(USER_ICON, width=40)
#             with cols[1]:
#                 st.markdown(
#                     f"""
#                     <div style='padding: 12px 18px; background-color: #cceeff; border-radius: 12px; color: #000000; font-size: 16px; margin-bottom: 24px;'>
#                         <strong style="color:#004466;">You:</strong><br>{content}
#                     </div>
#                     """,
#                     unsafe_allow_html=True
#                 )


# # --- Display all messages ---
# for msg in st.session_state.messages:
#     render_message(msg["role"], msg["content"])
#     st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# # --- Chat Input ---
# user_input = st.chat_input("Type your message here...")

# if user_input:
#     # Add user message
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     render_message("user", user_input)

#     # Add bot response
#     with st.spinner("Thinking..."):

#         response = rag_func(user_input)
#     st.session_state.messages.append({"role": "assistant", "content": response})
#     render_message("assistant", response)
