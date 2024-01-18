import os
import re
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

llm = HuggingFaceHub(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    model_kwargs={
        "temperature": 0.75,
        "max_length": 500, 
    }
)

def get_links():
    with open("../data/links.txt", "r", encoding="utf-8") as file:
        data = file.read()
    
    lines = data.strip().split('\n')

    places_template = {}
    for line in lines:
        parts = re.split(r':\s*', line, maxsplit=1)
        if len(parts) == 2:
            place = parts[0].strip()
            link = parts[1].strip()
            places_template[place] = link

    return places_template  

def find_places_and_links(text, places):
    results = {}
    
    for place, link in places.items():
        pattern = re.compile(fr'\b{place}\b', flags=re.IGNORECASE)
        matches = pattern.findall(text)
        
        if matches:
            results[place] = link
    
    return results

reviews_file_path = "../data/data.txt"
with open(reviews_file_path, "r", encoding="utf-8") as file:
    reviews = file.read().splitlines()

loader = TextLoader(reviews_file_path)
pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=511,
    chunk_overlap=100,
    separators=['\n\n', '\n', '(?<=\. )', ' ', '']
)
docs = text_splitter.split_documents(pages)

embeddings = HuggingFaceEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()
chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

def get_response_from_model(question: str):
    generated_response = chain({"query": question})
    question_index = generated_response["result"].find("Question:") or generated_response["result"].find("Answer:") or generated_response["result"].find("Helpful Answer:") or generated_response["result"].find("Recommended Restaurant:") 
    if question_index != -1:
        answer = generated_response["result"][:question_index].strip()
    else:
        answer = generated_response["result"]

    places = get_links()
    links = find_places_and_links(answer, places)
    if links:
        output_list = [f'Location:']

        for place, link in links.items():
            output_list.append(f'{place}: {link}')

    return answer + '\n'.join(output_list)