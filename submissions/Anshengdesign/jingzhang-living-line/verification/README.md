# 可复算脚本说明

本目录收录方案全部 15+ 项计算的本地脚本（Python + shapely/networkx/numpy/pyproj/matplotlib）。
- 数据依赖：研究数据/poi_wgs84/*.json（高德 POI，12 类 25,476 点）、osm/*.json（OSM 现状）、
  site_model.pkl、design_geometry/*.geojson——因体积与许可原因，原始数据不随包提交；
  脚本与输出（计算/*.json 摘要）的数字已全部登记于 metrics.json 与本包正文。
- 运行方式：`python3 c1_wilson.py` 等（依赖 requirements-review.txt + networkx/matplotlib）。
- 口径与 caveat：各脚本头部与 metrics.json 的 assumptions 字段完整声明代理口径。
