import json
import urllib.request
import urllib.parse
import concurrent.futures

API_KEY = "AIzaSyCWW8OXnc7QwIUTs_W0FCEVrZEm3qliDzk"

# 1000 new SAT words (not in existing list)
NEW_WORDS = """aberration abrasive abstain accolade admonish adversity advocate aesthetic affluent alleviate ambiguous ambivalent ameliorate analogous anecdote anomaly antagonist apathy arbitrary archaic articulate ascertain aspire astute audacious augment auspicious austere autonomous aversion avid banal benevolent bolster brevity candid capricious catalyst caustic circumspect clandestine coalesce cogent coherent complacent comprehensive concede concise conducive conflagration congenial conjecture consolidate conspicuous contempt contentious conundrum conventional conviction copious corroborate credulous criterion culminate curtail cynical dearth debilitate decorum deduce defer deference deficient delegate deleterious delineate denounce depict deplete deplore derivative desolate deterrent detrimental deviate didactic diffident digress diligent diminish discern discord disdain disparage disparity disseminate dissent dissonance divergent diverse divulge doctrine dogmatic dormant dubious eclectic eclipse effervescent egregious elicit eloquent elusive emancipate embellish eminent empathy empirical emulate endorse enigma entice enumerate ephemeral epitome equanimity equivocal eradicate erratic esoteric esteem ethereal euphemism evade evanescent exacerbate exalt exemplary exhaustive exhilarate expedite explicit exploit exposition expunge extol extraneous facilitate fallacy fanatical fastidious feasible fervent fickle flagrant flourish fluctuate forestall fortuitous foster fractious frivolous frugal fundamental futile galvanize garner garrulous glutton gratuitous gregarious guile hackneyed hamper haphazard harbinger hardy hedonism heresy hierarchy hindrance holistic homogeneous hubris hyperbole hypothetical iconoclast idiosyncrasy idyllic imminent impartial impede impending imperative impetuous implicit impoverish impromptu improvise incisive incoherent incongruous incorporate incorrigible incredulous indifferent indigenous indignant indolent industrious ineffable inept inevitable inexorable infamous infamy infer infiltrate infinitesimal influx ingenious inherent inhibit innate innocuous innovative inquisitive insatiable insidious insinuate insipid insolent instigate insurgent integral integrity intrepid intricate intrinsic intuitive inundate invective invoke irate ironic irrelevant irreverent jeopardize judicious kindle kinetic labyrinth laconic lament lampoon languid laud lavish lethargic levity linger listless lofty lucid luminous magnanimous malevolent malleable mandate manifest mar materialize meager meander mediate melancholy mercenary meticulous militant mitigate monotonous morose myriad naive negligent nonchalant notorious novel novice nuance nurture obdurate objective oblique obscure obstinate ominous opaque opportune opulent orthodox ostentatious overt pacify palpable paradigm paradox pariah parody partisan patronize paucity pedantic penchant pensive perilous peripheral perpetuate perplexing perseverance pertinent pervasive pessimistic petulant phenomenon philanthropic pious pivotal placate plagiarize plausible plight plunder poignant pompous ponderous pragmatic precedent preclude predecessor predilection predominant preeminent preliminary prelude premise premonition preposterous prestige prevalent pristine procrastinate prodigious proficient profound prohibit prolific prominent propensity prophetic propriety prosaic prosperity protocol prototype provincial provocative prudent pungent quaint qualm quandary querulous rampant rancor ratify ravenous rebuke reclusive reconcile rectify redundant refute rehabilitate reiterate rejuvenate relegate relinquish reluctant reminiscent renounce replete reprehensible repudiate rescind resigned resilient resolve resonate respite restrain reticent retribution reverence rhetoric rigorous robust rudimentary ruthless sagacious salient sanction saturate scant scrutinize seclude sedentary sentiment serenity servile shrewd skeptic slander solemn solicit solitude somber speculate sporadic spurious spurn stagnant steadfast stoic stringent strife subjugate submissive subordinate subsequent substantiate subtle succinct succumb superficial superfluous supplant suppress surmise surpass surreptitious susceptible sustain sycophant symmetry synthesis tacit tactful tangent tangible tedious temper tenacious tentative tenure terminate terrestrial terse testament thwart timid tirade torpid toxic transient transparent traverse trepidation trite trivial turbulent ubiquitous unanimous undermine underscore unilateral unprecedented unruly usurp utilitarian utopia validate valor vanquish vehement venerate verbose verify versatile vestige viable vicarious vigilant vindicate virtuoso virulent visceral vivacious volatile voluminous vulnerable wane wary whimsical wistful zealous zenith""".split()

def get_def(word):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=5)
        d = json.loads(r.read().decode('utf-8'))
        m = d[0]['meanings'][0]
        df = m['definitions'][0]
        return {'def': df['definition'], 'ex': df.get('example', f'The {word} was evident.'), 'pos': m['partOfSpeech']}
    except:
        return None

def translate(text, lang):
    try:
        url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}&q={urllib.parse.quote(text)}&target={lang}"
        r = urllib.request.urlopen(url, timeout=10)
        return json.loads(r.read())['data']['translations'][0]['translatedText']
    except:
        return text

# Load existing
with open('assets/data/words.json', 'r', encoding='utf-8') as f:
    words = json.load(f)
existing = set(w['word'] for w in words)
start_id = len(words) + 1

# Get new words not in existing
new_words = [w for w in NEW_WORDS if w not in existing][:1000]
print(f"Adding {len(new_words)} new words...")

# Get definitions parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
    defs = list(ex.map(get_def, new_words))

added = 0
for i, (word, d) in enumerate(zip(new_words, defs)):
    if not d:
        continue
    # Translate
    ko = translate(d['def'], 'ko')
    zh = translate(d['def'], 'zh')
    hi = translate(d['def'], 'hi')
    
    words.append({
        'id': start_id + added,
        'word': word,
        'level': ['Basic', 'Common', 'Advanced', 'Expert'][added % 4],
        'partOfSpeech': d['pos'],
        'definition': d['def'],
        'example': d['ex'],
        'translations': {
            'ko': {'definition': ko},
            'zh': {'definition': zh},
            'hi': {'definition': hi}
        }
    })
    added += 1
    if added % 50 == 0:
        print(f"{added} done")
        with open('assets/data/words.json', 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)

with open('assets/data/words.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)
print(f"Done! Total: {len(words)}")
