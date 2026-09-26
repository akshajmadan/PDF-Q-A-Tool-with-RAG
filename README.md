PDF Q&A Tool

A command-line tool that lets you ask questions about a PDF document and get answers grounded in its actual content, using a Retrieval-Augmented Generation (RAG) pipeline.

What it does

Instead of pasting an entire PDF into a prompt (which breaks on long documents and wastes tokens), this tool:

. Extracts text from a PDF
. Splits it into chunks
. Converts each chunk into an embedding (a numeric representation of its meaning)
. When you ask a question, embeds the question too and finds the chunk(s) most similar in meaning
. Sends only that relevant chunk + your question to an LLM (via Groq) to generate a grounded answer
. If no chunk is similar enough to the question, it tells you the question doesn't seem related to the document instead of guessing

This is the same core architecture behind most "chat with your document" products.

Tech stack
. pypdf — PDF text extraction
. sentence-transformers (all-MiniLM-L6-v2) — local, free embedding model
. Groq API (openai/gpt-oss-120b) — LLM for generating the final answer
. numpy / torch — similarity comparison between embeddings
Setup
Clone this repo and navigate into it:
   git clone https://github.com/yourusername/pdf-qa-tool.git
   cd pdf-qa-tool
Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
Install dependencies:
   pip install -r requirements.txt
Create a .env file in the project root with your Groq API key:
   GROQ_API_KEY=your_key_here

Get a free key at console.groq.com.

Place a PDF in the project folder and update the filename in main.py if needed.
Usage
python main.py

You'll be prompted to enter a question. The tool will retrieve the most relevant section of the PDF and generate an answer based on it.

How it works (in more detail)
Chunking: the extracted text is split into fixed-size word chunks (500 words) to keep each piece small enough for accurate retrieval.
Embeddings: each chunk is converted into a vector using a local sentence-transformer model — text with similar meaning produces similar vectors.
Retrieval: the question is embedded the same way, and cosine similarity is used to find the closest-matching chunk.
Relevance threshold: if the best similarity score falls below a set threshold, the tool assumes the question isn't answerable from the document and skips the LLM call entirely, rather than risking a hallucinated answer.
Generation: the retrieved chunk and the question are combined into a single prompt and sent to Groq's LLM, which generates a natural-language answer grounded in that context.
Possible improvements
Overlapping chunks to avoid losing context at chunk boundaries
A proper vector database (e.g. Chroma) for larger documents instead of in-memory comparison
Support for multiple PDFs at once
Returning multiple relevant chunks instead of just the single best match
