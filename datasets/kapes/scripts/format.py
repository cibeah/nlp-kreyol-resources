from pathlib import Path

folder = Path("texts/")

for file in folder.glob("*.txt"):
    with file.open("r", encoding="utf-8") as fp:
        alltext = fp.read()
    alltext = alltext.replace("\n", " ")
    lines = alltext.split(". ")
    with file.open("w", encoding="utf-8") as fp:
        alltext = fp.write("\n".join(lines))
