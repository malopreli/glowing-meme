function browserHistoryFakePrank(){
    status.textContent = "Browser History Panic";
    visual.innerHTML = '';
    visual.style.background = '#220022';
    
    const box = document.createElement('div');
    box.style.padding = '20px';
    box.style.borderRadius = '10px';
    box.style.background = 'linear-gradient(180deg,#420000,#220000)';
    box.style.width = '90%';
    box.style.margin = '0 auto';
    box.style.textAlign = 'center';
    box.style.color = '#ff0077';
    box.style.fontSize = '28px';
    box.style.fontWeight = '900';
    box.innerHTML = "I released your browser history 💀";
    visual.appendChild(box);

    // Slowly reveal fake entries over ~20 seconds
    const fakeEntries = [
        "2025-11-03 09:12 — pineapple-on-pizza-fanclub.example",
        "2025-11-02 22:01 — cats-in-socks-enthusiasts.example",
        "2025-10-31 18:44 — how-to-build-a-rockets-not-really.example",
        "2025-10-10 07:30 — definitely-not-your-searches.example",
        "2025-09-25 12:15 — dancing-llamas-2025.example",
        "2025-08-18 20:40 — ultra-goofy-meme-factory.example"
    ];

    fakeEntries.forEach((entry, idx) => {
        const t = setTimeout(() => {
            if(stopRequested) return;
            const p = document.createElement('div');
            p.textContent = entry + "  (fake)";
            p.style.margin = '6px 0';
            p.style.fontWeight = '700';
            box.appendChild(p);
        }, idx * 3200); // 6 entries * ~3.2s each ≈ 20s total
        activeTimeouts.push(t);
    });

    // End message after 20 seconds
    const tEnd = setTimeout(() => {
        if(stopRequested) return;
        const endMsg = document.createElement('div');
        endMsg.textContent = "...just kidding. Relax — this is a joke 😎";
        endMsg.style.marginTop = '12px';
        endMsg.style.fontWeight = '700';
        box.appendChild(endMsg);
    }, 20000);
    activeTimeouts.push(tEnd);

    // optional fun speech
    speakText("Relax, it's a prank", {volume:1.0});
}
