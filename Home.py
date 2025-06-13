import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="X 地圖標記", layout="wide")
st.title("📍 X（Twitter）帳號地圖標記工具")

st.markdown("請輸入帳號與地點（每行一筆，格式：`帳號, 地點`）")
user_input = st.text_area("輸入格式：帳號, 地點", height=200, placeholder="elonmusk, Austin, Texas\njack, New York")

if st.button("📌 產生地圖"):
    geolocator = Nominatim(user_agent="x_map_app")
    lines = user_input.strip().split('\n')

    markers = []
    for line in lines:
        if ',' not in line:
            st.warning(f"⚠️ 格式錯誤：{line}")
            continue
        username, location_text = [x.strip() for x in line.split(',', 1)]
        try:
            location = geolocator.geocode(location_text)
            if location:
                markers.append({
                    'username': username,
                    'location': location_text,
                    'lat': location.latitude,
                    'lon': location.longitude
                })
            else:
                st.warning(f"❗ 找不到地點：{location_text}")
        except Exception as e:
            st.error(f"錯誤：{location_text}（{e}）")

    if markers:
        m = folium.Map(location=[markers[0]['lat'], markers[0]['lon']], zoom_start=2)
        for marker in markers:
            folium.Marker(
                location=[marker['lat'], marker['lon']],
                tooltip=f"@{marker['username']}",
                popup=f"@{marker['username']}<br>{marker['location']}"
            ).add_to(m)
        st_folium(m, width=800, height=600)
    else:
        st.info("⚠️ 沒有成功標記任何位置")
