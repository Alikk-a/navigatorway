from collections import Counter

c = Counter()
in_copy = False
with open("dump.sql", encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.startswith("COPY public.naviway_page "):
            in_copy = True
            continue
        if in_copy:
            if line.strip() == "\\.":
                break
            parts = line.split("\t")
            if len(parts) >= 3:
                try:
                    c[int(parts[2])] += 1
                except ValueError:
                    pass

print("top pageparid in dump:", c.most_common(12))
for pid in (3, 5, 7, 11, 13, 15, 100):
    print(pid, c.get(pid, 0))
