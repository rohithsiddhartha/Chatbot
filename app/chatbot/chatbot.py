import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ConversationBufferMemory


def create_vector_store(text):
    """
    Create a vector store from the provided text chunks.
    
    Args:
        text (str): The input text to be split and embedded.

    Returns:
        FAISS: A vector store with embedded text chunks.
    """
    embeddings = OpenAIEmbeddings()
    text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def get_relevant_context(vector_store, question, k=3):
    """
    Retrieve relevant context from the vector store based on the question.
    
    Args:
        vector_store (FAISS): The vector store to search.
        question (str): The query to retrieve relevant documents.
        k (int): The number of relevant documents to retrieve (default is 3).

    Returns:
        str: Concatenated relevant document content.
    """
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    # retriever = vector_store.as_retriever()
    # docs = retriever.get_relevant_documents(question)
    docs = retriever.invoke(question)
    return " ".join([doc.page_content for doc in docs])


def create_chat_prompt_template():

    return ChatPromptTemplate.from_messages([
    ("system", """You are an intelligent assistant designed to guide users through the necessary steps to successfully accomplish their tasks. You have access to a comprehensive database that contains detailed instructions, solutions, and resources.

    When responding to a user's question:
    1. First, confirm whether the task can be accomplished and provide a brief explanation of why it can or cannot be done. Highlight any key benefits or advantages of the task if it is possible.
    2. After the initial response, ask the user if they would like to proceed with detailed instructions or if they need any additional support.

    Throughout your interactions, ensure that your instructions are clear and actionable. Be supportive and offer additional tips or advice if needed. If the user's question requires multiple steps or options, break down the information into manageable parts, guiding them through each step until they achieve their goal.

    Summary: {summary}

    Database Input: {context}
    """),
    ("human", "{input}"),
])


def setup_rag_with_history(vector_store, summary):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    prompt = create_chat_prompt_template()
    retrieval_chain = create_retrieval_chain(vector_store.as_retriever(), create_stuff_documents_chain(llm, prompt))

    return {"chain": retrieval_chain, "memory": memory, "vector_store": vector_store, "summary": summary}


def get_response(qa_system, question):

    if question.lower() == "reset":
        qa_system["memory"].clear()
        return "Chat history has been reset."

    context = get_relevant_context(qa_system["vector_store"], question)
    
    response = qa_system["chain"].invoke({
        "summary": qa_system["summary"],
        "input": question,
        "context": context,
        "chat_history": qa_system["memory"].chat_memory.messages
    })

    qa_system["memory"].chat_memory.add_user_message(question)
    qa_system["memory"].chat_memory.add_ai_message(response["answer"])
    
    return response["answer"]
    


if __name__ == "__main__":
    with open('collated_text.txt', 'r') as file:
        extracted_info = file.read()
    
    with open('summary.txt', 'r') as file:
        summary = file.read()

    # Create vector store
    vector_store = create_vector_store(extracted_info)

    # Setup RAG system with chat history
    qa_system = setup_rag_with_history(vector_store, summary)

    # Example conversation loop
    while True:
        user_question = input("Ask a question (or type 'exit' to quit) (or 'reset' to restart the chat without any history): ")
        if user_question.lower() == 'exit':
            break
        response = get_response(qa_system, user_question)
        print(f"Response: {response}\n")


