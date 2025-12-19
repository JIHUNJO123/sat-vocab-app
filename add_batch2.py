import json
import urllib.request
import urllib.parse
import concurrent.futures

API_KEY = "AIzaSyCWW8OXnc7QwIUTs_W0FCEVrZEm3qliDzk"

# More SAT words batch 2
NEW_WORDS = """abase abash abate abdicate abet abeyance abide abject abjure ablution abnegate abode abolish abominate aboriginal abortive abound abrade abreast abridge abrogate abscond absolve abstain abstemious abstinence abstruse abusive abut abyss accede accelerate accentuate accessible accession acclaim acclimate accolade accommodate accomplice accord accost accretion accrue accumulate acerbic acknowledge acme acolyte acquiesce acquire acquisitive acquit acrid acrimonious acrophobia actuate acuity acumen adamant adaptation addendum addict addled adept adherent adjacent adjunct administer admirable admonitory adolescent adorn adroit adulation advent adventitious adversary adversity advocate aegis aerate aerobic aesthetic affable affectation affidavit affiliate affinity affirm affliction affluence affront aftermath agenda agglomeration aggrandize aggregate aggrieve agile agitate agnostic agrarian ague alacrity albeit albino alchemy alcove alias alibi alienate alimentary alimony allegation allegiance allegory alliteration allocate allot alloy allude allure alluvial almanac alms aloof altercation altruistic amalgam amass ambidextrous ambient ambiguous ambivalence amble ambrosia ambulatory ameliorate amenable amend amenity amiable amicable amiss amity amnesia amnesty amoral amorphous amortize amphibian amphitheater ample amplify amputate amulet anachronism analgesic analogy anarchist anarchy anathema ancestry ancillary anecdote anemia anguish angular animate animosity annals annex annihilate annotate annuity annul anoint anomalous anonymity antagonism antecedent antediluvian anthem anthology anthropoid anthropologist antic anticipate antidote antipathy antiquated antique antiseptic antithesis anvil apathetic aperture apex aphasia aphorism apiary aplomb apocalyptic apocryphal apogee apostate apostle apotheosis appall apparatus apparel apparition appeal appease append appetite applause apposite appraise apprehend apprise approbation appropriate apt aquatic aquiline arable arbiter arbitrary arbitrate arboreal arcade arcane archaeology archaic archer archetype archipelago archive ardor arduous argot aria arid aristocracy armada armistice aroma arraign array arrears arrest arrhythmic arrogant arsenal arson articulate artifact artifice artisan ascendancy ascertain ascetic ascribe ashen askance askew asperity aspersion aspirant assault assay assent assess assiduous assimilate assuage astral astringent astute asunder asylum atavism atheist atone atrocity atrophy attain attenuate attest attribute attrition atypical audacity audit augury august aura auroral auspice austere authentic authoritarian authoritative autocrat automaton autonomous autopsy auxiliary avalanche avarice avenge averse avert aviary avid avocation avow avuncular awl awning awry axiom azure babble bacchanalian badger badinage baffle bait baleful balk ballad ballast balm banal bane bantering barb bard baroque barrage barren barrister bask bastion bate bauble bawdy beatific beatitude bedizen bedraggle befuddle beget begrudge beguile behemoth beholden behoove belabor belated beleaguer belie bellicose belligerent bemoan bemused benediction benefactor beneficent benevolent benighted benign bequeath berate bereaved bereft berserk beseech beset besiege besmirch bestial bestow betoken betray betroth bevy bewail bewilder bicameral bicker biennial bifurcate bigot bilingual bilious bilk billowing bivouac bizarre blanch bland blandishment blasé blasphemy blatant bleak blemish blight blithe bloated bludgeon blunder blurt boisterous bolster bombast bombastic bondage boorish booty botch bourgeois bovine bowdlerize braggadocio brandish brash bravado brawn brazenly breach breadth brevity brindled brink bristling brittle broach brochure brooch brook browbeat brunt brusque buccaneer bucolic budge buffet buffoon bulge bulk bully bulwark bumptious buoyant burgeon burlesque burnish bustle buttress cabal cache cacophony cadaver cadaverous cadence cadet cajole calamity caliber calligraphy callous callow calumny camaraderie cameo camouflage canard candor canine canon canopy cant cantankerous cantata canter canvass capacious capitulate capricious caption captious captivate carat carafe carapace carcass cardinal careen caricature carnage carnal carnivorous carousal carping cartographer cascade caste castigate casualty cataclysm catalyst catapult cataract catastrophe catcall catechism categorical catharsis catholic caucus caulk causal caustic cavalcade cavalier caveat cavern cavil cede celerity celestial celibate censor censorious censure centrifugal centurion cerebral ceremonious certitude cessation cession chafe chaff chagrin chalice chameleon champion chancy chaos charade charisma charlatan chary chasm chassis chaste chasten chastise chattel check checkered cherubic chicanery chide chimerical chisel chivalrous choleric choreography chortle chronicle churlish ciliated cipher circuitous circumlocution circumscribe circumspect circumvent cistern citadel cite clairvoyant clamber clamor clandestine clangor clapper clarion clasp claustrophobia cleave cleft clemency cliché clientele climactic clime clique cloister clout coagulate coalesce coalition coarse coax coddle codicil codify coercion coeval cogent cogitate cognate cognizance cognomen cohabit cohere coherent cohesion cohorts coiffure coincide colander collaborate collage collateral collation colleague collective colloquial colloquy collusion colossal colossus comatose combustible comely comestible comeuppance commandeer commemorate commensurate commiserate commodious communal commute compact compatible compel compendium compensatory compile complacent complaisant complement compliance compliant complicity component comport composure compound comprehensive compress comprise compromise compunction compute concave concede conceit conceive concentric conception concerted concession conciliatory concise conclave conclusive concoct concomitant concord concordat concur condescend condign condiments condole condone conducive conduit confide configuration confine confiscate conflagration confluence conformity confound confront congeal congenial congenital conglomerate congregation congruent conifer conjecture conjugal conjure connive connoisseur connotation connubial conscientious conscript consecrate consensus consequential conservatory consign consistency console consolidate consonance consort conspiracy constituent constitute constrain constrict construe consummate contagion contaminate contemn contend contentious contest contiguous continence contingent contortion contraband contravene contrite contrived controvert contumacious contusion conundrum convene conventional convergent conversant converse convex conveyance conviction convivial convoke convoluted copious coquette cordon cornucopia corollary coronation corporal corporeal corpulent correlate corroborate corrode corrosive corrugate cosmic cosmopolitan cosmos cosset coterie countenance countermand counterpart courageous courier covenant covert covetous crass craven credence credentials credible credulity credulous creed crescendo crest crestfallen crevice cringe criteria crone crony crouch crucial crucible crux crypt cryptic crystalline cubicle cuisine culinary cull culminate culpable culprit cultivate cumbersome cumulative cunning cupidity curator curb curmudgeon cursive cursory curtail cynical cynosure dais dally damp dank dapper dappled daub daunt dauntless dawdle daze deadlock deadpan dearth debacle debase debauch debilitate debonair debris debunk decadence decapitate decelerate deciduous decimate decipher declaim declivity decorate decorous decorum decoy decree decrepit decry deducible deface defamation default defeatist defection defector defer deference defiance deficient defile definitive deflect defunct degenerate degradation dehydrate deify deign delete deleterious deliberate delineate delirium delta deluge delusion demagogue demean demeanor demise demographic demolish demoniac demotic demur demure denigrate denizen denomination denouement denounce depict deplete deplore deploy depose depravity deprecate depreciate depredation deranged derelict deride derivative dermatologist derogate derogatory descry desecrate desiccate designation desolate desperado despicable despise despoil despondent despot destitute desultory detached deterrent detonation detraction detrimental deviate devious devoid devolve devout dexterous diabolical diadem diagnose diagonal dialectical diaphanous diatribe dichotomy dictum didactic diffidence diffuse digression dilapidated dilate dilatory dilemma dilettante diligence dilute diminution din dinghy dingy dint diplomatic dire dirge disabuse disaffected disapprobation disarray disavowal disband discernible disclaim disclose discombobulate disconcert disconsolate discontinuity discordant discountenance discourse discredit discreet discrepancy discrete discretion discriminate discursive disdain disembark disenfranchise disengage disfigure disgorge disgruntle disheveled disinclination disingenuous disinter disjointed disjunctive dislodge dismal dismantle dismember dismiss disparage disparity dispassionate dispatch dispel disperse displace dispirit disputatious disputation disreputable disrupt dissection dissemble disseminate dissent dissertation dissident dissimulate dissipate dissociate dissolution dissonant dissuade distant distend distill distinction distort distraught distrait distraught dither diva diverge diverse diversify diversion diversity divest divine divulge docile docket doctrinaire doctrine doddering dogged doggerel dogmatic doldrums doleful dolt domicile domineer donkey doodle dormant dorsal dossier dotage dote doting dour downcast drab draconian draff draggy drastic drawl dregs drivel droll drone droop dross drudge drudgery dubious ductile dudgeon dulcet dumbfound dupe duplicity""".split()

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
    if added % 100 == 0:
        print(f"{added} done")
        with open('assets/data/words.json', 'w', encoding='utf-8') as f:
            json.dump(words, f, ensure_ascii=False, indent=2)

with open('assets/data/words.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)
print(f"Done! Total: {len(words)}")
