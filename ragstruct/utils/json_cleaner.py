import json
import os
import argparse

def flatten_json(d, parent_key='', sep='_'):
    """
    Recursively flattens a nested JSON dictionary.
    E.g., {"a": {"b": 1}} => {"a_b": 1}
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def clean_json(input_path: str, output_path: str = "cleaned.json", remove_null: bool = True):
    """
    Flattens and cleans a JSON file for RAG embedding.
    
    Args:
        input_path (str): Path to original JSON.
        output_path (str): Where to save the cleaned JSON.
        remove_null (bool): Remove null or empty values.
    """
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    flattened = flatten_json(raw_data)

    if remove_null:
        flattened = {k: v for k, v in flattened.items() if v not in [None, "", [], {}]}

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(flattened, f, indent=2, ensure_ascii=False)

    print(f"✅ Cleaned and flattened JSON saved to: {output_path}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flatten and clean a JSON file for ragstruct")
    parser.add_argument("input", help="Path to the input JSON file")
    parser.add_argument("--output", help="Output path (default: cleaned.json)", default="cleaned.json")
    parser.add_argument("--keep-null", action="store_true", help="Keep null/empty fields")

    args = parser.parse_args()
    clean_json(args.input, args.output, remove_null=not args.keep_null)

