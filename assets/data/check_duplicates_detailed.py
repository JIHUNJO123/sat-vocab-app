import json

# Check duplicates within each file by level
files = ['words_n5_n3.json', 'words_n2.json', 'words_n1.json']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check duplicates by (word, level) combination
    word_level_pairs = {}
    duplicates = []
    
    for entry in data:
        key = (entry['word'], entry['level'])
        if key in word_level_pairs:
            duplicates.append(key)
        else:
            word_level_pairs[key] = entry
    
    print(f'\n{filename}:')
    print(f'  Total entries: {len(data)}')
    print(f'  Unique (word, level) pairs: {len(word_level_pairs)}')
    print(f'  Duplicates (same word, same level): {len(duplicates)}')
    if duplicates:
        print(f'  Sample duplicates: {duplicates[:10]}')
    else:
        print('  ✅ No duplicates!')

