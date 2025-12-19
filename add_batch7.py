import json
import urllib.request
import urllib.parse
import concurrent.futures

API_KEY = "AIzaSyCWW8OXnc7QwIUTs_W0FCEVrZEm3qliDzk"

# 300 words batch 7
NEW_WORDS = """abrogate accost adjure affray agape allay allege ambit amenable annex antechamber apothegm apposite arrogate askance astringent augury aviary badinage beatific bedlam beholden bequest bilk blanch blight bluster boisterous bombard brindled burnish cabal canard carouse cavort chasten chisel chronic clamber cloy coffer comity compunction conclave confiscate consign contravene contrition cosset craven crevice crotchety curate dally decry deference demarcate demur denude depict desist devolve disburse disclaim discursive disinter dissipate dissuade dither divulge dodder dolt dormant dross dulcet edify efface elegy emollient enervate engender enmity entreat equanimity erstwhile excoriate execrable exigency expatiate expiate extirpate facile factotum feint fetter fissure flout foment forestall forswear fractious freshet froward gaffe garish garner genuflect gestate gesticulate glean glib glower gnash gorge gradient grandiloquent grovel harangue harrow heyday hoary hone hubris hullabaloo iconoclast idyll ignominy imbibe imbroglio immolate impale impasse imperturbable imprecation impropriety impute inchoate incipient inculpate indefatigable indigence indite ineffable ineluctable iniquity insensate insuperable interpolate internecine interpose intimation intone intrepid inure invective inveigh irascible itinerant jape jejune jocose ken labyrinth languor largesse lassitude legerdemain levity libertine ligneous limn litany livid loath lucre macabre machination maelstrom malediction maleficent malodorous mangle manumit mar martinet mellifluous mendacity mendicant militate minutiae mire miscreant modicum morass mordant moribund mot motley muggy mulct munificent murky muster nabob nascent ne'er nefarious neologism nettle niggling nihilism noisome nonage noxious nugatory obdurate objurgate obloquy obviate occlude odoriferous officious onerous opine opprobrium ossify overwrought pallid palpitate panache pander panegyric parapet parch pariah parvenu patina paucity peculate penchant penury perambulate peremptory perfidy peripatetic perjury peroration perspicacity pertinacious perturb pervade philistine pillory pinion pique plaintive plangent plaudit plod plumb poise politic portent posit potable potentate prattle precipitate predicate predilection preen preponderate presage presentiment prevaricate prim privation probity profligate prolix propinquity propound proscribe proselyte prosody protract provender proviso prurient puissant punctilious purview pusillanimous quaff qualm quandary quarry quash querulous quietude quixotic quorum quotidian""".split()

def get_def(word):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=5)
        d = json.loads(r.read().decode('utf-8'))
        m = d[0]['meanings'][0]
        df = m['definitions'][0]
        return {'def': df['definition'], 'ex': df.get('example', ''), 'pos': m['partOfSpeech']}
    except:
        return None

def translate(text, lang):
    try:
        url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}&q={urllib.parse.quote(text)}&target={lang}"
        r = urllib.request.urlopen(url, timeout=10)
        return json.loads(r.read())['data']['translations'][0]['translatedText']
    except:
        return text

with open('assets/data/words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)
existing = set(w['word'] for w in words)
start_id = len(words) + 1

new_words = [w for w in NEW_WORDS if w not in existing]
print(f"Adding {len(new_words)} new words...")

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
    defs = list(ex.map(get_def, new_words))

added = 0
for word, d in zip(new_words, defs):
    if not d: continue
    ko = translate(d['def'], 'ko')
    zh = translate(d['def'], 'zh')
    hi = translate(d['def'], 'hi')
    words.append({
        'id': start_id + added,
        'word': word,
        'level': ['Basic', 'Common', 'Advanced', 'Expert'][added % 4],
        'partOfSpeech': d['pos'],
        'definition': d['def'],
        'example': d['ex'] or f"The {word} was remarkable.",
        'translations': {'ko': {'definition': ko}, 'zh': {'definition': zh}, 'hi': {'definition': hi}}
    })
    added += 1

with open('assets/data/words.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)
print(f"Done! Added {added}, Total: {len(words)}")
