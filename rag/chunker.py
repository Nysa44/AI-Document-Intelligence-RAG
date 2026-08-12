import re

def normalize_text(text):
    text=text.replace("\x00"," ")
    return re.sub(r"\s+"," ",text).strip()

def chunk_text(text,chunk_size=850,overlap=120):
    words=normalize_text(text).split()
    step=max(1,chunk_size-overlap)
    return [" ".join(words[i:i+chunk_size]) for i in range(0,len(words),step)
            if len(words[i:i+chunk_size])>=20]
