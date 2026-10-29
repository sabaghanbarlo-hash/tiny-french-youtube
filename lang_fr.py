"""French helpers for Tiny French (YouTube): which words are French, so French is spoken by a character and English by the narrator."""
import re

ACCENTS = set("àâäçéèêëîïôöùûüÿœæÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸŒÆ")
FR_WORDS = set("""
je tu il elle on nous vous ils elles me te se lui leur mon ma mes ton ta tes son sa ses notre nos votre vos leurs
le la les un une des du de d l au aux ce cet cette ces ça ceci cela
et ou mais donc or ni car que qui quoi dont où quand comment pourquoi combien si
dans sur sous avec sans pour par chez entre vers depuis pendant avant après contre
suis es est sommes êtes sont étais était avais avait ai as a avons avez ont vais vas va allons allez vont
fais fait faites font veux veut voulez voudrais voudrait peux peut pouvez dois doit
oui non pas ne plus jamais rien très trop assez bien mal beaucoup peu aussi encore déjà toujours souvent
bonjour bonsoir salut merci pardon excusez moi toi s'il vous plaît plait au revoir bientôt demain hier aujourd'hui
voici voilà voila c'est j'ai j'aime je m'appelle enchanté enchantée
un deux trois quatre cinq six sept huit neuf dix
rouge bleu vert jaune blanc noir petit petite grand grande bon bonne beau belle
manger boire parler aller venir voir aimer avoir être faire prendre donner
pain eau café thé lait pomme fromage croissant baguette gare train billet rue maison école ville
ami amie frère sœur mère père famille
matin soir nuit jour semaine lundi mardi mercredi jeudi vendredi samedi dimanche
""".split())
EN_WORDS = set("""
the a an and or but if so to of in on at for from with without by about as is are was were be been am do does did
how what which who whom whose when where why can could will would should shall may might must
you your yours i me my mine we us our he him his she her it its they them their this that these those
say says said mean means meaning translate translation word words phrase sentence correct answer question option
not no yes please thank thanks hello goodbye sorry excuse
french english which best choose pick right wrong true false
there here then than too very more most some any all each every one two three
""".split())
KNOWN = set()          # French words seen in the script itself (filled by learn())
_WORD = re.compile(r"[\wÀ-ÿŒœ]+(?:['’][\wÀ-ÿŒœ]+)*", re.U)


def words(text):
    out = []
    for w in _WORD.findall(text.lower()):
        out.append(w.replace("’", "'"))
        if "'" in w or "’" in w:                      # l'eau -> l, eau
            out.extend(p for p in re.split(r"['’]", w) if p)
    return out


def learn(text):
    """Remember the words of a French line so later mixed text (quiz options, explanations) is read in the right voice."""
    for w in words(text):
        if len(w) > 2 or w in FR_WORDS:
            KNOWN.add(w)


def pron(_text):
    """No automatic pronunciation line for French (add a third part to a line if you want one)."""
    return ""


def is_french(text, default=False):
    toks = words(text)
    if not toks:
        return False
    fr = sum(1 for t in toks if t in FR_WORDS or t in KNOWN or any(ch in ACCENTS for ch in t))
    en = sum(1 for t in toks if t in EN_WORDS and t not in KNOWN)
    if fr > en:
        return True
    if en > fr:
        return False
    return default


_QUOTED = re.compile(r"(«[^»]+»|“[^”]+”|\"[^\"]+\"|(?<![\w])'[^']+'(?![\w]))")


def split_runs(text, default=False):
    """-> [(run, is_french)]. «guillemets» always force French; other quoted bits and the text around them are classified."""
    runs = []
    for k, piece in enumerate(_QUOTED.split(text)):
        if not piece or not piece.strip():
            continue
        if k % 2:
            forced = piece[0] == "«"
            inner = piece[1:-1].strip()
            runs.append((inner, True if forced else is_french(inner, default=default)))
        else:
            runs.append((piece.strip(), is_french(piece)))
    merged = []
    for r, f in runs:                     # join neighbours with the same language
        if merged and merged[-1][1] == f:
            merged[-1] = (merged[-1][0] + " " + r, f)
        else:
            merged.append((r, f))
    return merged


def options_default(question):
    """Quiz options are French unless the question asks what a French word means."""
    return not re.search(r"\b(what does|mean|means|meaning|in english)\b", question or "", re.I)
