import custom_console
import sys
import os
from pathlib import Path

# Start main.py
custom_console.clear_console()
custom_console.start_process_timer()

# Unstructured Data
from llama_index.readers.file import UnstructuredReader
loader = UnstructuredReader()
years = [2022, 2021, 2020, 2019]
doc_set = {}
all_docs = []
for year in years:
    year_docs = loader.load_data(
        file=Path(f"./data/UBER/UBER_{year}.html"), split_documents=False
    )
    # insert year metadata into each year
    for d in year_docs:
        d.metadata = {"year": year}
    doc_set[year] = year_docs
    all_docs.extend(year_docs)

# initialize simple vector indices``
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core import Settings
import google_llm_init as google

Settings.chunk_size = 512
Settings.embed_model = GoogleGenAIEmbedding()
Settings.llm = google.llm

# Setup VectorStoreIndex, saving it to disk initially
print(f"{custom_console.COLOR_CYAN}Setting Up VectorStoreIndexes for UBER SEC Filings{custom_console.RESET_COLOR}")
# index_set = {}
# for year in years:
#     storage_context = StorageContext.from_defaults()
#     cur_index = VectorStoreIndex.from_documents(
#         doc_set[year],
#         storage_context=storage_context,
#     )
#     index_set[year] = cur_index
#     storage_context.persist(persist_dir=f"./storage/{year}")

# Load an Index from Disk
print(f"{custom_console.COLOR_YELLOW}Loaded UBER SEC files from VectorStoreIndex{custom_console.RESET_COLOR}")
index_set_2 = {}
for year in years:
    storage_context = StorageContext.from_defaults(
        persist_dir=f"./storage/{year}"
    )
    cur_index = load_index_from_storage(
        storage_context,
    )
    index_set_2[year] = cur_index

print(f"\n{custom_console.COLOR_MAGENTA}Vector Store Index: {custom_console.RESET_COLOR}")
print(index_set_2)

# Query Engine
individual_query_engine_tools = [
    QueryEngineTool(
        query_engine=index_set_2[year].as_query_engine(),
        metadata=ToolMetadata(
            name=f"vector_index_{year}",
            description=f"useful for when you want to answer queries about the {year} SEC 10-K for Uber",
        ),
    )
    for year in years
]

# Sub Question Query
query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=individual_query_engine_tools,
    llm=google.llm,
)
query_engine_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="sub_question_query_engine",
        description="useful for when you want to answer queries that require analyzing multiple SEC 10-K documents for Uber",
    ),
)

tools = individual_query_engine_tools + [query_engine_tool]

# Create Agent
import google_llm_init as google
from llama_index.core.agent.workflow import FunctionAgent
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# system_prompt.txt to be used for Agents' System Prompt.
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    loaded_system_prompt = f.read()
    # print(f"{loaded_system_prompt}\n")

workflow = FunctionAgent(
    tools=tools,
    llm=google.llm,
    system_prompt=loaded_system_prompt
)

async def main():
    custom_console.simple_initializer_spinner(3,"Initial Program Loading complete!")
    
    # print(google.llm.metadata)
    question = "What was Uber's best year revenue wise between 2019-2022?"
    response = await workflow.run(user_msg=question)
    print(f"{custom_console.COLOR_RED}~ Llama Chat Speaks!{custom_console.RESET_COLOR}\n")
    print(f"{custom_console.COLOR_YELLOW}Question:{custom_console.RESET_COLOR}")
    print(question)
    print(f"{custom_console.COLOR_YELLOW}\nAnswer{custom_console.RESET_COLOR}")
    print(response)

    # End Program
    custom_console.process_timer_elapsed_time_success()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
