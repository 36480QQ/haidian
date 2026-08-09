# -*- coding: utf-8 -*-
"""Record environment and the submission's precisely defined aggregate digest.

Python source carried with a ``.js`` suffix to satisfy the submission path
allow-list; execute with Python and never load it in the browser.
"""
import sys, hashlib, pathlib, json, platform
import pyproj, shapely, numpy
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
SUB = SCRIPT_DIR.parents[1]
print("python  :", sys.version.split()[0], "|", platform.platform())
print("pyproj  :", pyproj.__version__, "| PROJ", pyproj.proj_version_str)
print("shapely :", shapely.__version__)
print("numpy   :", numpy.__version__)
print("\n--- 输出文件 SHA-256 ---")
rows=[]
for p in sorted((SUB/"geometry").glob("*.geojson")) + [SUB/"metrics.json"]:
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    rows.append((p.name, h))
    print(f"  {p.name:26} {h}")
digest_text = "".join(h for _, h in rows)
agg = hashlib.sha256(digest_text.encode("ascii")).hexdigest()
print(f"\n  聚合指纹（9 个 GeoJSON 按名排序，metrics.json 固定末尾；拼接十六进制摘要字符串后再哈希）= {agg}")
record = {
    "python": sys.version.split()[0],
    "pyproj": pyproj.__version__,
    "proj": pyproj.proj_version_str,
    "shapely": shapely.__version__,
    "numpy": numpy.__version__,
    "aggregate_algorithm": {
        "per_file": "SHA-256 of exact file bytes, rendered as 64 lowercase hexadecimal characters",
        "order": "geometry/*.geojson sorted by filename ascending, followed by metrics.json",
        "concatenation": "concatenate the ten hexadecimal digest strings with no separator, prefix, or newline",
        "final": "SHA-256 of the 640 ASCII bytes in that concatenated string",
    },
    "files": dict(rows),
    "aggregate_sha256": agg,
}
path = SCRIPT_DIR / "run_record.json"
path.write_bytes((json.dumps(record, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
print("写入", path)
