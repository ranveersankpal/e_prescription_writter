import os
import tempfile
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredExcelLoader,
    UnstructuredWordDocumentLoader
)

async def extract_text_from_document(file):
    suffix = file.filename.split(".")[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    try:
        if suffix == "pdf":
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
            text = "\n".join([doc.page_content for doc in docs])

        elif suffix in ["xlsx", "xls"]:
            loader = UnstructuredExcelLoader(temp_path)
            docs = loader.load()
            text = "\n".join([doc.page_content for doc in docs])

        elif suffix == "docx":
            loader = UnstructuredWordDocumentLoader(temp_path)
            docs = loader.load()
            text = "\n".join([doc.page_content for doc in docs])

        else:
            raise ValueError("Only PDF, Excel, and Word (.docx) files are supported")

    finally:
        os.remove(temp_path)

    return text.strip()
