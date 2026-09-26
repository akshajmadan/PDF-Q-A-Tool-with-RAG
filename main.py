from pypdf import PdfReader
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()
import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

reader = PdfReader("computer_networking_basics_test.pdf")

full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

words = full_text.split()

chunk_size = 500

chunks = []
for i in range(0, len(words), chunk_size):
    chunk = " ".join(words[i:i + chunk_size])
    chunks.append(chunk)


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")



embeddings = model.encode(chunks)
question = input("Enter your question: ")
question_embedding = model.encode([question])
similarities = model.similarity(embeddings, question_embedding)
context = torch.Tensor.max(similarities).item()
threshold = 0.3
if(context < threshold):
    print("The context is not relevant to the question.")
    exit()
else:
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Here is the context: {context}\n\n Answer the following question based on the context: {question}",
        }
    ],
    
    model="openai/gpt-oss-120b",
)

print(chat_completion.choices[0].message.content)