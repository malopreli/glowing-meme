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
        d.rectangle([head_cx-head_r, head_cy-head_r-4, head_cx+head_r, head_cy-head_r+int(head_r/2)], fill=(240,200,60,255))
        # badge 67
        badge_r = int(W*0.18)
        badge_x = W - badge_r - int(W*0.05)
        badge_y = int(H*0.05)
        d.ellipse([badge_x, badge_y, badge_x+badge_r, badge_y+badge_r], fill=(220,40,40,230))
        try:
            f = ImageFont.truetype("Impact.ttf", size=int(badge_r*0.5))
        except Exception:
            f = ImageFont.load_default()
        text = "67"
        tw, th = d.textsize(text, font=f)
        d.text((badge_x + (badge_r - tw)/2, badge_y + (badge_r - th)/2 - 2), text, font=f, fill=(255,255,255,255))
        return img

    def composite_cameo(base_img_pil, cameo_img, opacity_pct=35, position="bottom-right", scale_pct=20):
        base = base_img_pil.convert("RGBA")
        W, H = base.size
        target_w = int(W * (scale_pct / 100.0))
        w0, h0 = cameo_img.size
        scale = target_w / float(w0)
        target_h = int(h0 * scale)
        cameo_resized = cameo_img.resize((target_w, target_h), Image.LANCZOS)
        # apply opacity
        alpha = cameo_resized.split()[-1].point(lambda p: int(p * (opacity_pct/100.0)))
        cameo_resized.putalpha(alpha)
        margin = int(W*0.03)
        if position == "bottom-right":
            pos = (W - target_w - margin, H - target_h - margin)
        elif position == "bottom-left":
            pos = (margin, H - target_h - margin)
        elif position == "top-right":
            pos = (W - target_w - margin, margin)
        elif position == "top-left":
            pos = (margin, margin)
        else:
            pos = ((W - target_w)//2, (H - target_h)//2)
        base.paste(cameo_resized, pos, cameo_resized)
        return base.convert("RGB")

    # Sub-modes
    if sub_mode == "Generate a single meme":
        col1, col2 = st.columns([1,2])
        with col1:
            st.subheader("Template selection")
            choice_method = st.radio("Choose template by:", ["Local template", "Upload now", "Image URL"], key="choice_method")
            base_img = None
            if choice_method == "Local template":
                if templates:
                    sel = st.selectbox("Select template", ["-- choose --"] + templates, key="sel_template")
                    if sel != "-- choose --":
                        try:
                            base_img = Image.open(sel)
                        except Exception as e:
                            st.error(f"Could not open template: {e}")
                else:
                    st.info("No local templates found. Upload images or add via URL in the sidebar.")
            elif choice_method == "Upload now":
                up = st.file_uploader("Upload image to generate meme from", type=["png","jpg","jpeg","gif","webp"], key="upload_now")
                if up:
                    base_img = Image.open(up)
            else:
                u = st.text_input("Image URL", key="img_url")
                if st.button("Load from URL", key="load_url_btn"):
                    if u:
                        im = load_image_from_url(u)
                        if im:
                            base_img = im

            st.markdown("---")
            st.subheader("Caption options")
            top_text = st.text_input("Top text", value=random.choice(CAPTIONS), key="top_text")
            bottom_text = st.text_input("Bottom text", value=random.choice(CAPTIONS), key="bottom_text")
            if st.checkbox("Randomize captions", value=False, key="rand_captions"):
                top_text = random.choice(CAPTIONS)
                bottom_text = random.choice(CAPTIONS)
            autofit = st.checkbox("Auto-fit/crop to meme aspect", value=True, key="autofit")
            generate = st.button("Generate Meme", key="generate_meme")

        with col2:
            st.subheader("Preview / Save")
            preview_area = st.empty()
            if base_img is None:
                preview_area.info("No template selected yet. Choose a local template, upload, or load from URL.")
            else:
                img_preview = pil_fit_max(base_img.copy(), max_size=(900,900))
                preview_area.image(img_preview, use_column_width=True)

            if generate and base_img is not None:
                img = base_img.copy()
                try:
                    if getattr(img, "is_animated", False):
                        img.seek(0)
                        img = img.convert("RGBA")
                except Exception:
                    img = img.convert("RGBA")
                if autofit:
                    img = pil_fit_max(img, max_size=(1200,1200))
                final = draw_meme_text(img, top_text, bottom_text)

                # Apply cameo if requested
                if cameo_mode != "None":
                    if cameo_mode == "Upload your own 67 image" and cameo_upload is not None:
                        try:
                            user_cameo = Image.open(cameo_upload).convert("RGBA")
                        except Exception:
                            user_cameo = None
                        cameo_src = user_cameo if user_cameo is not None else draw_67_silhouette(max(64, int(min(final.size)*0.2)))
                    else:
                        cameo_src = draw_67_silhouette(max(64, int(min(final.size)*0.2)))

                    final = composite_cameo(final, cameo_src, opacity_pct=cameo_opacity, position=cameo_position, scale_pct=cameo_scale)

                buf = io.BytesIO()
                final.save(buf, format="PNG")
                buf.seek(0)
                st.image(final, caption="Generated Meme with Cameo", use_column_width=True)
                st.download_button("Download Meme (PNG)", data=buf, file_name="meme_with_67.png", mime="image/png")

    elif sub_mode == "Meme Storm (rapid slideshow)":
        st.subheader("Meme Storm ⚡")
        st.write("Rapidly display a barrage of memes. Keep it fun and consensual.")
        speed = st.slider("Speed (ms per image)", 100, 2000, 350)
        count = st.slider("Number of memes to show", 5, 200, 30)
        allow_gifs = st.checkbox("Include GIFs (animated)", value=True)
        pool = []
        for t in templates:
            if not allow_gifs and t.lower().endswith(".gif"):
                continue
            pool.append(("file", t))
        for i in range(30):
            pool.append(("gen_caption", random.choice(CAPTIONS)))

        if len(pool) == 0:
            st.warning("No images available for Meme Storm — add templates or uploads.")
        else:
            st.info("Click Start to begin Meme Storm. Press Stop to end early.")
            start = st.button("Start Storm", key="storm_start")
            stop = st.button("Stop Storm", key="storm_stop")
            storm_area = st.empty()
            if start:
                for i in range(count):
                    if stop:
                        st.warning("Storm stopped by user.")
                        break
                    item = random.choice(pool)
                    if item[0] == "file":
                        path = item[1]
                        try:
                            if path.lower().endswith(".gif"):
                                with open(path, "rb") as f:
                                    storm_area.image(f.read())
                            else:
                                storm_area.image(path, use_column_width=True)
                        except Exception as e:
                            storm_area.write(f"Error showing {path}: {e}")
                    else:
                        caption = item[1]
                        bg = Image.new("RGB", (800, 600), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                        img = draw_meme_text(bg, caption, random.choice(CAPTIONS))
                        buf = io.BytesIO()
                        img.save(buf, format="PNG")
                        buf.seek(0)
                        storm_area.image(buf.getvalue())
                    time.sleep(speed/1000.0)
                st.success("Meme Storm complete!")

    elif sub_mode == "Upload / manage library":
        st.subheader("Manage your meme library")
        st.write("Drop images into the `memes/` folder or use the uploader below.")
        uploaded2 = st.file_uploader("Upload templates to add to library (multiples allowed)", accept_multiple_files=True, type=["png","jpg","jpeg","gif","webp"])
        if uploaded2:
            for f in uploaded2:
                try:
                    img = Image.open(f)
                    ensure_folder("memes")
                    filename = os.path.join("memes", f"{int(datetime.now().timestamp())}_{f.name}")
                    img.save(filename)
                    st.success(f"Saved {filename}")
                except Exception as e:
                    st.error(f"Couldn't save {f.name}: {e}")
            st.experimental_rerun()
        st.markdown("**Current library (first 40 shown):**")
        cols = st.columns(5)
        for idx, t in enumerate(templates[:40]):
            try:
                with cols[idx % 5]:
                    st.image(t, use_column_width=True)
                    if st.button(f"Remove {os.path.basename(t)}", key=f"rm{idx}"):
                        os.remove(t)
                        st.success(f"Removed {t}")
                        st.experimental_rerun()
            except Exception:
                continue

    else:  # Randomize captions & batch download
        st.subheader("Bake a meme batch")
        st.write("Create many randomized memes from your templates and download them as a zip.")
        if len(templates) == 0:
            st.warning("No templates in ./memes/. Add some first.")
        else:
            num_each = st.slider("Memes per template", 1, 20, 3)
            est_total = num_each * len(templates)
            st.write(f"Estimated total memes: {est_total}")
            if st.button("Generate batch (may take a moment)"):
                import zipfile
                zip_io = io.BytesIO()
                with zipfile.ZipFile(zip_io, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                    for t in templates:
                        try:
                            base = Image.open(t)
                            for i in range(num_each):
                                top = random.choice(CAPTIONS) if random.random()>0.15 else ""
                                bottom = random.choice(CAPTIONS) if random.random()>0.15 else ""
                                final = draw_meme_text(pil_fit_max(base.copy(), (1200,1200)), top, bottom)
                                # optionally apply cameo (simple chance)
                                if cameo_mode != "None" and random.random() < 0.6:
                                    cameo_src = draw_67_silhouette(max(64, int(min(final.size)*0.2)))
                                    final = composite_cameo(final, cameo_src, opacity_pct=cameo_opacity, position=cameo_position, scale_pct=cameo_scale)
                                buf = io.BytesIO()
                                final.save(buf, format="PNG")
                                buf.seek(0)
                                name = f"{os.path.splitext(os.path.basename(t))[0]}_{i}.png"
                                zf.writestr(name, buf.getvalue())
                        except Exception as e:
                            st.warning(f"Skipping {t}: {e}")
                zip_io.seek(0)
                st.download_button("Download meme batch (zip)", data=zip_io, file_name="memefest_batch.zip", mime="application/zip")
                st.success("Batch generated!")

# -------------------------
# 4) Chicken Chorus
# -------------------------
elif mode == "Chicken Chorus (simulated 70,000,000)":
    st.header("🐔 Chicken Chorus — Simulated 70,000,000 chickens singing 'MAMMA MIA' (theatrical)")
    st.write("This is a theatrical simulation only. It will not actually spawn 70 million elements. You must click to start audio (browsers block autoplay). A panic/STOP button is provided. Closing the tab is attempted only after confirmation (may be blocked by the browser).")

    requested_count = st.number_input("Simulate claimed chorus size (you can enter 70000000)", value=70000000, min_value=1, step=1)
    max_display = st.slider("Actual number of joke lines to render (keeps browser safe)", 10, 5000, 1500)
    duration_sec = st.slider("Chorus duration (seconds)", 3, 60, 12)

    CHICKEN_JOKES = [
        "Why did the chicken cross the playground? To get to the other slide!",
        "Why did the chicken join a band? Because it had the drumsticks!",
        "Why did the chicken sit in the middle of the road? It wanted to lay it on the line!",
        "What do chickens grow on? Eggplants!",
        "I'm not chicken, I'm poultry in motion!",
        "Do chickens like memes? Only if they're egg-ceptional.",
        "Chicken to the left of me, cluck to the right — here I am stuck in the meme tonight.",
        "Warning: excessive 'MAMMA MIA' may cause spontaneous dancing.",
    ]

    st.write("Click Start Chorus to begin. Use PANIC / STOP to halt immediately.")

    import streamlit.components.v1 as components

    html = f"""
    <div style="font-family: sans-serif;">
      <div style="margin-bottom:8px;">
        <strong>Claimed chorus size:</strong> {requested_count:,} (simulated)<br/>
        <strong>Rendering:</strong> {max_display} joke lines (actual to avoid freeze)<br/>
        <strong>Chorus length:</strong> {duration_sec} seconds
      </div>

      <div id="chicken-area" style="height:320px;border:1px solid #eee;padding:8px;overflow:auto;background:linear-gradient(180deg,#fff,#fff8f0);">
        <div style="color:#777">Waiting to start... press <em>Start Chorus</em>.</div>
      </div>

      <div style="margin-top:8px;">
        <button id="start-btn" style="padding:10px 16px;background:#ffcc00;border:none;border-radius:6px;font-weight:bold;cursor:pointer">Start Chorus</button>
        <button id="stop-btn" style="padding:10px 12px;margin-left:8px;background:#ff4444;border:none;border-radius:6px;color:white;cursor:pointer">PANIC / STOP</button>
      </div>

      <div id="close-area" style="margin-top:12px;"></div>
    </div>

    <script>
    (function(){{
      const jokes = {CHICKEN_JOKES};
      const requestedCount = {requested_count};
      const maxDisplay = {max_display};
      const durationSec = {duration_sec};
      let stopRequested = false;
      const chickenArea = document.getElementById("chicken-area");
      const startBtn = document.getElementById("start-btn");
      const stopBtn = document.getElementById("stop-btn");
      const closeArea = document.getElementById("close-area");

      function randomJoke(i) {{
        const j = jokes[Math.floor(Math.random()*jokes.length)];
        return `${{i+1}}. ${{j}} ${{'🐔'.repeat(((i%3)+1))}}`;
      }}

      function appendLine(text) {{
        const div = document.createElement("div");
        div.style.padding = "4px 0";
        div.textContent = text;
        chickenArea.appendChild(div);
        chickenArea.scrollTop = chickenArea.scrollHeight;
      }}

      function speakChorus(totalSeconds) {{
        if (!('speechSynthesis' in window)) {{
          console.warn("SpeechSynthesis API not available.");
          return;
        }}
        const synth = window.speechSynthesis;
        const endTime = Date.now() + (totalSeconds*1000);

        function speakOnce() {{
          if (stopRequested) return;
          if (Date.now() > endTime) return;

          const u = new SpeechSynthesisUtterance("MAMMA MIA");
          const voices = synth.getVoices() || [];
          if (voices.length) {{
            u.voice = voices[Math.floor(Math.random()*voices.length)];
          }}
          u.pitch = 0.5 + Math.random()*1.5;
          u.rate = 0.8 + Math.random()*0.8;
          u.volume = 0.7;
          u.onend = function() {{
            if (!stopRequested && Date.now() < endTime) {{
              setTimeout(speakOnce, 120 + Math.random()*300);
            }}
          }};
          synth.speak(u);
        }}
        if (synth.getVoices().length === 0) {{
          synth.onvoiceschanged = function(){{ speakOnce(); }};
        }} else {{
          speakOnce();
        }}
      }}

      function startChorus() {{
        stopRequested = false;
        chickenArea.innerHTML = "";
        closeArea.innerHTML = "";
        appendLine("🎵 Simulating " + requestedCount.toLocaleString() + " chickens singing 'MAMMA MIA'... (theatrical) 🎵");
        let i=0;
        const pace = Math.max(1, Math.floor(maxDisplay / (durationSec*4)));
        const tickMs = Math.max(10, Math.floor((durationSec*1000) / Math.max(100, maxDisplay/pace)));

        const interval = setInterval(function(){{
          if (stopRequested) {{
            clearInterval(interval);
            appendLine("⛔ Chorus stopped by user.");
            try {{ if (window.speechSynthesis) window.speechSynthesis.cancel(); }} catch(e){{}}
            return;
          }}
          for (let k=0;k<pace && i<maxDisplay;k++) {{
            appendLine(randomJoke(i));
            i++;
          }}
          if (i >= maxDisplay) {{
            clearInterval(interval);
            appendLine("🎉 Chorus display complete. Preparing the final flourish...");
            setTimeout(function(){{
              if (stopRequested) {{ appendLine("⛔ Chorus stopped before close attempt."); return; }}
              appendLine("🔔 Final chorus complete.");
              closeArea.innerHTML = `<div style="margin-top:8px;"><button id="confirm-close" style="padding:10px 12px;background:#222;color:#fff;border-radius:6px;border:none;cursor:pointer">Attempt to close this tab (may be blocked)</button> <button id="no-close" style="padding:10px 12px;margin-left:8px;background:#eee;border:none;border-radius:6px;cursor:pointer">Keep tab open</button></div>`;
              document.getElementById("confirm-close").onclick = function() {{
                appendLine("Attempting to close tab... (your browser may block this).");
                setTimeout(function(){{
                  try {{
                    window.close();
                    appendLine("If the tab didn't close, your browser prevented it — that's normal for tabs not opened by script.");
                  }} catch(e) {{
                    appendLine("Close attempt thrown an error (expected in many browsers).");
                  }}
                }}, 400);
              }};
              document.getElementById("no-close").onclick = function() {{
                appendLine("Close canceled. Tab will remain open. Hope you enjoyed the chorus!");
                closeArea.innerHTML = "";
              }};
            }}, 700);
          }}
        }}, tickMs);

        try {{ speakChorus(durationSec); }} catch(e){{ console.warn("Speech failed:", e); }}
      }}

      startBtn.onclick = function() {{ startChorus(); }};
      stopBtn.onclick = function() {{
        stopRequested = true;
        try {{ if (window.speechSynthesis) window.speechSynthesis.cancel(); }} catch(e){{}}
      }};
    }})();
    </script>
    """

    components.html(html, height=560, scrolling=True)
    st.session_state.last_prank = f"Chicken Chorus (simulated) @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("This app is intended for playful, consensual pranks and meme creation only. Do not use to harass, threaten, doxx, or intimidate anyone. Always get consent.")

