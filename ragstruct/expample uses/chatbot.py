# semantic_retriever_demo.py
import os
import json
import getpass
from ragstruct import ragstruct
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain.chat_models import init_chat_model

# 🔐 Set API Key
if not os.environ.get("yo api key"):
    os.environ["API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

# 🔧 Initialize model + embeddings
embedding_model = MistralAIEmbeddings(model="mistral-embed")
model = ChatMistralAI(model="mistral-large-latest")

# 📂 Load JSON memory
with open("your_json.json", "r", encoding="utf-8") as f:
    memory_json = json.load(f)

# 📦 Init retriever
retriever = ragstruct(
    embedding_model=embedding_model,
    llm_model=None,
    document=memory_json,
    from_json=True
)

# 🧠 Joshi personality
system_prompt = '''Help the user go through the text'''
# 💬 Chat history
conversation_history = []

# 🚀 Start chat
print("\n🎤  Type your question (or 'exit' to quit):\n")
while True:
    user_query = input("You: ").strip()
    if user_query.lower() in ["exit", "quit"]:
        break

    conversation_history.append(f"User: {user_query}")

    # 🔍 Retrieve relevant memory
    matched = retriever.retrieve(user_query, threshold=0.5, top_k=3)

    if matched:
        print(f"\n📌 Injected memory keys: {', '.join([k for k, _ in matched])}")
        context = "\n\n".join([f"[{k}]\n{v}" for k, v in matched])
        prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Query: {user_query}"
    else:
        history_context = "\n".join(conversation_history[-5:])
        prompt = f"{system_prompt}\n\nConversation History:\n{history_context}\nUser Query: {user_query}"

    # 🧠 Get response
    response = model.invoke(prompt)
    conversation_history.append(f"Bot: {response}")
    print(f"\n🤖 Bot: {response}\n")