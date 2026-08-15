# -*- coding: utf-8 -*-
"""高德 POI 抓取管线（京张AI创新带）
- Web Service Key: d0df0f722aa9967bbc08947b15540973（无需签名，实测可用）
- 网格分块多边形查询，规避单查询 600 条上限
- GCJ-02 → WGS84 转换（淀山湖数据纪律：统一坐标，禁止手工偏移）
- 12 大类 POI = 市民工作/生活/创业/休闲/健康/养老/科技发展的"看不见的动力"
输出：poi_raw/{cat}.json（原始）→ poi_wgs84/{cat}.json（转换后）
"""
import json, os, time, math, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "poi_raw"); WGS = os.path.join(HERE, "poi_wgs84")
os.makedirs(RAW, exist_ok=True); os.makedirs(WGS, exist_ok=True)

KEY = "d0df0f722aa9967bbc08947b15540973"
LON0, LAT0, LON1, LAT1 = 116.318, 39.930, 116.378, 40.040   # 略大于研究范围
TILE = 0.02

CATEGORIES = [
    ("170000", "company", "公司企业"),
    ("141200", "school", "学校"),
    ("141400", "research", "科研机构"),
    ("090000", "medical", "医疗保健"),
    ("080000", "sports", "体育休闲"),
    ("050000", "dining", "餐饮服务"),
    ("060000", "shopping", "购物服务"),
    ("070000", "living", "生活服务"),
    ("120000", "residential", "商务住宅"),
    ("110000", "scenic", "风景名胜"),
    ("150000", "transport", "交通设施"),
    ("160000", "finance", "金融保险"),
]

def tiles():
    ts = []
    lon = LON0
    while lon < LON1:
        lat = LAT0
        while lat < LAT1:
            ts.append((round(lon, 6), round(lat, 6), round(min(lon + TILE, LON1), 6), round(min(lat + TILE, LAT1), 6)))
            lat += TILE
        lon += TILE
    return ts

def fetch_polygon(poly, types, page):
    p = {"polygon": poly, "types": types, "offset": 25, "page": page, "extensions": "base", "key": KEY}
    qs = "&".join(f"{k}={v}" for k, v in p.items())
    url = f"https://restapi.amap.com/v3/place/polygon?{qs}"
    with urllib.request.urlopen(url, timeout=25) as r:
        return json.loads(r.read().decode())

def collect(types):
    all_pois = {}
    for t in tiles():
        poly = f"{t[0]},{t[1]}|{t[2]},{t[1]}|{t[2]},{t[3]}|{t[0]},{t[3]}"
        page = 1
        while page <= 24:   # 每 tile 最多 600 条
            try:
                j = fetch_polygon(poly, types, page)
            except Exception as e:
                print(f"  ERR {types} {t[:2]} p{page}: {e}")
                break
            if j.get("status") != "1":
                if j.get("infocode") == "10009":
                    print("  KEY FAILED"); return None
                break
            pois = j.get("pois", [])
            for poi in pois:
                pid = poi.get("id")
                if pid not in all_pois:
                    all_pois[pid] = poi
            if len(pois) < 25:
                break
            page += 1
            time.sleep(0.12)
        time.sleep(0.10)
    return list(all_pois.values())

# GCJ-02 → WGS84
A = 6378245.0; EE = 0.00669342162296594323
def _out_of_china(lon, lat):
    return not (72.004 <= lon <= 137.8347 and 0.8293 <= lat <= 55.8271)
def _transform_lat(x, y):
    ret = -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*x*y + 0.2*math.sqrt(abs(x))
    ret += (20.0*math.sin(6.0*x*math.pi) + 20.0*math.sin(2.0*x*math.pi)) * 2.0/3.0
    ret += (20.0*math.sin(y*math.pi) + 40.0*math.sin(y/3.0*math.pi)) * 2.0/3.0
    ret += (160.0*math.sin(y/12.0*math.pi) + 320*math.sin(y*math.pi/30.0)) * 2.0/3.0
    return ret
def _transform_lon(x, y):
    ret = 300.0 + x + 2.0*y + 0.1*x*x + 0.1*x*y + 0.1*math.sqrt(abs(x))
    ret += (20.0*math.sin(6.0*x*math.pi) + 20.0*math.sin(2.0*x*math.pi)) * 2.0/3.0
    ret += (20.0*math.sin(x*math.pi) + 40.0*math.sin(x/3.0*math.pi)) * 2.0/3.0
    ret += (150.0*math.sin(x/12.0*math.pi) + 300.0*math.sin(x/30.0*math.pi)) * 2.0/3.0
    return ret
def gcj2wgs(lon, lat):
    if _out_of_china(lon, lat):
        return lon, lat
    dlat = _transform_lat(lon - 105.0, lat - 35.0)
    dlon = _transform_lon(lon - 105.0, lat - 35.0)
    radlat = lat/180.0*math.pi
    magic = math.sin(radlat)
    magic = 1 - EE*magic*magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat*180.0)/((A*(1-EE))/(magic*sqrtmagic)*math.pi)
    dlon = (dlon*180.0)/(A/sqrtmagic*math.cos(radlat)*math.pi)
    return lon - dlon, lat - dlat

def convert(pois):
    out = []
    for p in pois:
        try:
            lon, lat = map(float, p["location"].split(","))
            wlon, wlat = gcj2wgs(lon, lat)
            out.append({
                "id": p.get("id"), "name": p.get("name"), "type": p.get("type"),
                "typecode": p.get("typecode"), "address": p.get("address"),
                "lon_wgs": round(wlon, 6), "lat_wgs": round(wlat, 6),
                "lon_gcj": lon, "lat_gcj": lat,
                "pname": p.get("pname"), "cityname": p.get("cityname"),
                "adname": p.get("adname"), "biz_type": p.get("biz_type", ""),
            })
        except Exception:
            continue
    return out

total = 0
for typecode, slug, zh in CATEGORIES:
    print(f"== {zh} ({typecode}) ==")
    pois = collect(typecode)
    if pois is None:
        break
    json.dump(pois, open(os.path.join(RAW, f"{slug}.json"), "w"), ensure_ascii=False)
    w = convert(pois)
    json.dump(w, open(os.path.join(WGS, f"{slug}.json"), "w"), ensure_ascii=False)
    print(f"   {zh}: raw={len(pois)} converted={len(w)}")
    total += len(w)
    time.sleep(0.3)
print("TOTAL WGS84 POIs:", total)
