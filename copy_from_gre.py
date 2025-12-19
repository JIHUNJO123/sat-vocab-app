import json

# GRE words 로드
with open('C:/Users/hooni/Desktop/gre_vocab_app/assets/data/words.json', 'r', encoding='utf-8') as f:
    gre_words = json.load(f)

# SAT words 로드
with open('assets/data/words.json', 'r', encoding='utf-8') as f:
    sat_words = json.load(f)

existing = set(w['word'] for w in sat_words)
start_id = len(sat_words) + 1

print(f"SAT 현재: {len(sat_words)}")
print(f"GRE 총: {len(gre_words)}")

# GRE에서 SAT에 없는 단어 가져오기
added = 0
for gw in gre_words:
    if gw['word'] not in existing and added < 346:
        sat_words.append({
            'id': start_id + added,
            'word': gw['word'],
            'level': gw.get('level', 'Advanced'),
            'partOfSpeech': gw.get('partOfSpeech', 'noun'),
            'definition': gw.get('definition', ''),
            'example': gw.get('example', ''),
            'translations': gw.get('translations', {})
        })
        existing.add(gw['word'])
        added += 1

with open('assets/data/words.json', 'w', encoding='utf-8') as f:
    json.dump(sat_words, f, ensure_ascii=False, indent=2)

print(f"Added {added} from GRE, Total: {len(sat_words)}")
