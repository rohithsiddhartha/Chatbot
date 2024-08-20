import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from langchain import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

from langchain_core.output_parsers import JsonOutputParser

from pydantic import BaseModel
import inspect

os.environ["OPENAI_API_KEY"] = "sk-"

INFORMATION_EXTRACTION_PROMPT = inspect.cleandoc(""" Given the following raw text extracted from a website, transform the content into a well-organized and concise format that retains all essential information. Ensure the output is structured in a way that can be easily utilized for tasks such as data analysis, presentation, or further processing by a personal assistant. Highlight key points, maintain accuracy, and eliminate unnecessary details. The final output should be clear, actionable, and optimized for readability. Ouptut doesn't have to follow the exact format of the example but adhere to the instructions given

Specific Instructions:
Input: Raw text data scraped from a webpage.
Output: A structured formatted text, optimized for clarity and further usage.
Objective: Ensure no loss of critical information while making the content easily digestible.
                                                 
                                                 
Here's the input web scraped text: {scraped_text}

Important:
- Ensure that the output is well-structured and easy to understand.
- Highlight key features, benefits, and the problem addressed.
- Maintain the essence of the content while eliminating unnecessary details.
- The output should be concise and optimized for readability.
- The final text should be actionable and informative.
                                                 
""")

class Parsermodel(BaseModel):
    clean_text: str

def create_prompt():
    parser = JsonOutputParser(pydantic_object=Parsermodel)
    prompt = PromptTemplate(
        input_variables=["scraped_text"],
        template=INFORMATION_EXTRACTION_PROMPT,
        # partial_variables = {"format_instructions": parser.get_format_instructions()}
    )
    return prompt


def execute_prompt(prompt, text):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(text)

def summarize_text(text):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(llm, chain_type="refine")
    return chain.run(docs)

def process_files(folder_path):
    prompt = create_prompt()
    all_extracted_info = ""

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                extracted_info = execute_prompt(prompt, content)
                all_extracted_info += f"\nExtracted from {filename}:\n{extracted_info}\n"
                print(f"Processed: {filename}")

    return all_extracted_info


if __name__ == "__main__":
    folder_path = "text"  

    # Generate summary of all extracted information
    with open('collated_text.txt', 'r') as file:
        all_extracted_info = file.read()
    print(all_extracted_info)
    
    summary = summarize_text(all_extracted_info)
    print("\nOverall Summary:")
    print(summary)

    
    with open("summary.txt", "w", encoding="utf-8") as file:
        file.write(summary)