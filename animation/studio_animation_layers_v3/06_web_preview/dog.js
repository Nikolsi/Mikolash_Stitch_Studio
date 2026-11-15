// Yorkshire terrier (puppy cut), sitting in the bed, facing the viewer. Pure SVG; groups are animated by CSS/JS.
// viewBox 120x190 is drawn at 0.46 scale in the scene (box in layer_map: dog.box_xyxy).
(() => {
  const strands = (cx, cy, n, len, spread, col, w, seed) => {
    let s = '', r = seed;
    const rnd = () => { r = (r * 9301 + 49297) % 233280; return r / 233280; };
    for (let i = 0; i < n; i++) {
      const a = (-90 + (rnd() - 0.5) * spread) * Math.PI / 180, l = len * (0.6 + rnd() * 0.6);
      const x0 = cx + (rnd() - 0.5) * 14, y0 = cy + (rnd() - 0.5) * 10;
      s += `M${x0.toFixed(1)} ${y0.toFixed(1)} q ${(Math.cos(a) * l * 0.5 + 2).toFixed(1)} ${(Math.sin(a) * l * 0.5).toFixed(1)} ${(Math.cos(a) * l).toFixed(1)} ${(Math.sin(a) * l).toFixed(1)} `;
    }
    return `<path d="${s}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`;
  };
  const legFur = (x, y0, y1, side, seed) => strands(x, (y0 + y1) / 2, 14, 12, 40, side ? '#f0cf98' : '#b8844a', 0.9, seed).replace(/q /g, 'q ');
  window.MSS_DOG_SVG = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 190" width="60" height="95" class="dog-svg">
 <defs>
  <filter id="fluff" x="-15%" y="-15%" width="130%" height="130%">
   <feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="2" seed="7" result="n"/>
   <feDisplacementMap in="SourceGraphic" in2="n" scale="5" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <radialGradient id="gold" cx="50%" cy="40%" r="65%"><stop offset="0" stop-color="#ecc78e"/><stop offset=".55" stop-color="#cf9d5f"/><stop offset="1" stop-color="#9b6834"/></radialGradient>
  <linearGradient id="goldLeg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9a868"/><stop offset="1" stop-color="#b07b42"/></linearGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a6c74"/><stop offset="1" stop-color="#3c3d44"/></linearGradient>
  <linearGradient id="knit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8474b"/><stop offset="1" stop-color="#922d33"/></linearGradient>
 </defs>
 <g class="dog-all" style="transform-origin:60px 185px">
  <!-- tail tuft behind the right haunch -->
  <g class="dog-tail" style="transform-origin:96px 160px"><path filter="url(#fluff)" d="M94 162 C 100 150, 108 146, 112 140 C 112 152, 106 162, 98 168 Z" fill="url(#steel)" stroke="#241a16" stroke-width="2.4"/></g>
  <!-- haunches -->
  <path filter="url(#fluff)" d="M22 186 C 18 166, 22 146, 36 138 L 46 186 Z" fill="url(#goldLeg)" stroke="#241a16" stroke-width="2.6"/>
  <path filter="url(#fluff)" d="M98 186 C 102 166, 98 146, 84 138 L 74 186 Z" fill="url(#goldLeg)" stroke="#241a16" stroke-width="2.6"/>
  <!-- torso (breathes) with steel saddle on the shoulders -->
  <g class="dog-chest" style="transform-origin:60px 180px">
   <path filter="url(#fluff)" d="M32 186 C 28 150, 30 112, 40 92 L 80 92 C 90 112, 92 150, 88 186 Z" fill="url(#gold)" stroke="#241a16" stroke-width="2.6"/>
   <path filter="url(#fluff)" d="M36 116 C 34 104, 38 92, 44 86 L 76 86 C 82 92, 86 104, 84 116 C 76 104, 68 100, 60 100 C 52 100, 44 104, 36 116 Z" fill="url(#steel)" stroke="none"/>
   <path filter="url(#fluff)" d="M48 104 C 54 100, 66 100, 72 104 C 70 124, 66 140, 60 146 C 54 140, 50 124, 48 104 Z" fill="#e8c38c" stroke="none" opacity=".85"/>
   ${strands(60, 128, 22, 10, 30, '#f2d39f', 1, 3)}${strands(60, 136, 16, 9, 30, '#9c6a37', 1, 11)}
   <!-- optional sweater -->
   <g class="dog-sweater">
    <path d="M33 150 C 31 128, 34 108, 41 94 L 79 94 C 86 108, 89 128, 87 150 C 78 156, 42 156, 33 150 Z" fill="url(#knit)" stroke="#241a16" stroke-width="2.4"/>
    <path d="M38 98 C 50 104, 70 104, 82 98 L 80 108 C 68 113, 52 113, 40 108 Z" fill="#efe1c4" stroke="#241a16" stroke-width="1.6"/>
    <path d="M36 134 l4 -4 l4 4 l4 -4 l4 4 l4 -4 l4 4 l4 -4 l4 4 l4 -4 l4 4 l4 -4 l4 4" fill="none" stroke="#efe1c4" stroke-width="2"/>
    <path d="M40 112 L40 150 M46 113 L46 152 M52 114 L52 153 M58 114 L58 154 M64 114 L64 154 M70 113 L70 153 M76 112 L76 152" stroke="#7d232a" stroke-opacity=".35" stroke-width="1.4"/>
   </g>
  </g>
  <!-- front legs, puppy-cut fluff -->
  <path filter="url(#fluff)" d="M40 186 C 38 164, 40 138, 46 122 L 58 124 C 58 146, 58 168, 57 186 Z" fill="url(#goldLeg)" stroke="#6b4524" stroke-width="1.4"/>
  <path filter="url(#fluff)" d="M80 186 C 82 164, 80 138, 74 122 L 62 124 C 62 146, 62 168, 63 186 Z" fill="url(#goldLeg)" stroke="#6b4524" stroke-width="1.4"/>
  ${legFur(49, 140, 180, 1, 5)}${legFur(71, 140, 180, 1, 9)}${legFur(49, 150, 184, 0, 13)}${legFur(71, 150, 184, 0, 17)}
  <!-- head -->
  <g class="dog-head" style="transform-origin:60px 92px">
   <g class="dog-ear-l" style="transform-origin:40px 36px">
    <path filter="url(#fluff)" d="M36 44 C 28 30, 22 14, 24 2 C 36 8, 46 18, 52 30 Z" fill="url(#gold)" stroke="#241a16" stroke-width="2.4"/>
    <path d="M36 36 C 32 26, 30 18, 30 11 C 37 16, 42 22, 45 29 Z" fill="#8c5a3c"/>
    ${strands(30, 24, 8, 9, 60, '#f0cf98', 1, 21)}
   </g>
   <g class="dog-ear-r" style="transform-origin:80px 36px">
    <path filter="url(#fluff)" d="M84 44 C 92 30, 98 14, 96 2 C 84 8, 74 18, 68 30 Z" fill="url(#gold)" stroke="#241a16" stroke-width="2.4"/>
    <path d="M84 36 C 88 26, 90 18, 90 11 C 83 16, 78 22, 75 29 Z" fill="#8c5a3c"/>
    ${strands(90, 24, 8, 9, 60, '#f0cf98', 1, 23)}
   </g>
   <!-- skull + cheek fur with fringe -->
   <path filter="url(#fluff)" d="M30 50 C 30 32, 44 22, 60 22 C 76 22, 90 32, 90 50 C 92 62, 90 74, 84 84 C 80 92, 72 96, 68 92 C 64 98, 56 98, 52 92 C 48 96, 40 92, 36 84 C 30 74, 28 62, 30 50 Z" fill="url(#gold)" stroke="#241a16" stroke-width="2.6"/>
   ${strands(42, 82, 14, 12, 70, '#9c6a37', 1.1, 31)}${strands(78, 82, 14, 12, 70, '#9c6a37', 1.1, 37)}${strands(60, 40, 18, 9, 80, '#f3d6a6', 1, 41)}
   <!-- light forehead / muzzle -->
   <path filter="url(#fluff)" d="M52 34 C 56 30, 64 30, 68 34 L 66 54 C 72 56, 76 62, 74 70 C 70 78, 50 78, 46 70 C 44 62, 48 56, 54 54 Z" fill="#efcf9c" opacity=".9"/>
   <!-- eyes -->
   <g class="dog-eyes">
    <g class="dog-pupils"><circle cx="45" cy="52" r="5" fill="#1c1210"/><circle cx="75" cy="52" r="5" fill="#1c1210"/><circle cx="46.6" cy="50.4" r="1.6" fill="#fff"/><circle cx="76.6" cy="50.4" r="1.6" fill="#fff"/></g>
    <g class="dog-lids"><path d="M39 47 h12 v10 h-12 Z" fill="#c7955a"/><path d="M69 47 h12 v10 h-12 Z" fill="#c7955a"/><path d="M39.5 54 q5.5 3 11 0 M69.5 54 q5.5 3 11 0" fill="none" stroke="#241a16" stroke-width="1.6"/></g>
   </g>
   <!-- nose, mouth, tongue -->
   <path d="M53 63 C 53 59, 67 59, 67 63 C 67 68, 62 71, 60 71 C 58 71, 53 68, 53 63 Z" fill="#141010" stroke="#241a16" stroke-width="1"/>
   <ellipse cx="57.5" cy="62" rx="2" ry="1.1" fill="#6d6363"/>
   <path d="M60 71 v4 M54 77 q6 4 12 0" fill="none" stroke="#3a2418" stroke-width="1.5" stroke-linecap="round"/>
   <path class="dog-tongue" d="M57 78 q3 8 6 0 Z" fill="#e2687a" stroke="#3a2418" stroke-width="1"/>
  </g>
 </g>
</svg>`;
})();
