from pathlib import Path
import sys

file_path = Path(sys.argv[1])

content = file_path.read_text(encoding="utf-8")

# 删除所有空行（包括空格、Tab 组成的行）
lines = [
    line
    for line in content.splitlines()
    if line.strip()
]

file_path.write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8",
)

print(f"已清理: {file_path}")
