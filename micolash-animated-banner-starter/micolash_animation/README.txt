MICOLASH STITCH STUDIO — ANIMATED BANNER STARTER

WHAT'S INCLUDED
- index.html: standalone demo page with example overlay text/navigation.
- styles.css: responsive scene layout and independent character layer.
- script.js: looping left-right movement and running-frame playback.
- assets/studio-background.png: generated studio room background.
- assets/run-1.png ... run-8.png: character running frames with transparent backgrounds.

HOW TO PREVIEW
1. Unzip the folder.
2. Open index.html in a modern browser. (If your browser blocks local images, run a local server, e.g. `python -m http.server 8000`, then visit http://localhost:8000.)

HOW TO ADD TO YOUR EXISTING SITE
- Copy the assets folder into your site project.
- Copy the .character element from index.html into the banner container.
- Copy the .room and .character CSS rules from styles.css.
- Add script.js, or merge its code into your existing JS bundle.
- Keep your existing menu/buttons above the character with a higher z-index.

IMPORTANT PROTOTYPE NOTES
- This first version animates the running cycle and moves the character between the two sides.
- It uses a running pose as the idle placeholder. For a polished final version, we still need dedicated transparent poses/frames for sitting at the computer, standing up, sitting at the embroidery machine, and turning/transitioning.
- The character sprite sheet was chroma-keyed from a generated green-screen sheet; inspect edges on your actual background. If you notice a green fringe, we can refine the matte.
- The background and positions are a starting point. The left/right percentages and character size should be tuned to your final banner dimensions.
