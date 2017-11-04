
import re


def preprocessing(facts):
    newFacts = []
    for i, fact in enumerate(facts):
        facts[i] = facts[i].strip()
        # remove fact id '[1]'
        if re.search("\[\d+\]", facts[i]):
            facts[i] = fact[4:]  # this gets rid of the [12] tags in front of each fact
        # replace money amount with 'argent'
        facts[i] = re.sub("[\d*\s*]*\d+[,]?\d*\s*\$", " argent ", facts[i])
        # lower case the fact
        facts[i] = facts[i].lower()

        # replace time value with 'heure'
        facts[i] = re.sub("\d+h\d*", " heure ", facts[i])
        # replace date value with 'date'
        facts[i] = re.sub("\d+-\d+-\d+", " date ", facts[i])
        facts[i] = re.sub("\d+.{0,2}?\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s+(\d{4}))?", " date ", facts[i])
        facts[i] = re.sub(
            "(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})",
            " date ", facts[i])
        # replace month values with 'moisDanslannee'
        facts[i] = re.sub(
            "(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)",
            " moisDanslannee ", facts[i])

        facts[i] = re.sub(
            "-le",
            " le", facts[i])
        match = re.search("\.([a-z][a-z])", facts[i])
        if match is not None:
            facts[i] = facts[i][:match.start()] + '. ' + facts[i][match.start()+1:]

    return facts
