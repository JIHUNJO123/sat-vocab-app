import json
import urllib.request
import urllib.parse
import concurrent.futures

API_KEY = "AIzaSyCWW8OXnc7QwIUTs_W0FCEVrZEm3qliDzk"

# batch 9 - academic verbs and adjectives
NEW_WORDS = """abash abate abdicate aberration abhor abject ablaze abloom abnegate abode abolish abominate aborigine abound abrasive abridge abroad abrupt abscond absolve abstention abstinence abstract abstruse absurd abundant abusive abut abyss academic accede accelerate accentuate accept accessible accession accessory accidental acclimate accommodate accomplice accomplished accordion accost accredit accrue accumulate accusation accusatory accustom acerbic ache achievable acid acidic acknowledgment acne acoustic acquaint acquire acquisitive acquittal acrid acrobat acrobatic acronym activate active activism actor actress actual acuity acute adage adamant adapt adaptable addendum addict addictive addition additional additive addled address adept adequate adhere adhesion adhesive adjacent adjourn adjudicate adjunct adjustable adjustment administer administration admiral admirable admiration admire admissible admit admittance adolescence adopt adorable adore adorn adrenaline adrift adroit adulation adulatory adulterate adulthood advance advancement advantage advent adventurous adversarial adversary adverse adversity advert advertise advisable advise advisory advocate aerial aerobic aerodynamic aesthetic afar affable affectation affected affiliate affiliation affirm affirmation affirmative affliction affluent afford affordable affront afire afloat aforementioned afraid aft afterglow aftermath afternoon afterward agape agate aged ageless agency agenda agglomerate aggrandize aggravate aggregate aggression aggressive aggressor aggrieved aghast agile agility aging agitate agitated agitation agnostic agonize agonizing agony agrarian agree agreeable agreement agricultural agriculture aground ahead ailing ailment aimless airdrop airy ajar akin alarm alarming albeit albino album alchemy alert alertness algebra algebraic alias alibi alien alienate alight align alignment alike alimentary alimony alive alkali alkaline allegation alleged allegiance allegorical allegory allergic allergy alleviate alley alliance allied alligator allocate allot allotment allowable allowance alloy allude allure alluring allusion ally almanac almighty almond alms aloft aloha alone aloof aloud alphabet alphabetical alpine already also alterable alteration altercation alternate alternative although altitude alto altruism altruistic aluminum amateur amaze amazed amazement amazing ambassador amber ambiance ambidextrous ambient ambiguity ambiguous ambition amble ambrosia ambulance ambush ameliorate amenable amend amendment amenity amiable amicable amid amidst amiss ammonia ammunition amnesia amnesty amok amoral amorous amorphous amount amour amphibian amphibious amphitheater ample amplification amplify amplitude amputate amulet amuse amusement amusing anachronism anachronistic anaerobic anagram analogous analogue analogy analyse analysis analyst analytic analytical analyze anarchist anarchy anatomical anatomy ancestral ancestry anchor anchorage ancient ancillary anecdotal anecdote anemia anemic anesthetic angel angelic anger angle angler angling angry anguish angular animal animate animated animation animosity ankle annals annex annihilate annihilation anniversary annotate annotation announce announcement annoy annoyance annoyed annoying annual annuity annul anomalous anomaly anonymity anonymous antagonism antagonist antagonistic antagonize antecedent antelope antenna anthem anthology anticipate anticipation anticlimactic antidote antigen antipathy antiquarian antiquated antique antiquity antiseptic antisocial antithesis antithetical antsy anxiety anxious anybody anyhow anyone anyplace anything anyway anywhere apart apartheid apathetic apathy apex aphrodisiac apiece aplomb apocalypse apocalyptic apocryphal apogee apologetic apologize apology apoplectic apostle apothecary appall appalled appalling apparatus apparel apparent apparently appeal appealing appear appearance appease appellant appellate append appendage appendix appetite appetizer appetizing applaud applause apple applicable applicant application applied apply appoint appointment appraisal appraise appreciable appreciate appreciation appreciative apprehend apprehension apprehensive apprentice apprenticeship approach approachable appropriate appropriation approval approve approximate approximation aptitude aquarium aquatic aqueduct aquifer arable arbiter arbitrary arbitrate arbitration arbitrator arboreal arbor arcade arcane arch archaeological archaeologist archaeology archaic archangel archbishop archery archetype archipelago architect architectural architecture archive archway ardent ardor arduous area arena arguable arguably argue argument argumentative arid arise aristocracy aristocrat aristocratic arithmetic ark armada armadillo armament armchair armed armistice armoire armor armored armory armpit army aroma aromatic arouse arrange arrangement array arrears arrest arrival arrive arrogance arrogant arrow arsenal arson art arterial artery artful arthritis artichoke article articulate articulation artifact artifice artificial artillery artisan artist artistic artistry artwork""".split()

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
