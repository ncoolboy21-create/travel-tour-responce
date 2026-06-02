import json

# LOAD JSON DATA
with open("travel_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(f"Loaded {len(data)} travel records")

# CONVERT JSON TO TEXT
documents = []

for record in data:
    text = f"""
Destination: {record['destination_name']}
Country: {record['country']}
Destination Type: {record['destination_type']}
Travel Style: {record['travel_style']}
Budget Range: ₹{record['budget_min']} - ₹{record['budget_max']}
Trip Duration: {record['trip_duration']}
Activities: {', '.join(record['activities'])}
Meal Preference: {record['meal_preference']}

Description:
{record['description']}
""".strip()

    documents.append(text)
print(f"Created {len(documents)} documents")

# SAVE DOCUMENTS AS TXT
with open("travel_documents.txt", "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(doc)
        f.write("\n" + "=" * 80 + "\n")

print("travel_documents.txt saved successfully")

