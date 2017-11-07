import re


def preprocessing(facts):
    """
    Takes a list of strings and removes/replaces words such that they map to a common word. 
    Also remove unnecessary words/phrases
    
    :param facts: list of strings 
    :return: sanitized list of strings
    """
    months = "janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre"

    for i, fact in enumerate(facts):
        facts[i] = facts[i].strip()

        # remove fact id '[1]'
        if re.search("\[\d+\]", facts[i]):
            match = re.search("[A-Za-z]", facts[i])
            if match is not None:
                facts[i] = fact[match.start():]  # this gets rid of the [12] tags in front of each fact

        # replace money amount
        facts[i] = re.sub("[\d*\s*]*\d+[,]?\d*\s*\$", " argent ", facts[i])

        # lower case the fact
        facts[i] = facts[i].lower()

        # replace time value
        facts[i] = re.sub("\d+h\d*", " heure ", facts[i])

        # replace date value
        facts[i] = re.sub("\d+-\d+-\d+", " date ", facts[i])
        facts[i] = re.sub(
            "\d+.{0,2}?\s+(" + months + ")(\s+(\d{4}))?",
            " date ", facts[i])
        facts[i] = re.sub(
            "(" + months + ")\s+(\d{4})",
            " date ", facts[i])

        # replace month values
        facts[i] = re.sub(
            "(" + months + ")",
            " nom_du_mois ", facts[i])

        # remove hyphens
        facts[i] = re.sub("-le", " le", facts[i])

        # separate period(.) from words
        match = re.search("\.([a-z][a-z])", facts[i])
        if match is not None:
            facts[i] = facts[i][:match.start()] + ". " + facts[i][match.start() + 1:]

        # map landlord to a common word
        facts[i] = re.sub("locatrice(s)?", "locateur", facts[i])

        facts[i] = re.sub("pour ces motifs, le tribunal", "", facts[i])

    return facts
