
from dataclasses import dataclass
from langchain_community.utilities import GoogleSerperAPIWrapper
import os
import chromadb
import requests
import tarfile
import shutil
import re
from pathlib import Path
from llama_index import download_loader
from llama_index import VectorStoreIndex, StorageContext, load_index_from_storage
from interpreter import interpreter
from serpapi import GoogleSearch
from tavily import TavilyClient
from gpt_researcher import GPTResearcher
import asyncio
from bs4 import BeautifulSoup
import fitz


# This is the dataclass that defines a tool
@dataclass
class Tool:
    name: str
    description: str
    tool_input: dict
    return_value: str
    function: callable


# Tools are defined here
def hello(name):
    return f"Hello, {name}!"

def goodbye_world(name):
    return f"Goodbye, {name}!"

# def search_google(query):
#     searcher = GoogleSerperAPIWrapper()
#     return searcher.run(query)

async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type, config_path=os.environ["GPT_RESEARCHER_CONFIG_PATH"])
    report = await researcher.run()
    return report

def web_research(query):
    report = asyncio.run(get_report(query=query, report_type="research_report"))
    return report

def web_search_to_get_url(query):
    tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    # For basic search:
    response = tavily.search(query=query, max_results=1)
    # Get the search results as context to pass an LLM:
    urls = [result["url"] for result in response["results"]]
    # You can also get a simple answer to a question including relevant sources all with a simple function call:
    # tavily.qna_search(query=query)
    return urls

# TODO: GPTResearcher が強そうなので、とりあえずそれを使う
# def web_search(query):
#     tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
#     # For basic search:
#     response = tavily.search(query=query)
#     # Get the search results as context to pass an LLM:
#     context = [{"url": obj["url"], "content": obj["content"]} for obj in response.results]
#     # You can also get a simple answer to a question including relevant sources all with a simple function call:
#     # tavily.qna_search(query=query)
#     return context
def read_file(file_name, work_dir = "./", **kwargs):
    try:
        with open(os.path.join(work_dir, file_name), "r") as f:
            content = f.read()
        return content
    except:
        print(f"cannot read file {file_name}")

def fetch_text_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # コンテンツタイプをチェックして、PDF か HTML か判断
        content_type = response.headers.get('Content-Type')
        if 'application/pdf' in content_type:
            # PDF からテキストを抽出
            with fitz.open(stream=response.content, filetype="pdf") as doc:
                text = ''
                for page in doc:
                    text += page.get_text()
        elif 'text/html' in content_type:
            # HTML をパースしてテキストを抽出
            soup = BeautifulSoup(response.content, 'html.parser')
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()
            text = soup.get_text(separator='\n', strip=True)
        else:
            return "Unsupported content type"
        
        return text
    except requests.RequestException as e:
        return f"Error: {e}"

def write_file(file_name, content, work_dir = "./", **kwargs):
    try:
        with open(os.path.join(work_dir, file_name), "w") as f:
            f.write(content)
        observation = f"File {file_name} written successfully."
        return observation
    except:
        print(f"cannot write file {file_name}")

def write_python_file(file_name, content, work_dir = "./", **kwargs):
    try:
        with open(os.path.join(work_dir, file_name), "w") as f:
            f.write(content)
        os.chmod(os.path.join(work_dir, file_name), 0o755)
        observation = f"File {file_name} written successfully."
        return observation
    except:
        print(f"cannot write file {file_name}")

def search_papers(query):
    chroma_client = chromadb.PersistentClient(path=os.environ["ARXIV_PAPER_DATABASE_DIR"])  # /auto-agent/database
    collection = chroma_client.get_collection(name="arxiv_papers")
    results = collection.query(
        query_texts=[query],
        n_results=1
    )
    # Download the papers
    for paper_id in results['ids'][0]:
        _download_paper_pdf(paper_id)
        # try:
        #     _download_paper_latex(paper_id)
        # except:
        #     print(f"cannot download latex file of {paper_id}")
    # Return the data
    data = {
        "ids": results['ids'][0],
        "abstracts": results['documents'][0]
    }
    return data

def _download_paper_pdf(paper_id, path="/auto-agent/database/papers/"):
    # Download the papers
    url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    response = requests.get(url)
    filename = f"{paper_id}.pdf"
    with open(path + filename, 'wb') as f:
        f.write(response.content)
    print(f"Papers downloaded successfully to /auto-agent/database/papers/.")

# https://github.com/auto-res/arxiv-source/blob/main/src/arxiv_source/arxiv.py
def _download_paper_latex(paper_id, path="/auto-agent/database/papers/"):
    # Create a temporary directory
    tmp_dir = path + 'tmp/'
    os.makedirs(tmp_dir, exist_ok=True)
    os.chdir(tmp_dir)

    # Download the source files
    url = f"https://arxiv.org/e-print/{paper_id}"
    response = requests.get(url)
    filename = f"{paper_id}.tar.gz"
    with open(filename, 'wb') as f:
        f.write(response.content)

    # Extract the source files
    with tarfile.open(filename, 'r:gz') as tar:
        tar.extractall()

    # Move the .tex file to the papers directory
    tex_files = [file for file in os.listdir(tmp_dir) if file.endswith('.tex')]
    if len(tex_files) == 0:
        print("No .tex files found.")
    elif len(tex_files) > 1:
        print("Multiple .tex files found. Skipping.")
    else:
        print(f"Found one .tex file: {tex_files[0]}")
    os.rename(tmp_dir + tex_files[0], path + tex_files[0])

    # Remove the temporary directory
    shutil.rmtree(path + 'tmp')

    # Change the working directory back to the working directory
    os.chdir("/auto-agent")

    print(f"Papers downloaded successfully to /auto-agent/database/papers/.")

def anwer_question_from_paper(**kwargs):
    new_index=True
    query = kwargs["query"]
    index = kwargs["index"]
    path=f"/auto-agent/database/papers/{index}.pdf"

    if new_index:  # TODO: implement the way to save the index
        PDFReader = download_loader("PDFReader")

        loader = PDFReader()
        documents = loader.load_data(file=Path(path))
        # インデックスの作成
        index = VectorStoreIndex.from_documents(documents)

        # インデックスの保存
        index.storage_context.persist()
    else:
        # インデックスの読み込み
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)

    # クエリエンジンの作成
    query_engine = index.as_query_engine()

    return query_engine.query(query).response

def run_open_interpreter(command):
    prompt = f"Execute `{command}` on local computer"
    interpreter.auto_run = True
    interpreter.force_task_completion = True
    dialogues = interpreter.chat(prompt)
    # assistant の role を持つ辞書の content を抽出して結合する
    assistant_contents = "\n\n".join(
        [dialogue['content'] for dialogue in dialogues if dialogue['role'] == 'assistant']
        )
    return assistant_contents


# This is the list of tools that will be used by the agent
tools = [
    # Tool(
    #     name="Hello",
    #     description="Say hello to somebody",
    #     tool_input={
    #         "name": "Name to be said hello to"
    #     },
    #     return_value="The observatioon will be a string of the form 'Hello, {name}!'",
    #     function=hello
    # ),
    # Tool(
    #     name="Goodbye",
    #     description="Say goodbye to somebody",
    #     tool_input={
    #         "name": "Name to be said goodbye to"
    #     },
    #     return_value="The observatioon will be a string of the form 'Goodbye, {name}!'",
    #     function=goodbye_world
    # ),
    # TODO: 一度の検索で有益な情報をとってこれることはまだ難しいので、もう少し研究が進んだら実装する
    # Tool(
    #     name="Google Search",
    #     description="Search Google for a query. Use this tool when you need to get the gneneral information about a topic. Use this only when it's really necessary.",
    #     tool_input={
    #         "query": "Query to be searched for"
    #     },
    #     return_value="The observation will be an answer to the query in the form of a string",
    #     function=search_google
    # ),
    Tool(
        name="Read File",
        description="Read a file from the current working directory",
        tool_input={
            "file_name": "Name of the file to be read"
        },
        return_value="The observation will be the content of the file",
        function=read_file
    ),
    Tool(
        name="Write File",
        description="Write a file to the current working directory",
        tool_input={
            "file_name": "Name of the file to be written",
            "content": "Content of the file to be written"
        },
        return_value="The observation will be a string of the form 'File {file_name} written successfully.'",
        function=write_file
    ),
    Tool( 
        name="Write Python File",
        description="This tool create a python file. Use this to create any tool.",
        tool_input={
            "file_name": "Name of the file to be written with .py extension",
            "content": "Python code to be written in the file"
        },
        return_value="The observation will be a string of the form 'File {file_name} written successfully.'",
        function=write_python_file
    ),
    # TODO: とってきた論文を有効活用できることはまだ難しいので、もう少し研究が進んだら実装する、最低限プランニングの段階に限定するなどする
    # Tool(
    #     name="Search Papers",
    #     description="Search the arXiv database for papers. Use this tool when you need to know the existing research on a topic, or when you need to find an expertise knowledge on this topic.",
    #     tool_input={
    #         "query": "Query to be searched for"
    #     },
    #     return_value="The observation will be a dictionary like string of the form {'ids': [id1, id2, ...], 'abstracts': [abstract1, abstract2, ...]} and the pdf and tex file of papers will be downloaded to /auto-agent/database/papers/",
    #     function=search_papers
    # ),
    # Tool(
    #     name="Answer Question from Paper",
    #     description="Answer a question from a paper saved in as /auto-agent/database/papers/{index}.pdf",
    #     tool_input={
    #         "query": "Query to be answered",
    #         "index": "arxiv index of the arxiv paper to be read"
    #     },
    #     return_value="The observation will be a dictionary like string of the form {'ids': [id1, id2, ...], 'abstracts': [abstract1, abstract2, ...]}",
    #     function=anwer_question_from_paper
    # ),
    # TODO: Python コマンドの実行とか、個別でツールとして用意した方がいいかもだけど、自動デバッグしてくれるので一旦 interpreter を使う
    Tool(
        name="Run Open Interpreter",
        description="Use this to run a command in the terminal, e.g. to run a python script, to run a shell command, or to run a command line tool.",
        tool_input={
            "command": "Command to be run in the terminal"
        },
        return_value="The observation will be a string of the outcome of the command",
        function=run_open_interpreter
    ),
    Tool(
        name="Web Research Report",
        description="Use this tool to do web research on query and get a summary report with source urls. Use this only when it's really necessary.",
        tool_input={
            "query": "Query to be researched on the web. Do not pass URL."
        },
        return_value="The observation will be a report on the query",
        function=web_research
    ),
    # Tool(
    #     name="Web Search with URL",
    #     description="Use this tool to search the web for a query and get a list of results with URLs. Use this only when it's really necessary.",
    #     tool_input={
    #         "query": "Query to be searched for"
    #     },
    #     return_value="The observation will be a list of search results with URLs",
    #     function=web_search_to_get_url
    # ),
    # Tool(
    #     name="Fetch Text from URL",
    #     description="Use this tool to fetch the text from a URL. Use this only when it's really necessary.",
    #     tool_input={
    #         "url": "URL to be fetched"
    #     },
    #     return_value="The observation will be the text fetched from the URL",
    #     function=fetch_text_from_url
    # )
]
