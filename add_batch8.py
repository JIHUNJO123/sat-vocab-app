import json
import urllib.request
import urllib.parse
import concurrent.futures

API_KEY = "AIzaSyCWW8OXnc7QwIUTs_W0FCEVrZEm3qliDzk"

# batch 8
NEW_WORDS = """rabble raconteur raffish rakish ramify rancor rankle rapprochement ratify raze rebuff recant recidivism reciprocate recondite recreant recrimination rectitude redact redoubt redress refractory regale remonstrance remunerate rend renege repine replete reprobate repudiate requisition rescind restitution resurgent retinue retrograde revamp revile rib ribald riposte rococo roil rostrum rubric ruffian ruminate sacrosanct sagacity salacious salient salubrious sanctimony sangfroid sanguinary sapient sardonic saturnine savant scapegoat scathing scintilla scourge screed scribe scrivener scruffy scrutinize scurvy secular seditious sedulous seethe semantics semblance senescent sentinel sepulchral sequester seraphic serendipitous serene serpentine servitude severance shard shibboleth shiftless shirk shoddy shrill sibilant simper sinecure sinuous skeptic skiff skulduggery slake slander slaver sleazy slipshod slough slovenly sluggard smirk snide sobriety sodden solace solecism solicitous solipsism somnolent sonorous sophistry sophomoric soporific sordid sortie sotto voce soupcon spate specious spendthrift splice spry spurious squalid stanch staunch steadfast stentorian stigmatize stint stipend stoic stolid stratagem stratum stricture strident stultify stupor stygian subservient substantive subterfuge succumb sully sundry supercilious supplicate surfeit surmount surreptitious surrogate svelte swathe sybaritic sycophant sylvan synod synopsis tacit taciturn talisman tangential tantamount tawdry teetotaler temerity temporal tendentious tenebrous tenet tensile tenuous tepid terminus terrestrial terse thane thespian thrall threnody throttle timbre tincture tirade titanic titular toady toadyism tome tonsorial torpid torrential tortuous touchstone tout traduce traipse trammel transgress transient translucent transmute transpire travail tremulous trenchant trepidation tribulation trice trident trifling troth truculent truncheon tryst tumescent tundra turgid turncoat turpitude tutelage twain twilight tyro ubiquitous umbrage unctuous undulate unguent unimpeachable unkempt unmitigated unseemly unsullied untoward urbane usurpation usury vacillate vagary vainglory valediction valet valorous vandalize vanguard variegated vassal vaunt veer venal veneer venerate ventral veracious verdure verisimilitude vernacular vernal verso vertex vertigo vestige vex viable vicar vicarious vicissitude vie vigilant vigil vilify vindicate vintner virago virile virtuoso virulent visage visceral viscid viscous vitiate vitrify vivacious vivisection vociferous volition voluble voracious votary vulpine waggish wane wanton wastrel watershed wax weal welt welter wheedle whet whimsical whinny whittle wield willful wily winnow winsome wistful wizened woe woebegone wont wraith wrangle wrath wrest writhe wry xenophobia yahoo yarn yeoman yoke yokel zany zealot zeitgeist zenith zephyr zest""".split()

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
