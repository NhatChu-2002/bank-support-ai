import json
import requests

API_URL = "http://127.0.0.1:8000/chat"

def run():
    total = 0
    correct_cat = 0

    with open("test_cases.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            text = item["text"]
            expected = item["expected_category"]

            r = requests.post(API_URL, json={"customer_name": "Test", "message": text})
            out = r.json()
            pred = out["category"]

            total += 1
            if pred == expected:
                correct_cat += 1
            else:
                print(f"MISS | expected={expected} got={pred} | text={text}")

    print(f"\nClassification accuracy: {correct_cat}/{total} = {correct_cat/total:.2%}")

if __name__ == "__main__":
    run()
