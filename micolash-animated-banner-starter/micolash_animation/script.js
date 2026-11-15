// Micolash Stitch Studio — simple looping character animation.
// Tune these values after checking the banner on your actual website.
const runner = document.getElementById('runner');
const character = document.querySelector('.character');
const frames = Array.from({ length: 8 }, (_, i) => `assets/run-${i + 1}.png`);

const settings = {
  leftPosition: 25,       // % from the left edge: computer side
  rightPosition: 67,      // % from the left edge: embroidery-machine side
  idleAtEachSide: 3500,   // pause at each workstation (ms)
  runDuration: 2100,      // time to cross the room (ms)
  frameDuration: 105      // speed of the running cycle (ms)
};

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let frameTimer = null;
let currentFrame = 0;
let facingRight = true;

function showFrame(index) {
  currentFrame = index % frames.length;
  runner.src = frames[currentFrame];
}

function runAnimation() {
  if (reduceMotion) {
    showFrame(0);
    return;
  }
  frameTimer = window.setInterval(() => showFrame(currentFrame + 1), settings.frameDuration);
}
function stopAnimation() {
  if (frameTimer !== null) window.clearInterval(frameTimer);
  frameTimer = null;
  showFrame(0);
}
function pause(ms) { return new Promise(resolve => window.setTimeout(resolve, ms)); }
function moveTo(position, direction) {
  facingRight = direction === 'right';
  character.style.transform = facingRight ? 'scaleX(1)' : 'scaleX(-1)';
  character.style.transition = `left ${settings.runDuration}ms linear`;
  runAnimation();
  // Force layout so the browser starts the transition from the current position.
  void character.offsetWidth;
  character.style.left = `${position}%`;
  return pause(settings.runDuration);
}

async function loop() {
  if (reduceMotion) return;
  character.style.left = `${settings.leftPosition}%`;
  character.style.transform = 'scaleX(1)';
  while (true) {
    stopAnimation();
    await pause(settings.idleAtEachSide);
    await moveTo(settings.rightPosition, 'right');
    stopAnimation();
    await pause(settings.idleAtEachSide);
    await moveTo(settings.leftPosition, 'left');
  }
}

// Preload all frames so the first run does not stutter.
frames.forEach(src => { const image = new Image(); image.src = src; });
loop();
