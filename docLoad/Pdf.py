from langchain_community.document_loaders import PyPDFLoader
from langchain_unstructured import UnstructuredLoader

file_path = (
    "C:\\Users\\HP280\\Desktop\\test.pdf"
)

import asyncio

async def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = []

    # 使用 async for 迭代异步生成器
    async for page in loader.alazy_load():
        pages.append(page)

    # 输出第一页面的 metadata 和 content
    if pages:
        print(f"{pages[0].metadata}\n")
        print(pages[0].page_content)

# 使用 asyncio.run 来运行异步函数
asyncio.run(load_pdf(file_path))



loader = UnstructuredLoader(
    file_path=file_path,
    strategy="hi_res",
    partition_via_api=True,
    coordinates=True,
)
docs = []
for doc in loader.lazy_load():
    docs.append(doc)



