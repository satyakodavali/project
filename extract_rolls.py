import re

with open(r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\database\seed_data.sql', 'r') as f:
    data = f.read()

pattern = r"INSERT INTO students.*?VALUES \('(\w+)'.*?, (\d+), '"
rolls = re.findall(pattern, data)

y4 = sorted([r for r, y in rolls if y == '4'])
y3 = sorted([r for r, y in rolls if y == '3'])
y2 = sorted([r for r, y in rolls if y == '2'])

with open(r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\database\roll_numbers.txt', 'w') as out:
    out.write("ALL PASSWORDS: Pass123!\n")
    out.write("=" * 50 + "\n")
    
    out.write(f"\n=== 4th YEAR Students ({len(y4)}) ===\n")
    for r in y4:
        out.write(f"  {r}\n")

    out.write(f"\n=== 3rd YEAR Students ({len(y3)}) ===\n")
    for r in y3:
        out.write(f"  {r}\n")

    out.write(f"\n=== 2nd YEAR Students ({len(y2)}) ===\n")
    for r in y2:
        out.write(f"  {r}\n")

    out.write(f"\nTotal: {len(y4) + len(y3) + len(y2)} students (2nd-4th year)\n")

print("Done! Check roll_numbers.txt")
