import json

# Step 1: Load raw document blocks
with open(r"C:\Users\shlok\Desktop\GenAI\GenAIProject\rag_model\travel_documents.txt", "r", encoding="utf-8") as f:
    content = f.read()

records = content.split("=" * 80)
records = [r.strip() for r in records if r.strip()]

print("Total records:", len(records))

# Step 2: Decide target chunk count
target_chunks = 300

# Compute how many records per chunk
chunk_size = max(1, len(records) // target_chunks)

print("Records per chunk:", chunk_size)

# Step 3: Group records into bigger chunks
grouped_chunks = []

for i in range(0, len(records), chunk_size):
    group = records[i:i + chunk_size]

    # Combine multiple destinations into one chunk
    combined_text = "\n\n".join(group)

    grouped_chunks.append(combined_text)

# Step 4: Save to JSON
with open(r"C:\Users\shlok\Desktop\GenAI\GenAIProject\rag_model\travel_chunks.json", "w", encoding="utf-8") as f:
    json.dump(grouped_chunks, f, indent=2, ensure_ascii=False)

print("Final number of chunks:", len(grouped_chunks))
print("Saved to travel_chunks.json")