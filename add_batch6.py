import json
import urllib.request
import urllib.parse
import concurrent.futures

API_KEY = "AIzaSyCWW8OXnc7QwIUTs_W0FCEVrZEm3qliDzk"

# More SAT words batch 6 - high frequency SAT specific
NEW_WORDS = """aberrant abjure abrade abscission abstruse accede acclimate accrete acquiesce acrimonious adjudicate adroit adultery adversarial aegis affable affable agnostic agrarian alacrity albatross alcove allegory allocution allusion altercation ambiance ameliorate amend amicable anachronistic analogous anathema anecdotal anomalous antagonist antebellum anthropocentric antipathy antithetical apathy aperture apex aphorism apocalyptic apocryphal apostrophe appease approbation apropos aptitude aquatic arbiter arbitrary arbitrate archaic archipelago ardent arduous arid aristocracy armistice aromatic artisan ascertain ascetic aspirant assail assay assent assertive assiduous assimilate assuage astute attenuate attrition audacious augment auspicious austere autocratic avarice aversion axiom azure bacchanalian baleful banal bane baroque barrage bastion bayou beckon belabor beleaguered belie bellicose belligerent bemoan benevolent berate bereft bestial besiege bevy bilious biopsy blase blatant blemish blithe bohemian boorish brash brawn brevity broach bromide bucolic burgeon buttress cabal cacophony cadence cajole callous candid candor cant capricious captious cardinal carnage carnivorous carte blanche cascade castigate catalyst caustic cavalier caveat celerity censorious censure cerebral chaff chagrin charlatan chasm chastise cherub chicanery chide choleric churlish circuitous circumscribe circumspect circumvent clandestine clemency clique coalesce codify cogent cognizant colloquial collusion commensurate compendium complacent compliant compunction conciliate conclave concomitant condescend condolence conflagration confluence conformist congenial conjecture connive consanguinity conscientious consecrate consensus consort conspicuous consummate contemn contentious contingent contrite conundrum convene converge convivial copious cordon corollary corporeal corroborate cosmopolitan coterie countenance countermand covert credulous creed criterion crypt culpable cursory cynical dalliance dearth debacle decadence decorum defamatory deferential defunct deign deleterious delineate deluge demagogue demeanor demise demure denigrate denizen denounce deplete deplorable deprecate deride derivative desecrate desiccate desolate despot desultory detached deterrent devolve diaphanous diatribe dichotomy didactic diffident digress dilatory dilemma dilettante diminutive dirge disaffected discerning discomfit discordant discourse disdain disenfranchise disgruntled dishevel disparage dispatch disperse disquiet dissemble disseminate dissolution dissonance distend divergent divestiture docile dogmatic dormant dour draconian dubious dulcet duplicitous duress ebullient eclectic effervescent efficacious effrontery egalitarian egregious elated elegy elicit elite elixir elliptical elocution elucidate emaciated emanate emancipate embellish embroil emollient empirical emulate enclave endemic endorse enigma ennui enormity enthrall enumerate ephemeral epitome equanimity equivocal eradicate erudite eschew esoteric espouse ethereal etymology euphemism evanescent evince exacerbate exacting exalt exasperate exculpate execrable exemplary exempt exhort exigent exonerate expedient expedite expiate explicit exposition expunge extant extenuate extol extort extricate exuberant facetious facilitate faction fallacious fastidious fatuous fawn feckless fecund felicitous fervent fester fetid fetter fidelity fiendish figurative filial filibuster finesse flaccid flagrant flamboyant fledgling flippant florid flourish flout foible foment forbearance foreboding forensic forfeit formidable fortuitous foster fractious frenetic frivolous frugal fulsome furtive futile gaffe gainsay galvanize gambit gamut garish garrulous gauche gaudy genre germane gestalt gibe glean glib gorge grandiloquent gratuitous gregarious grievous guile guileless gullible hackneyed haggard hallowed hamper hapless harbinger harrowing haughty hedonism hegemony heinous heresy heterogeneous heuristic hiatus hierarchy histrionic homogeneous hone husband hyperbole iconoclast idiosyncrasy idyllic ignominious illicit imminent immutable impasse impeccable impecunious imperative imperious impervious impetuous implacable implicate implicit importune impregnable impromptu improvident impudent impugn impunity incandescent incantation incense inchoate incipient incisive inclement incongruous incorrigible incredulous incriminate inculcate incumbent incursion indelible indigent indignant indolent indomitable indulgent ineffable inept inequity inexorable infamy inference infidel infiltrate infinitesimal influx ingratiate inherent innocuous innuendo inscrutable insidious insinuate insipid insolent insouciant instigate insular insurgent intangible interminable intractable intransigent intrepid intrinsic introspective inundate inured invective inveterate invidious irascible irksome irreverent itinerant jargon jaundiced jeopardize jingoist jocular judicious juxtapose kaleidoscope keen ken kindle kinetic labyrinthine laceration lachrymose lackluster laconic laissez faire lament lampoon languish largesse lascivious latent laudable lethargic leviathan licentious limpid linchpin listless lithe litigious loathe loquacious lucid lucrative lugubrious luminous luxuriant machination magnanimous magnate maladroit malfeasance malicious malleable mandate manifest manifold mar marshal martinet maudlin maverick meander melancholy melee mellifluous mendacious mendicant mercenary mercurial meritorious metamorphosis meticulous milieu minion mire miscreant miserly missive mitigate mnemonics modicum mollify monotonous moot moribund morose mortify mundane munificent mutable myriad nadir narcissism nascent nebulous nefarious neophyte nepotism nettle nominal nonchalant noncommittal notoriety novice noxious nuance obdurate obfuscate obligatory oblique oblivion obscure obsequious obsolete obstinate obtuse odious officious ominous omnipotent omniscient onerous opaque opportunist opprobrium opulence oracle oration ordain orthodox oscillate ostentatious ostracize oust overture overwrought painstaking palatable palliate panacea pandemic panegyric paradigm paradox paragon pariah parody parry parsimony partisan pastoral patent pathological pathos patronize paucity pecuniary pedagogue pedantic pedestrian penchant penitent pensive penurious perennial perfunctory peripatetic pernicious perpetuate perquisite perspicacious pertinent peruse pervasive petulant philanthropy phlegmatic pilgrimage pinnacle pious pique pithy placate placid plaintive platitude plausible plethora poignant polemic pompous ponderous portend portent posthumous pragmatic preamble precarious precedent precipitous preclude precocious precursor predator predecessor predilection preeminent preempt premise premonition preponderance prerequisite prescient prestige presumptuous pretentious prevalent prevaricate primordial pristine privy probity proclivity prodigal prodigious profane profound profuse proliferate prolific promulgate propagate propensity prophetic propitiate propriety prosaic proscribe proselytize protagonist protracted provincial provocative prowess prudent prurient pseudonym pundit pungent purport purvey quagmire quaint qualm quandary querulous quiescent quintessential quixotic quotidian raconteur ramification rampant rancor rapacious ratify raucous ravenous rebuke recalcitrant recant reciprocal recluse reconcile recondite recount rectitude recumbent redolent redundant refute regal relegate relish remonstrate remorse renege renounce repast replete reprehensible reprisal reproach reprobate repudiate requisite rescind resentment resigned resilient resolute respite resplendent restitution reticent retribution reverent rhetoric rigorous robust rogue rostrum rudimentary ruminate rustic ruthless saccharine sacrilege sacrosanct sagacious salient salubrious sanction sanctimonious sanguine sardonic satiate satirical savant scant scathing schism scintillate scourge scrupulous scrutinize scurrilous secluded secular sedentary sedition seethe segue self effacing seminal sensuous sententious sentient seraph serendipity serpentine servile sever sham shrewd shun simile simulation sinecure singular skulk slander sloth slovenly smug snare sobriety sojourn solace solicitous soliloquy soporific sordid sparse spartan spawn specious speculative spurious squalid squander stagnant staid stalwart stamina stark staunch steadfast stigma stilted stint stipulate stoic stolid stratagem strident stringent stymie suave subjugate sublime subordinate subpoena subsequent subservient substantiate subtle subtlety subvert succinct succumb suffrage sullen sumptuous sundry supercilious superficial superfluous supine supplant supplicant surfeit surmise surpass surreptitious surrogate sycophant symbiotic synopsis tacit taciturn tangential tantalize tantamount tarnish taut tawdry tedious temerity temperate tempestuous temporal tenacious tenet tentative tenuous tepid terrestrial terse therapeutic thespian thrifty thwart tirade toady tome torpid torrid tortuous tout tractable trajectory transcend transgression transient transitory travesty treatise tremulous trenchant trepidation trite truculent tumult turbid turgid turpitude tyro ubiquitous umbrage unassuming uncanny unconscionable unctuous undermine unequivocal unfetter uniformity unilateral unkempt unprecedented unravel unseemly untoward unwitting upbraid urbane usurp utilitarian utopian vacillate vagabond vagrant vanguard vapid vehement venal venerable venerate veracious verbose verdant verity vernacular vernal versatile vex viable vicarious vicissitude vigilant vilify vindicate vindictive virtuoso virulent visceral viscous vitriolic vituperate vivacious vocation vociferous volatile volition voluminous voracious vouchsafe waive wane warrant wary watershed wax whimsical willful wily wistful withstand wizened woe wrangle wrath wrest writhe xenophobe yoke zeal zealous zenith zephyr""".split()

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
for i, (word, d) in enumerate(zip(new_words, defs)):
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
    if added % 200 == 0:
        print(f"{added} done")
        with open('assets/data/words.json', 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)

with open('assets/data/words.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)
print(f"Done! Total: {len(words)}")
