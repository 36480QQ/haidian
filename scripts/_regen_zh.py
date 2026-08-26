# -*- coding: utf-8 -*-
"""Regenerate the ZH (Chinese) figures using the current source (no EN patches).
Restores Chinese figures that the EN generator may have overwritten."""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCRIPTS = Path(r"C:/Users/wengyongsheng/Desktop/open-city-ai/haidian/scripts")
sys.path.insert(0, str(SCRIPTS))
REPO = SCRIPTS.parent
SUB = REPO / "submissions" / "wengyongsheng29-spec" / "jingzhang-agent-native-belt"
FIG_DIR = SUB / "assets" / "figures"

import gen_figures_real as g
g.REPO = REPO; g.SUB = SUB; g.FIG_DIR = FIG_DIR

# Ensure ZH savefig goes to plain names (the EN patch redirects known base names
# to .en.png; here we do NOT import that patch, so plain names stay ZH).
for name, fn in [
    ("site-overview", g.fig_site_overview),
    ("land-use-structure", g.fig_land_use),
    ("key-areas", g.fig_key_areas),
    ("mobility-bluegreen", g.fig_mobility),
    ("metrics-evidence", g.fig_metrics),
    ("concept-section", g.fig_section),
    ("implementation-roadmap", g.fig_roadmap),
    ("site-readiness", g.fig_site_readiness),
    ("ai-typologies", g.fig_ai_typologies),
    ("protocol-1909", g.fig_protocol_1909),
]:
    try:
        fn()
        print(f"OK  {name}.png")
    except Exception as e:
        print(f"ERR {name}.png: {e}")
print("ALL ZH DONE")
