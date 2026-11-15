(() => {
  'use strict';
  const D = window.MSS;
  const $ = (id) => document.getElementById(id);
  const stage = $('stage'), charEl = $('char'), framesEl = $('frames'), sitrig = $('sitrig');
  let fFront = $('frameA'), fBack = $('frameB'), speed = 1;
  const torso = $('leanTorso'), boot = $('leanBoot'), needle = $('needle'), machineHead = $('machineHead');
  const FR = (n) => `../02_character_frames/${n}.png`;
  const [AX, AY] = D.character.anchor_px;
  const WC = D.character.walk_cycle, CYCLE = WC.order, ADV = WC.advance_px_per_frame, WALK_DT = 1 / WC.fps;
  const SR = D.character.sit_rear, LR = D.character.lean_rig;
  const params = new URLSearchParams(location.search);
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const rand = (a, b) => a + Math.random() * (b - a);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const ease = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

  // ---------- preload frames
  const used = new Set(CYCLE);
  D.route.forEach((s) => s.frame && used.add(s.frame));
  used.forEach((f) => { const i = new Image(); i.src = FR(f); });

  // ---------- static placement from the layer map
  const box = (el, b) => Object.assign(el.style, { left: b[0] + 'px', top: b[1] + 'px', width: b[2] - b[0] + 'px', height: b[3] - b[1] + 'px' });
  const A = D.ambient_overlays;
  box($('pcGlow'), A.pc_rgb_glow.box_xyxy);
  box($('colon'), A.clock_colon_off.box_xyxy);
  box($('monL'), A.monitor_glow.boxes_xyxy[0]);
  box($('monR'), A.monitor_glow.boxes_xyxy[1]);
  charEl.style.setProperty('--pivot-x', SR.head_pivot_canvas[0] + 'px'); charEl.style.setProperty('--pivot-y', SR.head_pivot_canvas[1] + 'px');
  charEl.style.setProperty('--hip-x', LR.hip_pivot_canvas[0] + 'px'); charEl.style.setProperty('--hip-y', LR.hip_pivot_canvas[1] + 'px');
  charEl.style.setProperty('--heel-x', LR.heel_pivot_canvas[0] + 'px'); charEl.style.setProperty('--heel-y', LR.heel_pivot_canvas[1] + 'px');

  // ---------- content slots: any image/video is projected onto the slot quad (matrix3d)
  function quadMatrix(w, h, q) {
    const [[x0, y0], [x1, y1], [x2, y2], [x3, y3]] = q;
    const dx1 = x1 - x2, dx2 = x3 - x2, dx3 = x0 - x1 + x2 - x3, dy1 = y1 - y2, dy2 = y3 - y2, dy3 = y0 - y1 + y2 - y3;
    const den = dx1 * dy2 - dx2 * dy1, g = (dx3 * dy2 - dx2 * dy3) / den, k = (dx1 * dy3 - dx3 * dy1) / den;
    const a = x1 - x0 + g * x1, b = x3 - x0 + k * x3, d = y1 - y0 + g * y1, e = y3 - y0 + k * y3;
    return `matrix3d(${a / w},${d / w},0,${g / w},${b / h},${e / h},0,${k / h},0,0,1,0,${x0},${y0},0,1)`;
  }
  Object.entries(D.content_slots).forEach(([id, s]) => {
    const el = document.createElement('div'); el.className = 'slot'; el.dataset.slot = id;
    const [w, h] = s.size; el.style.width = w + 'px'; el.style.height = h + 'px'; el.style.transform = quadMatrix(w, h, s.quad);
    const isVideo = /\.(mp4|webm)$/i.test(s.file), m = document.createElement(isVideo ? 'video' : 'img');
    if (isVideo) Object.assign(m, { muted: true, loop: true, autoplay: true, playsInline: true });
    m.src = '../' + s.file; if (s.filter) m.style.filter = s.filter; if (s.fit) m.style.objectFit = s.fit;
    el.appendChild(m); $('slots').appendChild(el);
  });

  // ---------- fit the 1672x941 stage into the window
  let fitMode = 'contain';
  function fit() {
    const vw = innerWidth, vh = innerHeight;
    const s = fitMode === 'contain' ? Math.min(vw / 1672, vh / 941) : Math.max(vw / 1672, vh / 941);
    stage.style.transform = `translate(${(vw - 1672 * s) / 2}px, ${(vh - 941 * s) / 2}px) scale(${s})`;
  }
  addEventListener('resize', fit); fit();

  // ---------- character helpers
  const place = (x, y, flip) => { charEl.style.transform = `translate(${Math.round(x - AX)}px, ${Math.round(y - AY)}px)` + (flip ? ' scaleX(-1)' : ''); };
  const mode = (m) => {
    charEl.classList.remove('mode-frame', 'mode-sit', 'mode-lean'); charEl.classList.add('mode-' + m);
    framesEl.classList.toggle('on', m === 'frame');
    if (m !== 'frame') { fFront.dataset.f = ''; fFront.style.opacity = 0; fBack.style.opacity = 0; }
  };
  // frame-based poses: two buffers, the next frame (at its own locked position) fades in over the previous one
  function showFrameAt(name, x, y, flip, fade) {
    mode('frame');
    const tr = `translate(${Math.round(x - AX)}px, ${Math.round(y - AY)}px)` + (flip ? ' scaleX(-1)' : '');
    if (fFront.dataset.f === name && fFront.style.transform === tr) return;
    if (!fade || !fFront.dataset.f) {
      Object.assign(fFront.style, { transition: 'none', transform: tr, opacity: 1, zIndex: 2 }); fFront.src = FR(name); fFront.dataset.f = name;
      fBack.style.transition = 'none'; fBack.style.opacity = 0; return;
    }
    const d = fade / speed;
    Object.assign(fBack.style, { transition: 'none', transform: tr, opacity: 0, zIndex: 2 }); fBack.src = FR(name); fBack.dataset.f = name;
    fFront.style.zIndex = 1; void fBack.offsetWidth;
    fBack.style.transition = `opacity ${d}s linear`; fFront.style.transition = `opacity ${d * 0.5}s linear ${d * 0.5}s`;
    fBack.style.opacity = 1; fFront.style.opacity = 0;
    [fFront, fBack] = [fBack, fFront];
  }
  const FADE_WALK = WALK_DT * (D.character.walk_cycle.crossfade || 0.6), FADE_HOLD = 0.12;
  const statusEl = $('status'), status = (t) => { statusEl.textContent = t; };

  // ---------- character timeline
  const sitOverride = params.has('sit') ? Number(params.get('sit')) : null;
  let idx = -1, step = null, t = 0, walk = null;
  function startStep(i) {
    idx = i % D.route.length; step = D.route[idx]; t = 0;
    if (step.label) status(step.label);
    // someone is behind the chair -> the mesh shows the hoodie instead of the desk
    const behind = ['sit', 'rise', 'sitdown'].includes(step.type) || (step.type === 'hold' && step.at[0] >= 440 && step.at[0] <= 545 && step.at[1] <= 730);
    $('meshOccupied').classList.toggle('on', behind);
    document.body.classList.toggle('typing', step.type === 'sit');
    charEl.classList.remove('look-right', 'no-bob', 'arms-off');
    if (step.type === 'sit') {
      step._dur = sitOverride || (Array.isArray(step.dur) ? rand(step.dur[0], step.dur[1]) : step.dur);
      step._turnAt = rand(2.5, 5); step._turnLen = rand(1.8, 3);
      mode('sit'); sitrig.style.transform = ''; place(step.at[0], step.at[1], false);
    } else if (step.type === 'rise' || step.type === 'sitdown') {
      mode('sit'); charEl.classList.add('no-bob', 'arms-off'); place(step.at[0], step.at[1], false);
    } else if (step.type === 'hold') {
      showFrameAt(step.frame, step.at[0], step.at[1], step.flip, FADE_HOLD);
    } else if (step.type === 'walk') {
      walk = { x: step.from[0], i: 0, acc: 0 }; showFrameAt(CYCLE[0], walk.x, walkY(walk.x), step.dir < 0, FADE_HOLD);
    } else if (step.type === 'lean') {
      mode('lean'); place(step.at[0], step.at[1], false); leanPose(step.angle_from, 0);
    }
  }
  const stepDur = () => (step.type === 'sit' ? step._dur : step.type === 'lean' ? step.in_s + step.hold_s + step.out_s : step.dur);
  function walkY(x) {
    const chair = step.dir > 0 ? step.from : step.to, lane = step.dir > 0 ? step.to : step.from;
    const k = clamp((x - chair[0]) / (step.y_ease_until_x - chair[0]), 0, 1);
    return chair[1] + (lane[1] - chair[1]) * k * k * (3 - 2 * k);
  }
  function leanPose(angle, tap) { torso.style.transform = `rotate(${-angle}deg)`; boot.style.transform = `rotate(${-tap}deg)`; }

  function tick(dt) {
    t += dt;
    if (step.type === 'walk') {
      walk.acc += dt;
      while (walk.acc >= WALK_DT) {
        walk.acc -= WALK_DT; walk.x += step.dir * ADV[walk.i]; walk.i = (walk.i + 1) % CYCLE.length;
        if ((step.dir > 0 && walk.x >= step.to[0]) || (step.dir < 0 && walk.x <= step.to[0])) { startStep(idx + 1); return; }
      }
      showFrameAt(CYCLE[walk.i], walk.x, walkY(walk.x), step.dir < 0, FADE_WALK); return;
    }
    if (step.type === 'sit') {
      if (t > step._turnAt + step._turnLen) { step._turnAt = t + rand(4, 7); step._turnLen = rand(1.8, 3); }
      charEl.classList.toggle('look-right', t >= step._turnAt && t <= step._turnAt + step._turnLen);
    } else if (step.type === 'rise' || step.type === 'sitdown') {
      const k = ease(clamp(t / step.dur, 0, 1)), up = step.type === 'rise' ? k : 1 - k;
      sitrig.style.transform = `translateY(${(-SR.DROP_px * up).toFixed(2)}px)`;
      if (step.type === 'sitdown') charEl.classList.toggle('arms-off', k < 0.8);
    } else if (step.type === 'lean') {
      let angle = 0, tap = 0;
      if (t < step.in_s) angle = step.angle_from * (1 - ease(t / step.in_s));
      else if (t < step.in_s + step.hold_s) {
        const th = t - step.in_s;
        for (const [a, b] of step.taps) if (th >= a && th < b) { const f = ((th - a) % step.tap_period) / step.tap_period; tap = step.tap_deg * Math.pow(Math.sin(Math.PI * f), 2); }
      } else angle = step.angle_from * ease(clamp((t - step.in_s - step.hold_s) / step.out_s, 0, 1));
      leanPose(angle, tap);
    }
    if (t >= stepDur()) startStep(idx + 1);
  }

  // ---------- embroidery machine: one needle strokes, the head barely vibrates
  const M = D.machine; let mt = 0;
  function machineTick(dt) {
    mt += dt;
    const ph = mt % (M.run_s + M.pause_s);
    if (ph < M.run_s) {
      const s = 0.5 - 0.5 * Math.cos(2 * Math.PI * M.needle.hz * ph);
      needle.style.transform = `translateY(${(s * M.needle.stroke_px).toFixed(2)}px)`;
      machineHead.style.transform = `translateY(${(s * M.head.jitter_px).toFixed(2)}px)`;
    } else { needle.style.transform = ''; machineHead.style.transform = ''; }
  }

  // ---------- controls
  let playing = true, last = performance.now();
  $('btnPlay').onclick = (e) => { playing = !playing; e.target.textContent = playing ? '❚❚ Пауза' : '▶ Играть'; };
  $('btnMachine').onclick = () => { if (step && step.type === 'sit') t = step._dur; };
  $('btnSpeed').onclick = (e) => { speed = speed === 1 ? 2 : speed === 2 ? 4 : 1; e.target.textContent = `Скорость ×${speed}`; };
  $('btnFit').onclick = (e) => { fitMode = fitMode === 'contain' ? 'cover' : 'contain'; e.target.textContent = fitMode === 'contain' ? 'Режим: вписать' : 'Режим: заполнить'; fit(); };
  $('btnDebug').onclick = () => document.body.classList.toggle('debug');
  if (params.has('debug')) document.body.classList.add('debug');
  if (params.has('nohud')) $('hud').style.display = 'none';

  startStep(0);
  if (reduceMotion) { status('prefers-reduced-motion: сцена статична'); return; }
  const all = (d) => { tick(d); machineTick(d); };
  if (params.has('t')) { let left = Number(params.get('t')); while (left > 0) { const d = Math.min(0.05, left); all(d); left -= d; } }
  function loop(now) {
    const dt = Math.min(0.1, (now - last) / 1000) * speed; last = now;
    if (playing && !document.hidden) all(dt);
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();
