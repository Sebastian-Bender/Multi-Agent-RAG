import chainlit as cl
import hashlib
from typing import List, Dict
import os
from pathlib import Path

from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessageChunk
from retriever.file_handler import DocumentProcessor
from retriever.builder import RetrieverBuilder
from agent.workflow import AgentWorkflow
from config import constants, settings
from utils.logging import logger

from dotenv import load_dotenv
load_dotenv()


# Initialize components
processor = DocumentProcessor()
retriever_builder = RetrieverBuilder()
workflow = AgentWorkflow()

state = {
    'retriever': None,
    'file_hashes': frozenset(),
}

def _get_file_hashes(uploaded_files: List) -> frozenset:
    """Generate SHA-256 hashes for uploaded files."""
    hashes = set()
    for file in uploaded_files:
        with open(file.path, "rb") as f:
            hashes.add(hashlib.sha256(f.read()).hexdigest())
    return frozenset(hashes)

@cl.on_chat_start
async def start():
    """Initialize the chat interface."""
    await cl.Message(
        content="Get accurate, varified answers to questions about you documents!\n\n"
                "**How it works:**\n"
                "1. 📤 Upload your document(s) (PDF, DOCX, TXT, MD)\n"
                "2. ❓ Ask your question\n"
                "3. 🚀 Get AI-powered answers with verification\n\n"
                "**Features:**\n"
                "• Multi-agent workflow for accurate answers\n"
                "• Document relevance checking\n"
                "• Answer verification and fact-checking\n"
                "• Support for multiple document formats\n\n"
                "Ready to start! Upload some documents or ask a question."
    ).send()



# Add example loading actions
@cl.on_chat_start
async def add_example_actions():
    uploaded_files = None

    # Wait for the user to upload a file
    while uploaded_files == None:
        uploaded_files = await cl.AskFileMessage(
            content="Please upload a text file to begin!", accept=constants.ALLOWED_TYPES
        ).send()

    chunks = processor.process(uploaded_files)
    current_hashes = _get_file_hashes(uploaded_files)
                
    if state["retriever"] is None or current_hashes != state["file_hashes"]:
        logger.info("Processing new/changed documents...")
        chunks = processor.process(uploaded_files)
        retriever = retriever_builder.build_hybrid_retriever(chunks)
        
        state.update({
            "file_hashes": current_hashes,
            "retriever": retriever
        })
    # Let the user know that the system is ready
    await cl.Message(
        content="Files uploaded! Start chat now!"
    ).send()


@cl.on_message
async def main(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    answer = cl.Message(content="")

    if len(msg.elements) > 0:
        uploaded_files = msg.elements
        chunks = processor.process(uploaded_files)
        current_hashes = _get_file_hashes(uploaded_files)
                    
        if state["retriever"] is None or current_hashes != state["file_hashes"]:
            logger.info("Processing new/changed documents...")
            chunks = processor.process(uploaded_files)
            retriever = retriever_builder.build_hybrid_retriever(chunks)
            
            state.update({
                "file_hashes": current_hashes,
                "retriever": retriever
            })

    initial_state = workflow.prepare_initial_state(question=msg.content, retriever=state["retriever"])
    
    for chunk in workflow.compiled_workflow.stream(initial_state, stream_mode="messages", subgraphs=True, config=RunnableConfig(callbacks=[cb], **config)):
            msg, metadata = chunk[1]
            if isinstance(msg, AIMessageChunk):
                await answer.update()
            if (
                metadata["langgraph_node"] == "final_node"
            ):
                answer.content += msg.content 
                await answer.update()

    await answer.send()




