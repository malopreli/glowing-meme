# main.py
# Loopy Random Prank Generator — single Start button, Stop button.
# - Cycles through random pranks in a loop until Stop is pressed.
# - Flashy visuals and browser speech (SpeechSynthesis volume=1.0).
# - DOES NOT control system volume or access private data.
# - All pranks are simulated and fictional.

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Goofy Random Pranks", page_icon="🤪", layout="wide")
st.title("Goofy Ahh Random Prank Loop 🤪")
st.write("Click **Start** to begin a chaotic loop of random pranks. Click **Stop** to end it immediately.")

# Embed the entire prank loop UI in one HTML/JS component.
# The JS uses SpeechSynthesis (volume=1.0), flashy CSS, and a random-prank loop.
html = """
<div style="font-family: Inter, Arial, sans-serif; padding:18px;">
  <div style="display:flex; gap:12px; align-items:center;">
    <button id="startBtn" style="padding:12px 18px; background:#00cc66; border:none; color:white; font-weight:700; border-radius:8px; cursor:pointer; box-shadow:0 6px 18px rgba(0,0,0,0.15);">START</button>
    <button id="stopBtn" style="padding:12px 18px; background:#ff4444; border:none; color:white; font-weight:700; border-radius:8px; cursor:pointer; box-shadow:0 6px 18px rgba(0,0,0,0.15);">STOP</button>
    <div id="status" style="margin-left:12px; font-weight:700; color:#222;">Idle</div>
  </div>

  <div id="stage" style="margin-top:16px; height:520px; border-radius:12px; overflow:hidden; position:relative; border:2px solid #111;">
    <!-- stage content injected by JS -->
    <div id="visual" style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:#111; color:#fff; font-size:28px;">
      Ready. Press START for maximum chaos.
    </div>
  </div>
</div>

<script>
(function(){
  const startBtn = document.getElementById('startBtn');
  const stopBtn = document.getElementById('stopBtn');
  const visual = document.getElementById('visual');
  const status = document.getElementById('status');

  // Prank assets (text-based, safe)
  const MEME_LINES = [
    "When your code runs on the first try",
    "No one: Absolutely no one: Me:",
    "This is fine.",
    "404: motivation not found",
    "POV: You clicked the link",
    "It was at this moment he knew... he messed up",
    "Modern problems require modern solutions",
    "We live in a society (but with better memes)",
    "Me: I'll go to bed early. Also me at 3 AM:",
    "Top text / Bottom text"
  ];

  const CHICKEN_JOKES = [
    "Why did the chicken cross the playground? To get to the other slide!",
    "Why did the chicken join a band? Because it had the drumsticks!",
    "What do chickens grow on? Eggplants!",
    "I'm not chicken, I'm poultry in motion!",
    "Do chickens like memes? Only if they're egg-ceptional.",
    "Chicken to the left of me, cluck to the right — here I am stuck in the meme tonight."
  ];

  let loopInterval = null;
  let activeTimeouts = [];
  let stopRequested = false;

  function clearActiveTimers(){
    activeTimeouts.forEach(t => clearTimeout(t));
    activeTimeouts = [];
  }

  function cancelSpeech(){
    try {
      if (window.speechSynthesis) window.speechSynthesis.cancel();
    } catch(e){}
  }

  function setFlashyBackground(colors, speedMs){
    // colors: array of color strings
    let i = 0;
    visual.style.transition = 'background 200ms linear';
    const flash = setInterval(() => {
      if (stopRequested) { clearInterval(flash); return; }
      visual.style.background = colors[i % colors.length];
      i++;
    }, Math.max(60, speedMs));
    activeTimeouts.push(flash);
    return flash;
  }

  function stopEverything(){
    stopRequested = true;
    status.textContent = "Stopping...";
    clearActiveTimers();
    cancelSpeech();
    // slight delay to let things settle
    setTimeout(() => {
      // reset visuals
      visual.innerHTML = '<div style="text-align:center;color:#fff;font-size:26px;">Stopped. Press START to go again.</div>';
      visual.style.background = '#111';
      status.textContent = "Stopped";
      stopRequested = false;
    }, 250);
  }

  // --- Prank impls ---

  function fakeUpdatePrank(duration = 3500){
    status.textContent = "Fake Update";
    visual.innerHTML = '';
    visual.style.display = 'flex';
    visual.style.flexDirection = 'column';
    visual.style.alignItems = 'center';
    visual.style.justifyContent = 'center';
    visual.style.background = '#061024';

    const box = document.createElement('div');
    box.style.background = 'rgba(255,255,255,0.03)';
    box.style.padding = '22px';
    box.style.borderRadius = '10px';
    box.style.width = '80%';
    box.style.textAlign = 'center';
    box.style.border = '2px solid rgba(255,255,255,0.06)';
    box.innerHTML = '<div style="font-size:22px;font-weight:800;margin-bottom:10px;color:#fff">SYSTEM UPDATE</div><div id="pbar" style="width:100%;height:18px;background:#222;border-radius:9px;overflow:hidden;"><div id="pfill" style="width:0%;height:100%;background:linear-gradient(90deg,#00e676,#00bcd4)"></div></div><div id="ptext" style="margin-top:10px;color:#ddd">Preparing...</div>';
    visual.appendChild(box);

    const pfill = document.getElementById('pfill');
    const ptext = document.getElementById('ptext');

    let start = Date.now();
    let steps = 60;
    for(let i=0;i<=steps;i++){
      const t = setTimeout(() => {
        if (stopRequested) return;
        const pct = Math.floor((i/steps) * 100);
        pfill.style.width = pct + '%';
        ptext.textContent = 'Installing... ' + pct + '%';
        if (i === steps) {
          ptext.textContent = 'Done. Nothing changed. 😉';
          // confetti-like effect (text)
          const conf = document.createElement('div');
          conf.innerHTML = '🎉🎈';
          conf.style.fontSize = '30px';
          conf.style.marginTop = '12px';
          box.appendChild(conf);
        }
      }, Math.floor(i * (duration/steps)));
      activeTimeouts.push(t);
    }
  }

  function memeFloodPrank(duration=3500){
    status.textContent = "Meme Flood";
    visual.style.background = '#0b0b0b';
    visual.innerHTML = '';
    const container = document.createElement('div');
    container.style.width = '100%';
    container.style.height = '100%';
    container.style.overflow = 'hidden';
    container.style.position = 'relative';
    visual.appendChild(container);

    const colors = ['#ff0077','#00ff88','#33ccff','#ffcc00','#ff4444','#7a5cff'];
    const flash = setFlashyBackground(colors, 100);

    let i=0;
    const pace = 90; // ms
    const maxItems = Math.min(80, Math.floor(duration / 40) * 2 + 8);
    function spawn(){
      if (stopRequested) return;
      const el = document.createElement('div');
      el.textContent = MEME_LINES[Math.floor(Math.random()*MEME_LINES.length)];
      el.style.position = 'absolute';
      el.style.left = Math.floor(Math.random()*80)+'%';
      el.style.top = Math.floor(Math.random()*80)+'%';
      el.style.fontSize = (18 + Math.floor(Math.random()*28)) + 'px';
      el.style.fontWeight = '900';
      el.style.color = ['white','black','yellow','cyan'][Math.floor(Math.random()*4)];
      el.style.transform = 'rotate('+ (Math.random()*40-20) +'deg)';
      el.style.textShadow = '0 2px 6px rgba(0,0,0,0.6)';
      el.style.opacity = '0.95';
      container.appendChild(el);
      i++;
      if (i < maxItems) {
        const t = setTimeout(spawn, pace + Math.random()*120);
        activeTimeouts.push(t);
      } else {
        // done
      }
    }
    spawn();

    // speech burst: a quick "MAMMA MIA!" to hype
    speakText("MAMMA MIA!", {rate: 1.0, pitch: 1.2, volume: 1.0});
  }

  function browserHistoryFakePrank(){
    status.textContent = "Browser History Panic (fake)";
    visual.style.background = '#2a0a0a';
    visual.innerHTML = '';
    const box = document.createElement('div');
    box.style.padding = '22px';
    box.style.borderRadius = '8px';
    box.style.background = 'linear-gradient(180deg,#420000,#220000)';
    box.style.width = '90%';
    box.style.textAlign = 'center';
    box.style.color = '#fff';
    box.innerHTML = '<div style="font-size:26px;font-weight:900">IMPORTANT</div><div style="margin-top:8px;font-weight:800">I released your browser history</div>';
    visual.appendChild(box);

    const t1 = setTimeout(() => {
      if (stopRequested) return;
      // reveal truth
      box.innerHTML += '<div style="margin-top:12px;color:#fff;font-weight:700">...just kidding. Relax — this is a joke.</div>';
      // fake entries
      const list = document.createElement('ul');
      list.style.marginTop = '12px';
      list.style.textAlign = 'left';
      const fake = [
        "2025-11-03 09:12 — pineapple-on-pizza-fanclub.example",
        "2025-11-02 22:01 — cats-in-socks-enthusiasts.example",
        "2025-10-31 18:44 — how-to-build-a-rockets-not-really.example",
        "2025-10-10 07:30 — definitely-not-your-searches.example"
      ];
      fake.forEach(it => {
        const li = document.createElement('li');
        li.textContent = it + "  (fake)";
        li.style.margin = '6px 0';
        li.style.fontWeight = '700';
        list.appendChild(li);
      });
      box.appendChild(list);
    }, 900);
    activeTimeouts.push(t1);

    // tiny dramatic beep
    speakText("Relax, it's a prank.", {rate:1.0, pitch:0.9, volume:1.0});
  }

  function chickenChorusPrank(duration=4000){
    status.textContent = "Chicken Chorus";
    visual.style.background = '#f9f5ee';
    visual.innerHTML = '';
    const area = document.createElement('div');
    area.style.padding = '18px';
    area.style.width = '100%';
    area.style.height = '100%';
    area.style.overflow = 'auto';
    area.style.fontSize = '18px';
    area.style.color = '#222';
    visual.appendChild(area);

    let i=0;
    const max = Math.min(50, Math.floor(duration/60)*5 + 10);
    function appendJ(){
      if (stopRequested) return;
      const div = document.createElement('div');
      div.textContent = (i+1) + '. ' + CHICKEN_JOKES[Math.floor(Math.random()*CHICKEN_JOKES.length)];
      div.style.padding = '6px 0';
      div.style.fontWeight = '800';
      area.appendChild(div);
      area.scrollTop = area.scrollHeight;
      i++;
      if (i < max){
        const t = setTimeout(appendJ, 90 + Math.random()*140);
        activeTimeouts.push(t);
      }
    }
    appendJ();
    // chant MAMMA MIA repeatedly
    startSpeechLoop("MAMMA MIA", duration);
  }

  function maxVolume67Prank(duration=3500){
    // simulated "full volume 67" scene (we DO NOT change system volume).
    status.textContent = "MAX VOLUME 67 (simulated)";
    visual.style.background = '#000';
    visual.style.color = '#fff';
    visual.innerHTML = '';

    // big blaring banner
    const banner = document.createElement('div');
    banner.style.width = '100%';
    banner.style.height = '100%';
    banner.style.display = 'flex';
    banner.style.flexDirection = 'column';
    banner.style.alignItems = 'center';
    banner.style.justifyContent = 'center';
    banner.style.fontSize = '48px';
    banner.style.fontWeight = '900';
    banner.style.letterSpacing = '2px';
    banner.style.textAlign = 'center';
    banner.innerHTML = '🔊🔊🔊 MAX VOLUME 67 ACTIVATED 🔊🔊🔊<div style="font-size:18px;margin-top:12px;font-weight:700;">(simulated)</div>';
    visual.appendChild(banner);

    // aggressive strobe
    const colors = ['#ff0000','#ffffff','#00ff00','#0000ff','#ff00ff','#ffff00'];
    const strobe = setInterval(() => {
      if (stopRequested) return;
      banner.style.background = colors[Math.floor(Math.random()*colors.length)];
      banner.style.color = (Math.random()>0.5) ? '#000' : '#fff';
    }, 120);
    activeTimeouts.push(strobe);

    // loud speech: "67" then "MAMMA MIA" loops, volume=1.0
    const seq = [
      {text: "SYNTHESIZING 67", opts:{rate:0.95,pitch:0.9,volume:1.0}},
      {text: "SIXTY SEVEN", opts:{rate:1.0,pitch:1.2,volume:1.0}},
      {text: "MAMMA MIA", opts:{rate:1.1,pitch:1.4,volume:1.0}}
    ];
    // speak them in quick succession
    (async function playSeq(){
      for(let i=0;i<Math.ceil(duration/700);i++){
        if (stopRequested) break;
        // pick one at random each cycle
        const s = seq[Math.floor(Math.random()*seq.length)];
        speakText(s.text, s.opts);
        await new Promise(r => setTimeout(r, 420 + Math.random()*300));
      }
      clearInterval(strobe);
    })();
  }

  // utility: speak once
  function speakText(text, opts){
    try {
      if (!('speechSynthesis' in window)) return;
      const utt = new SpeechSynthesisUtterance(text);
      utt.volume = (opts && opts.volume !== undefined) ? opts.volume : 1.0;
      utt.rate = (opts && opts.rate !== undefined) ? opts.rate : 1.0;
      utt.pitch = (opts && opts.pitch !== undefined) ? opts.pitch : 1.0;
      const voices = window.speechSynthesis.getVoices();
      if (voices && voices.length>0) utt.voice = voices[Math.floor(Math.random()*voices.length)];
      window.speechSynthesis.speak(utt);
    } catch(e){}
  }

  // looped speech for duration
  function startSpeechLoop(phrase, durationMs){
    try {
      if (!('speechSynthesis' in window)) return;
      const end = Date.now() + durationMs;
      function loopSpeak(){
        if (stopRequested) return;
        if (Date.now() > end) return;
        speakText(phrase, {rate:1.0,pitch:1.0,volume:1.0});
        const t = setTimeout(loopSpeak, 300 + Math.random()*450);
        activeTimeouts.push(t);
      }
      loopSpeak();
    } catch(e){}
  }

  // Choose a random prank and run it (each prank handles timing internally)
  const PRANKS = [
    () => fakeUpdatePrank(3000 + Math.random()*2000),
    () => memeFloodPrank(3000 + Math.random()*2200),
    () => browserHistoryFakePrank(),
    () => chickenChorusPrank(3000 + Math.random()*3000),
    () => maxVolume67Prank(2500 + Math.random()*3000)
  ];

  function runRandomPrankCycle(){
    if (stopRequested) return;
    // pick a prank
    const prank = PRANKS[Math.floor(Math.random()*PRANKS.length)];
    try {
      prank();
    } catch(e){
      console.error("prank error", e);
    }
  }

  // Main loop controller: run a prank every N seconds
  let mainLoopHandle = null;
  function startLoop(){
    if (mainLoopHandle) return;
    stopRequested = false;
    status.textContent = "Running";
    visual.style.transition = 'background 120ms linear';
    // initial immediate prank
    runRandomPrankCycle();
    // cycle every 3.2 - 5.5 seconds (random jitter)
    mainLoopHandle = setInterval(() => {
      if (stopRequested) {
        clearInterval(mainLoopHandle);
        mainLoopHandle = null;
        return;
      }
      clearActiveTimers();
      cancelSpeech();
      // small gap reset
      visual.innerHTML = '<div style="color:#fff;font-size:20px;">— next prank incoming —</div>';
      const jitter = 800 + Math.random()*800;
      const t = setTimeout(() => {
        runRandomPrankCycle();
      }, jitter);
      activeTimeouts.push(t);
    }, 4200 + Math.random()*2000);
  }

  function stopLoop(){
    clearInterval(mainLoopHandle);
    mainLoopHandle = null;
    stopEverything();
  }

  startBtn.onclick = function(){
    // reset any previous
    stopRequested = false;
    clearActiveTimers();
    cancelSpeech();
    // start loop
    if (mainLoopHandle) {
      // already running — restart quickly
      clearInterval(mainLoopHandle);
      mainLoopHandle = null;
    }
    status.textContent = "Starting";
    setTimeout(() => {
      status.textContent = "Running";
    }, 300);
    startLoop();
  };

  stopBtn.onclick = function(){
    stopLoop();
  };

  // ensure speech voices are warmed up in some browsers
  if ('speechSynthesis' in window) {
    window.speechSynthesis.getVoices();
  }
})();
</script>
"""

components.html(html, height=720, scrolling=True)

st.caption("Note: The 'MAX VOLUME 67' prank uses the browser's speech API at volume=1.0 (browser-only). This app does NOT and CANNOT change your system volume or access private data.")


