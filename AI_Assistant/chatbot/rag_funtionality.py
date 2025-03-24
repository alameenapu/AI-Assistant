from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from decouple import config
import re

# Load API key
api_key = config("OPENAI_API_KEY")

# Embedding Function (only needed if creating new DB)
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Load existing Chroma DB (do NOT pass embedding_function here)
vector_db = Chroma(
    persist_directory="../vector_db",
    collection_name="friendship_ngo",
    embedding_function=embedding_function
)

# LLM setup
llm = ChatOpenAI(model="gpt-4o-mini",max_tokens=800, temperature=0.6, openai_api_key=api_key)  #max_tokens=300,

# Memory for chat history
memory = ConversationBufferMemory(
    return_messages=True, memory_key="chat_history"
)

# QA Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=vector_db.as_retriever(
        search_kwargs={"fetch_k": 10, "k": 8}, search_type="mmr"
    ),
    chain_type="stuff"
)

def rag_func(question:str) -> str:
    """
    This function takes in user question or prompt and returns a response
    :param: question: String value of the question or the prompt fom the user
    :response: String value of the answer to the user question.
    """
    response = qa_chain.invoke({"question": question})
    answer = response.get("answer")
    
    answer = re.sub(r"</?div>", "", answer)
    return answer


# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain.prompts import PromptTemplate
# from langchain.chains import ConversationalRetrievalChain
# from langchain_openai import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
# from decouple import config

# # Load API key
# api_key = config("OPENAI_API_KEY")

# # Embedding model
# embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# # Load existing Chroma DB
# vector_db = Chroma(
#     persist_directory="../vector_db",
#     collection_name="friendship_ngo",
#     embedding_function=embedding_function
# )

# # LLM setup
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     max_tokens=800,  # Increased for more flexibility
#     temperature=0.6,
#     openai_api_key=api_key
# )

# # Memory buffer
# memory = ConversationBufferMemory(
#     return_messages=True,
#     memory_key="chat_history"
# )

# # 🔥 Custom concise prompt template
# custom_prompt = PromptTemplate.from_template("""
# You are a helpful assistant for Friendship NGO.
# When answering a question, if you find additional related facts in the context, include them concisely even if not explicitly asked.
# Be clear, informative, but brief.
# Question: {question}
# Context: {context}
# Answer:
# """)

# # QA Chain with concise control
# qa_chain = ConversationalRetrievalChain.from_llm(
#     llm=llm,
#     memory=memory,
#     retriever=vector_db.as_retriever(
#         search_kwargs={"fetch_k": 4, "k": 3}, search_type="mmr"
#     ),
#     combine_docs_chain_kwargs={"prompt": custom_prompt}
# )

# # Final function to invoke
# def rag_func(question: str) -> str:
#     """
#     This function takes a user question and returns a concise response.
#     """
#     response = qa_chain.invoke({"question": question})
#     return response.get("answer")
