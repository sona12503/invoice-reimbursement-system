from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA


embedding_model = OpenAIEmbeddings()
llm = ChatOpenAI(temperature=0)

def query_chatbot(user_query, vector_store_path="faiss_index"):
    # Load saved FAISS index
    vectorstore = FAISS.load_local(vector_store_path, embedding_model)
    retriever = vectorstore.as_retriever()
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    response = qa_chain.run(user_query)
    return response
