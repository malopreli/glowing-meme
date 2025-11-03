# max_chaos_full.py
import streamlit as st
import threading
import random
import time

st.set_page_config(page_title="MAX CHAOS Chicken Meme Apocalypse", page_icon="🔥🐔", layout="wide")
st.title("MAX CHAOS Meme Apocalypse 🐔💨")
st.write("Press START for full chaos. STOP ends it immediately. Everything is simulated and safe.")

# Initialize session state
if "stop_flag" not in st.session_state:
    st.session_state.stop_flag = True  # initially stopped

# Placeholders
placeholder_main = st.empty()
placeholder_memes = st.empty()
placeholder_chickens = st.empty()

# Goofy colors
COLORS = ['#ff0077','#00ff88','#33ccff','#ffcc00','#ff4444','#7a5cff',
          '#ff6600','#00ffee','#ff00ff','#ff99cc','#00ccff','#ffbb33','#88ff00','#ff0066','#cc00ff']

# Meme generation
TEMPLATES = ["When you","Me when","POV:","Nobody:","Also me:","Expectation:","Reality:","Plot twist:"]
ACTIONS = ["open the project","run the build","see 0 tests fail","your dog walks on your keyboard","the coffee kicks in","your Wi-Fi dies"]
SUBJECTS = ["in production","at 3 AM","during standup","before breakfast","right after deployment"]

def generate_memes(n=10000):
    memes = []
    for _ in range(n):
        meme = f"{random.choice(TEMPLATES)} {random.choice(ACTIONS)} {random.choice(SUBJECTS)} 💀🤣🔥"
        memes.append(meme)
    return memes

# Pranks
def fake_update():
    placeholder_main.markdown(f"<div style='color:{random.choice(COLORS)}; font-size:32px; font-weight:900;'>Installing updates...</div>", unsafe_allow_html=True)
    time.sleep(2)

def meme_flood():
    memes = generate_memes(2000)
    for meme in memes:
        if st.session_state.stop_flag: return
        placeholder_memes.markdown(f"<div style='color:{random.choice(COLORS)}; font-size:{random.randint(14,28)}px;'>{meme}</div>", unsafe_allow_html=True)
        time.sleep(0.02)
    placeholder_memes.empty()

def browser_history_prank():
    placeholder_main.markdown(f"<div style='background-color:#220022;color:#ff0077;padding:20px;border-radius:10px;'>I released your browser history 💀</div>", unsafe_allow_html=True)
    fake_entries = [
        "2025-11-03 09:12 — pineapple-on-pizza-fanclub.example",
        "2025-11-02 22:01 — cats-in-socks-enthusiasts.example",
        "2025-10-31 18:44 — how-to-build-a-rockets-not-really.example",
        "2025-10-10 07:30 — definitely-not-your-searches.example",
        "2025-09-25 12:15 — dancing-llamas-2025.example",
        "2025-08-18 20:40 — ultra-goofy-meme-factory.example"
    ]
    for entry in fake_entries:
        if st.session_state.stop_flag: return
        placeholder_main.markdown(f"<div style='color:{random.choice(COLORS)}; padding:5px;'>{entry} (fake)</div>", unsafe_allow_html=True)
        time.sleep(3.2)
    placeholder_main.markdown(f"<div style='color:{random.choice(COLORS)}; padding:10px;'>...just kidding. Relax — this is a joke 😎</div>", unsafe_allow_html=True)

def chicken_chorus():
    placeholder_main.markdown(f"<div style='color:{random.choice(COLORS)}; font-size:28px;'>🐔🐔🐔 Chicken jokes galore 🐔🐔🐔</div>", unsafe_allow_html=True)
    # flying spinning chickens
    for _ in range(20):  # multiple frames
        if st.session_state.stop_flag: return
        chickens = []
        for _ in range(50):
            left = random.randint(0, 80)
            top = random.randint(0, 80)
            rot = random.randint(0, 360)
            emoji = random.choice(["🐔","🐓","🐤"])
            chickens.append(f"<div style='position:absolute; left:{left}%; top:{top}%; transform: rotate({rot}deg); font-size:{random.randint(20,40)}px;'>{emoji}</div>")
        html = "<div style='position:relative; width:100%; height:400px;'>" + "".join(chickens) + "</div>"
        placeholder_chickens.markdown(html, unsafe_allow_html=True)
        time.sleep(0.2)
    placeholder_chickens.empty()

def max_volume_67():
    for _ in range(10):
        if st.session_state.stop_flag: return
        placeholder_main.markdown(f"<div style='color:{random.choice(COLORS)}; font-size:48px; font-weight:900;'>🔊 MAX VOLUME 67 🔊</div>", unsafe_allow_html=True)
        time.sleep(0.1)

# Main prank loop
def prank_loop():
    pranks = [fake_update, meme_flood, browser_history_prank, chicken_chorus, max_volume_67]
    while not st.session_state.stop_flag:
        prank = random.choice(pranks)
        prank()
        time.sleep(random.uniform(cycle_min/1000, cycle_max/1000))

# Buttons
start = st.button("START")
stop = st.button("STOP")

if start:
    if st.session_state.stop_flag:
        st.session_state.stop_flag = False
        threading.Thread(target=prank_loop, daemon=True).start()

if stop:
    st.session_state.stop_flag = True
    placeholder_main.markdown(f"<div style='color:#ffffff; font-size:28px;'>Stopped. Press START to chaos again.</div>", unsafe_allow_html=True)
    placeholder_memes.empty()
    placeholder_chickens.empty()

