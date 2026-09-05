import csv
from pympler import asizeof

filename = "q_table1.csv"
max_rows = 100000

q_table = {}


def fast_tuple(text):
    return tuple(
        int(x)
        for x in text[1:-1].split(",")
        if x.strip()
    )


with open(filename, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)

    for i, row in enumerate(reader, start=1):

        state = fast_tuple(row[0])
        action = fast_tuple(row[1])
        q = float(row[2])

        if state not in q_table:
            q_table[state] = {}

        q_table[state][action] = q

        if i % 10000 == 0:
            print(f"{i:,} 行読み込み済み")

        if i >= max_rows:
            break


size_bytes = asizeof.asizeof(q_table)
size_gb = size_bytes / 1024**3

print()
print(f"測定行数: {max_rows:,}")
print(f"state数: {len(q_table):,}")
print(f"メモリ使用量: {size_gb:.3f} GB")

estimated_gb = size_gb * (3_000_000 / max_rows)

print(f"300万行単純推定: 約 {estimated_gb:.2f} GB")