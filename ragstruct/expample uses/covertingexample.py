from ragstruct.structurer import Structurer
from langchain.chat_models import init_chat_model
import json


# 🔧 Your LLM setup (e.g., mistral, ollama, openai)
llm = init_chat_model("mistral-large-latest", model_provider="mistralai")

# 🧠 Init the structurer
structurer = Structurer(llm=llm, chunk_size=700)

# 📂 Load your long paragraph doc
with open("input.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# 🛠️ Structure the doc
structured_output = structurer.structure_document(raw_text)

# 💾 Save
with open("output_structured.json", "w", encoding="utf-8") as f:
    json.dump(structured_output, f, indent=2)
