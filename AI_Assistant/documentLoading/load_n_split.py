import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma  # ✅ Reliable and still supports persist()

# PDF file path
FILE_PATH = r"D:\Drive\Chatbot\documnets\FriendshipSecondaryHealthCamp.pdf"
persist_directory = r"D:\Drive\Chatbot\vector_db"
collection_name = "friendship_ngo"

# Check if file exists
if not os.path.exists(FILE_PATH):
    print(f"❌ Error: File not found at {FILE_PATH}")
else:
    print(f"📄 File found at: {FILE_PATH}")

    try:
        # Load and split PDF into pages
        loader = PyPDFLoader(FILE_PATH)
        pages = loader.load_and_split()
        print(f"📄 Total Pages Loaded: {len(pages)}")

        # Embedding function
        embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

        # Create vector database
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_function,
            collection_name=collection_name
        )

        # Add new documents
        print("📦 Total documents before:", len(vectordb.get()['documents']))
        vectordb.add_documents(pages)
        vectordb.persist()
        print("📦 Total documents after:", len(vectordb.get()['documents']))
        print("✅ Vector DB created and persisted successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
