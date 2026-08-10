import json
import hashlib
import os

sub_dir = r"C:\Users\11932\Documents\Codex\2026-08-10\https-github-com-open-city-ai\work\haidian\submissions\RubenCampoa\jingzhang-ai-commons"

# 1. Update metrics.json textual consistency
metrics_path = os.path.join(sub_dir, "metrics.json")
with open(metrics_path, "r", encoding="utf-8") as f:
    metrics = json.load(f)

if "site_area_sqm" in metrics.get("metrics", {}):
    metrics["metrics"]["site_area_sqm"]["confidence"] = "medium"
    metrics["metrics"]["site_area_sqm"]["assumptions"] = ["Provisional/submitted boundary is used for calculation as official polygon is pending."]

with open(metrics_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)
    f.write("\n")

# 2. Re-hash everything that is in manifest.json (except manifest.json itself)
manifest_path = os.path.join(sub_dir, "manifest.json")
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for item in manifest.get("files", []):
    rel_path = item.get("path")
    if rel_path == "manifest.json":
        continue
    
    f_path = os.path.join(sub_dir, rel_path)
    if os.path.exists(f_path):
        with open(f_path, "rb") as f:
            item["sha256"] = hashlib.sha256(f.read()).hexdigest()

with open(manifest_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Updated metrics, manifest and rehashed all files with LF explicitly.")
