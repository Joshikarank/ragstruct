from ragstruct import ragstruct

# === Set your JSON file here
json_path = "path_to_your_file.json"  # Change path if needed

# === Load the ragstruct retriever (BGE is auto-forced)
retriever = ragstruct(json_path)

print("\n🎵 ragstruct is Ready!")
print("🧠 Ask a question (type 'exit' to quit):\n")

while True:
    query = input("> ").strip()
    if query.lower() in ["exit", "quit"]:
        break
    if query:
        result = retriever.retrieve(query)
        print(f"\n📦 Result:\n{result}\n")
