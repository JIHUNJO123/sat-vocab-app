import json
import google.generativeai as genai
import time

API_KEY = "AIzaSyCWW8OXnc7QwIUTs_W0FCEVrZEm3qliDzk"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Load existing words
with open('assets/data/words.json', 'r', encoding='utf-8') as f:
    existing = json.load(f)
existing_words = set(w['word'].lower() for w in existing)
print(f"Existing: {len(existing)} words")

def generate_batch(start_id, count=50):
    prompt = f"""Generate {count} SAT vocabulary words with definitions, examples, and translations.
DO NOT include these words: {', '.join(list(existing_words)[:100])}

Return ONLY valid JSON array:
[
  {{
    "word": "aberrant",
    "partOfSpeech": "adjective",
    "definition": "departing from an accepted standard",
    "example": "His aberrant behavior worried his parents.",
    "ko": "비정상적인",
    "zh": "异常的",
    "hi": "असामान्य"
  }}
]

Requirements:
- SAT-level vocabulary (not too easy, not too obscure)
- Clear, concise definitions
- Natural example sentences
- Accurate translations
- Return exactly {count} words"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        
        words = json.loads(text.strip())
        result = []
        for i, w in enumerate(words):
            if w['word'].lower() not in existing_words:
                result.append({
                    'id': start_id + i,
                    'word': w['word'],
                    'partOfSpeech': w.get('partOfSpeech', 'noun'),
                    'definition': w['definition'],
                    'example': w['example'],
                    'level': ['Basic', 'Common', 'Advanced', 'Expert'][(start_id + i) % 4],
                    'translations': {
                        'ko': {'definition': w.get('ko', '')},
                        'zh': {'definition': w.get('zh', '')},
                        'hi': {'definition': w.get('hi', '')}
                    }
                })
                existing_words.add(w['word'].lower())
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []

# Generate 1000 new words in batches of 50
all_new = []
start_id = len(existing) + 1

for batch in range(20):  # 20 batches * 50 = 1000
    print(f"Batch {batch+1}/20...")
    words = generate_batch(start_id + len(all_new), 50)
    all_new.extend(words)
    print(f"  Got {len(words)}, Total: {len(all_new)}")
    
    if len(all_new) >= 1000:
        break
    time.sleep(1)

# Combine and save
existing.extend(all_new[:1000])
print(f"\nTotal words: {len(existing)}")

with open('assets/data/words.json', 'w', encoding='utf-8') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print("Saved!")
