# fun_festival_app.py
# "Meme & Prank Festival" — single Streamlit app combining:
# - Harmless troll pranks (fake update, endless progress, faux crash, etc.)
# - Safe Browser History Panic (clearly fictional + consent)
# - MemeFest generator (templates in ./memes/, uploads, download)
# - 67 cameo (stylized silhouette or user-uploaded cameo)
# - Chicken Chorus simulation (simulated 70,000,000 chickens singing "MAMMA MIA")
#
# IMPORTANT: This app intentionally avoids any claim of accessing private data.
# Only use images you have rights to. Use pranks responsibly.

import streamlit as st
import time
import random
import io
import os
import glob
import requests
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageOps

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Meme & Prank Festival 🤡🐔", page_icon="🎪", layout="wide")

# -------------------------
# Helper utilities
# -------------------------
def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_local_templates(folder="memes"):
    ensure_folder(folder)
    exts = ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp")
    files = []
    for e in exts:
        files.extend(glob.glob(os.path.join(folder, e)))
    return sorted(files)

def load_image_from_url(url, timeout=6):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content)).convert("RGBA")
    except Exception as e:
        st.warning(f"Couldn't load image from URL: {e}")
        return None

def pil_fit_max(img, max_size=(800,800)):
    img.thumbnail(max_size, Image.LANCZOS)
    return img

def get_font(size):
    # Try Impact-like font if available, else default
    try:
        return ImageFont.truetype("Impact.ttf", size=size)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size=size)
        except Exception:
            return ImageFont.load_default()

def draw_meme_text(img: Image.Image, top_text: str, bottom_text: str):
    image = img.convert("RGBA")
    draw = ImageDraw.Draw(image)
    w, h = image.size

    def draw_outlined_text(text, pos_y, font_size_pct=0.08):
        font_size = max(12, int(h * font_size_pct))
        font = get_font(font_size)
        margin = int(w*0.05)
        text_w, text_h = draw.textsize(text, font=font)
        while text_w > (w - margin*2) and font_size > 10:
            font_size = int(font_size * 0.9)
            font = get_font(font_size)
            text_w, text_h = draw.textsize(text, font=font)

        x = (w - text_w) / 2
        y = pos_y
        stroke = max(2, int(font_size/12))
        for dx in range(-stroke, stroke+1):
            for dy in range(-stroke, stroke+1):
                if dx==0 and dy==0:
                    continue
                draw.text((x+dx, y+dy), text, font=font, fill=(0,0,0,255))
        draw.text((x, y), text, font=font, fill=(255,255,255,255))

    if top_text:
        draw_outlined_text(top_text.upper(), pos_y=int(h*0.02), font_size_pct=0.09)
    if bottom_text:
        font_size = max(12, int(h * 0.09))
        font = get_font(font_size)
        text_w, text_h = draw.textsize(bottom_text, font=font)
        pos_y = h - text_h - int(h*0.02)
        draw_outlined_text(bottom_text.upper(), pos_y=pos_y, font_size_pct=0.09)
    return image.convert("RGB")

# Basic caption corpus for Memefest
CAPTIONS = [
    "When you open Python and nothing explodes",
    "Me: I'll go to bed early. Also me at 3 AM:",
    "Modern problems require modern solutions",
    "I don't always test my code, but when I do — I do it in production",
    "A wild bug appeared",
    "That feeling when the CI passes first try",
    "No one: Absolutely no one: Me:",
    "Expectation vs Reality",
    "This is fine.",
    "404: motivation not found",
    "It was at this moment he knew... he messed up",
    "Insert witty caption here",
    "I regret nothing",
    "Say less",
    "We live in a society (but with better memes)",
]

# -------------------------
# App layout & sidebar
# -------------------------
st.title("Meme & Prank Festival 🤡🐔 — All pranks are staged, fictional, and consent-first")
st.write("This app combines playful pranks and a meme generator. Everything is fictional: the app cannot access real browser history or personal data. Use responsibly and only on consenting friends.")

modes = [
    "Troll Modes (gentle pranks)",
    "Browser History Panic (safe joke)",
    "MemeFest (generator + 67 cameo)",
    "Chicken Chorus (simulated 70,000,000)",
]

mode = st.sidebar.radio("Choose a mode", modes)

if "last_prank" not in st.session_state:
    st.session_state.last_prank = "none"

st.sidebar.markdown("---")
st.sidebar.caption("All pranks: fictional & consent-based. Do not harass or threaten.")

st.write("Last prank run:", st.session_state.last_prank)
st.markdown("---")

# -------------------------
# 1) Troll Modes
# -------------------------
if mode == "Troll Modes (gentle pranks)":
    st.header("Troll Modes — Harmless Pranks")
    st.write("Choose a prank. All are theatrical and include undo/stop options.")

    prank = st.selectbox("Prank", [
        "Gentle Surprise (balloons/confetti)",
        "Endless Progress (slow progress bar)",
        "Fake Update (dramatic)",
        "Faux Crash (theatrical)",
        "Reverse Typing (fun)",
        "Random Mischief"
    ])

    def small_pause(t=0.5):
        time.sleep(t)

    if prank == "Gentle Surprise (balloons/confetti)":
        st.write("Light-hearted surprise.")
        if st.button("Tickle me"):
            st.info("Preparing surprise...")
            small_pause(0.7)
            st.balloons()
            st.success("Surprise delivered 🎉 — all in good fun.")
            st.session_state.last_prank = f"Gentle Surprise @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    elif prank == "Endless Progress (slow progress bar)":
        st.write("Start and watch a long, playful progress bar. Cancel anytime.")
        start = st.button("Start Endless Progress")
        cancel = st.button("Cancel")
        if start:
            progress = st.progress(0)
            info = st.empty()
            loop_limit = random.randint(80, 300)
            for i in range(loop_limit+1):
                if cancel:
                    info.warning("You cancelled the endless progress. Well done.")
                    break
                progress.progress(int((i/loop_limit)*100))
                info.text(f"Working... {int((i/loop_limit)*100)}%")
                time.sleep(0.06 + random.random()*0.04)
            else:
                progress.progress(100)
                info.success("Done! That took... surprisingly long.")
            st.session_state.last_prank = f"Endless Progress @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    elif prank == "Fake Update (dramatic)":
        st.write("Simulates a dramatic system update; always includes reveal and undo.")
        if st.button("Begin Update"):
            placeholder = st.empty()
            # typing simulation
            text = "Downloading update package..."
            s = ""
            for ch in text:
                s += ch
                placeholder.text(s + "▌")
                time.sleep(0.03)
            placeholder.text(s)
            small_pause(0.4)
            p = st.progress(0)
            for i in range(101):
                p.progress(i)
                time.sleep(0.03)
                if i == 50:
                    st.warning("Applying compatibility patch...")
            st.success("Update complete. Phew — nothing actually changed.")
            if st.button("Show Confetti"):
                st.balloons()
            st.session_state.last_prank = f"Fake Update @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    elif prank == "Faux Crash (theatrical)":
        st.write("Shows a scary crash banner, then reveals it's fake and offers undo.")
        if st.button("Trigger Faux Crash"):
            st.markdown(
                """
                <div style="background:#8b0000;padding:20px;border-radius:10px;color:white;">
                <h2 style="margin:0;">SYSTEM ERROR</h2>
                <p style="margin:0;font-weight:600;">Critical failure detected. Reboot recommended.</p>
                </div>
                """, unsafe_allow_html=True
            )
            time.sleep(1.2)
            st.error("...just kidding. No data harmed. 😅")
            if st.button("Undo the joke"):
                st.success("Undo complete. Smile restored.")
            st.session_state.last_prank = f"Faux Crash @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    elif prank == "Reverse Typing (fun)":
        st.write("Type text and see it typed backwards slowly.")
        text = st.text_input("Text to reverse", "Hello friend!")
        if st.button("Show reversed"):
            placeholder = st.empty()
            rev = text[::-1]
            s = ""
            for ch in rev:
                s += ch
                placeholder.text(s + "▌")
                time.sleep(0.04)
            placeholder.text(s)
            st.session_state.last_prank = f"Reverse Typing @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    else:  # Random Mischief
        if st.button("Unleash Mischief"):
            choice = random.choice(["gentle","progress","fake_update","crash","typing"])
            st.info("Picking a mischief...")
            time.sleep(0.6)
            if choice == "gentle":
                st.balloons()
                st.success("Balloons! Cute.")
            elif choice == "progress":
                p = st.progress(0)
                for i in range(101):
                    p.progress(i)
                    time.sleep(0.02)
                st.success("That was fast mischief.")
            elif choice == "fake_update":
                st.warning("Applying unsafe update...")
                time.sleep(0.6)
                st.success("All safe. Mischief complete.")
            elif choice == "crash":
                st.markdown("<h3 style='color:orange'>Temporary chaos averted.</h3>", unsafe_allow_html=True)
            else:
                st.write("surprise!")
            st.session_state.last_prank = f"Random Mischief ({choice}) @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# -------------------------
# 2) Browser History Panic (safe)
# -------------------------
elif mode == "Browser History Panic (safe joke)":
    st.header("Browser History Panic — SAFE JOKE")
    st.write("This is purely theatrical. This app CANNOT access your real browser history.")
    st.write("The prank shows an alarming message for a moment then immediately reveals it's fake. Consent required to view a 'fake preview'.")

    consent = st.checkbox("I consent to being shown a clearly fake browser-history preview (for laughs).")
    if st.button("Trigger Fake Leak"):
        st.markdown(
            """
            <div style="background:#8b0000;padding:18px;border-radius:10px;color:white;">
            <h2 style="margin:0;">!!! URGENT !!!</h2>
            <p style="margin:0;font-weight:700;">I released your browser history.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(1.1)
        st.error("Scary message above? Take a breath.")
        st.success("Relax — it's theatrical. Nothing was accessed.")
        st.info("Below is a completely fictional 'preview' (made up entries) — only shown if you ticked consent.")

        if not consent:
            st.warning("Consent required to view the fake preview. Check the box if this is a harmless joke between friends.")
        else:
            # generate obviously silly fake entries
            sites_fun = [
                "pineapple-on-pizza-fanclub.example",
                "how-to-train-your-dragon-actually.example",
                "definitely-not-your-searches.example/awful-ideas",
                "cats-in-socks-enthusiasts.example",
                "top-secret-cookie-recipes.example",
                "conspiracy-theory-about-toast.example",
                "mystery-novel-plot-generator.example",
            ]
            now = datetime.now()
            fake_entries = []
            for i in range(6):
                timestamp = (now - timedelta(minutes=random.randint(1, 60*24*30))).strftime("%Y-%m-%d %H:%M")
                site = random.choice(sites_fun) + f"/fun-{random.randint(1,999)}"
                fake_entries.append({"time": timestamp, "site": site})
            st.markdown("**Fictional preview (for laughs only):**")
            for idx, e in enumerate(fake_entries, start=1):
                st.write(f"{idx}. **{e['time']}** — {e['site']}  — *(completely fake — funny entry)*")
            st.caption("All entries above are fabricated. This app cannot access real browser data.")

        st.markdown("---")
        if st.button("Undo / Reveal Truth"):
            st.success("All good — nothing was accessed. Keep it friendly! 😊")
        st.session_state.last_prank = f"Browser History Panic (safe joke) @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# -------------------------
# 3) MemeFest (generator + 67 cameo)
# -------------------------
elif mode == "MemeFest (generator + 67 cameo)":
    st.header("MemeFest — Generate memes, add cameo, Meme Storm")
    st.write("Add templates into `./memes/` or upload one. The app won't use any real-person images unless you upload them (only upload images you have rights to).")

    ensure_folder("memes")
    templates = load_local_templates("memes")
    st.sidebar.markdown(f"Local meme templates: **{len(templates)}** (drop images into ./memes/ to expand)")

    sub_mode = st.selectbox("MemeFest action", [
        "Generate a single meme",
        "Meme Storm (rapid slideshow)",
        "Upload / manage library",
        "Randomize captions & batch download"
    ])

    # Shared cameo UI (used in generation)
    st.markdown("### Cameo: 67 (stylized or upload your own)")
    cameo_mode = st.radio("Cameo source", ["None", "Upload your own 67 image", "Stylized 67 silhouette (safe)"], index=0, key="cameo_mode")
    cameo_opacity = st.slider("Cameo opacity (background)", 10, 100, 35, key="cameo_opacity")
    cameo_scale = st.slider("Cameo size (percentage of canvas)", 10, 50, 20, key="cameo_scale")
    cameo_position = st.selectbox("Cameo position", ["bottom-right", "bottom-left", "top-right", "top-left", "center"], key="cameo_position")

    cameo_upload = None
    if cameo_mode == "Upload your own 67 image":
        cameo_upload = st.file_uploader("Upload 67 image (use only images you have rights to)", type=["png","jpg","jpeg","webp","gif"], key="cameo_upload")

    def draw_67_silhouette(size_px):
        W = max(64, size_px)
        H = W
        img = Image.new("RGBA", (W, H), (0,0,0,0))
        d = ImageDraw.Draw(img)
        # body
        body_w, body_h = int(W*0.5), int(H*0.55)
        body_x = (W - body_w)//2
        body_y = int(H*0.30)
        d.rounded_rectangle([body_x, body_y, body_x+body_w, body_y+body_h], radius=10, fill=(40, 80, 160, 255))
        # head
        head_r = int(W*0.18)
        head_cx = W//2
        head_cy = int(H*0.18)
        d.ellipse([head_cx-head_r, head_cy-head_r, head_cx+head_r, head_cy+head_r], fill=(255, 224, 140, 255))
        # hair
        d.rectangle([head_cx-head_r, head_cy-head_r-4, head_c_]()
