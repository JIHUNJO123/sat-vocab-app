import json

# Check duplicates within each file
files = ['words_n5_n3.json', 'words_n2.json', 'words_n1.json']
all_words = {}

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    words = [w['word'] for w in data]
    unique_words = set(words)
    duplicates = [w for w in unique_words if words.count(w) > 1]
    
    print(f'\n{filename}:')
    print(f'  Total entries: {len(words)}')
    print(f'  Unique words: {len(unique_words)}')
    print(f'  Duplicates: {len(duplicates)}')
    if duplicates:
        print(f'  Sample duplicates: {duplicates[:10]}')
    
    all_words[filename] = unique_words

# Check overlaps between files
print('\n=== Overlaps between files ===')
n5n3 = all_words['words_n5_n3.json']
n2 = all_words['words_n2.json']
n1 = all_words['words_n1.json']

overlap_n5n3_n2 = n5n3 & n2
overlap_n2_n1 = n2 & n1
overlap_n5n3_n1 = n5n3 & n1

print(f'Overlap between N5-N3 and N2: {len(overlap_n5n3_n2)} words')
if overlap_n5n3_n2:
    print(f'  Sample: {list(overlap_n5n3_n2)[:10]}')

print(f'Overlap between N2 and N1: {len(overlap_n2_n1)} words')
if overlap_n2_n1:
    print(f'  Sample: {list(overlap_n2_n1)[:10]}')

print(f'Overlap between N5-N3 and N1: {len(overlap_n5n3_n1)} words')
if overlap_n5n3_n1:
    print(f'  Sample: {list(overlap_n5n3_n1)[:10]}')

