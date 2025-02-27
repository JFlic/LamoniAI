from typing import List

import lancedb
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector

import os
import time
import lancedb
from langchain_community.vectorstores import LanceDB

from langchain_community.llms import HuggingFaceHub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import LanceDB
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, DirectoryLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Create a LanceDB database
db = lancedb.connect("data/lancedb")
print(db)

# Specify Embedding Model
embedding_model_name = 'BAAI/bge-m3'
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name, model_kwargs={'device': 'gpu'})
