import re
from wordfreq import zipf_frequency

def orangutang(file):
    f = open(file, "r", encoding="utf-8")
    itxt = f.read()
    f.close()

    if "_" in itxt or "-" in itxt or "'" in itxt:
        raise ValueError("contains unhandled characters")
    
    stxt = itxt.split(" ")
    otxt = ""

    for word in stxt:
        map = {
            "ok": list("AOU"),
            "ook": list("BP"),
            "okk": list("CSZ"),
            "Ok": list("DT"),
            "oK": list("EIY"),
            "ookk": list("FVW"),
            "OK": list("GKQX"),
            "Ookk": list("H"),
            "oOkk": list("J"),
            "oOKk": list("L"),
            "OokK": list("MN"),
            "oOkK": list("R"),
        }

        ooks = re.split(r"(?i)(?<=k)(?=o)", word)
        ltr_list = [[] for i in range(len(ooks))]

        for i in range(len(ooks)):
            for k, v in map.items():
                if ooks[i] == k:
                    ltr_list[i] = v

        def combine(ltr_list):
            if len(ltr_list) == 1:
                return ltr_list[0]
            m = [a + b for a in ltr_list[0] for b in ltr_list[1]]
            ltr_list = [m] + ltr_list[2:]
            return combine(ltr_list)
        comb = combine(ltr_list)
        words = []
        print(comb)

        for a in comb:
            if zipf_frequency(a, "en") > 0.0:
                words.append(a)

        if len(words) == 0:
            otxt += "<no valid words>"
        elif len(words) > 1:
            otxt += "<" + ", ".join(words) + ">"
        else:
            otxt += words[0]
        otxt += " "
    
    o = open(file + "_translated.txt", "w", encoding="utf-8")
    o.write(otxt)
    o.close()

def human(file):
    f = open(file, "r", encoding="utf-8")
    itxt = f.read()
    f.close()

    map = {
        "AOU": "ok",
        "BP": "ook",
        "CSZ": "okk",
        "DT": "Ok",
        "EIY": "oK",
        "FVW": "ookk",
        "GKQX": "OK",
        "H": "Ookk",
        "J": "oOkk",
        "L": "oOKk",
        "MN": "OokK",
        "R": "oOkK",
    }

    otxt = ""
    for c in itxt:
        u = c.upper()
        ook = None
        for k, v in map.items():
            if u in k:
                ook = v
                break
        if ook:
            otxt += ook
        else:
            otxt += c

    o = open(file + "_translated.txt", "w", encoding="utf-8")
    o.write(otxt)
    o.close()


# orangutang("ok.txt")
human("example.txt")