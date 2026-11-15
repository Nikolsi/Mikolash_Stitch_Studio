// generated from 04_guides/layer_map.json — edit content_slots there or here (keep both in sync)
window.MSS = {
 "scene": [
  1672,
  941
 ],
 "layers_back_to_front": [
  {
   "z": 0,
   "file": "01_scene_layers/00_background_clean_plate.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    0,
    0,
    1672,
    941
   ],
   "motion": "static",
   "role": "Мастерская без кресла, тени кресла, головки/игл, неона и мячика. Закрытые участки восстановлены."
  },
  {
   "z": 1,
   "file": "01_scene_layers/00b_neon_sign.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    394,
    132,
    655,
    301
   ],
   "motion": "flicker",
   "role": "Неоновая вывеска (сменяемый «баннер»): трубки + свечение на стене, полупрозрачная. Можно заменить любым RGBA того же холста."
  },
  {
   "z": 2,
   "name": "content_slots",
   "type": "slot",
   "role": "Постеры и экраны мониторов: картинки из /content проецируются на четырёхугольники (см. content_slots)."
  },
  {
   "z": 3,
   "file": "01_scene_layers/01_chair_shadow.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    387,
    723,
    602,
    770
   ],
   "motion": "static",
   "role": "Тень/отражения кресла на полу."
  },
  {
   "z": 4,
   "file": "01_scene_layers/02_machine_needles_static.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    1346,
    504,
    1412,
    520
   ],
   "motion": "static",
   "role": "Неподвижные иглы и лапки (11 из 12)."
  },
  {
   "z": 5,
   "file": "01_scene_layers/02b_machine_needle_active.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    1378,
    509,
    1383,
    520
   ],
   "motion": "needle",
   "role": "Одна активная игла: ход 0→4 px вниз, синусоида ~9 Гц во время шитья."
  },
  {
   "z": 6,
   "file": "01_scene_layers/03_machine_head.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    1334,
    413,
    1418,
    514
   ],
   "motion": "head",
   "role": "Головка: подрагивание ≤0.5 px синхронно с иглой."
  },
  {
   "z": 7,
   "name": "character",
   "type": "character",
   "role": "Персонаж (02_character_frames)."
  },
  {
   "z": 8,
   "file": "01_scene_layers/05_chair_seat_base.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    409,
    620,
    571,
    765
   ],
   "motion": "static",
   "role": "Сиденье, механизм, крестовина. Кресло спинкой к зрителю — поверх персонажа."
  },
  {
   "z": 9,
   "file": "01_scene_layers/06_chair_back.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    396,
    479,
    592,
    670
   ],
   "motion": "static",
   "role": "Спинка и подлокотники — поверх персонажа."
  },
  {
   "z": 10,
   "file": "01_scene_layers/06b_chair_back_mesh_occupied.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    414,
    495,
    538,
    603
   ],
   "motion": "occupied",
   "role": "Сетка спинки «занята»: сквозь плетение видна толстовка, а не стол. Показывается, пока персонаж сидит/стоит за креслом."
  },
  {
   "z": 11,
   "file": "01_scene_layers/07_foreground_rug.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    435,
    775,
    1394,
    875
   ],
   "motion": "static",
   "role": "Ковёр (перекрытие, на маршруте не задействован)."
  },
  {
   "z": 12,
   "name": "dog",
   "type": "dog",
   "role": "Собака: пиксельные спрайт-кадры 68×104 (09_dog/frames, sw_* — в кофточке), исходник SVG 09_dog/yorkie.svg."
  },
  {
   "z": 13,
   "name": "ball",
   "type": "ball",
   "role": "Теннисный мячик: 8 кадров вращения 32×32 (01_scene_layers/ball/), катится от носа собаки."
  },
  {
   "z": 14,
   "file": "01_scene_layers/08_dog_bed_front_rim.png",
   "canvas": [
    1672,
    941
   ],
   "position": [
    0,
    0
   ],
   "bbox_xyxy": [
    189,
    830,
    437,
    906
   ],
   "motion": "static",
   "role": "Передний бортик лежанки — поверх собаки и мячика."
  }
 ],
 "content_slots": {
  "monitor_left": {
   "quad": [
    [
     329,
     379
    ],
    [
     479,
     379
    ],
    [
     479,
     488
    ],
    [
     329,
     488
    ]
   ],
   "size": [
    150,
    109
   ],
   "aspect": 1.3761,
   "file": "content/monitor_left.png",
   "kind": "screen",
   "fit": "cover",
   "filter": ""
  },
  "monitor_right": {
   "quad": [
    [
     490,
     382
    ],
    [
     697,
     382
    ],
    [
     697,
     488
    ],
    [
     490,
     488
    ]
   ],
   "size": [
    207,
    106
   ],
   "aspect": 1.9528,
   "file": "content/monitor_right.png",
   "kind": "screen",
   "fit": "cover",
   "filter": ""
  },
  "poster_fuji": {
   "quad": [
    [
     738,
     229
    ],
    [
     844,
     229
    ],
    [
     844,
     335
    ],
    [
     738,
     335
    ]
   ],
   "size": [
    106,
    106
   ],
   "aspect": 1.0,
   "file": "content/poster_fuji.png",
   "kind": "poster",
   "fit": "cover",
   "filter": ""
  },
  "poster_torii": {
   "quad": [
    [
     882,
     229
    ],
    [
     982,
     229
    ],
    [
     982,
     335
    ],
    [
     882,
     335
    ]
   ],
   "size": [
    100,
    106
   ],
   "aspect": 0.9434,
   "file": "content/poster_torii.png",
   "kind": "poster",
   "fit": "cover",
   "filter": ""
  },
  "poster_wave": {
   "quad": [
    [
     1018,
     228
    ],
    [
     1120,
     228
    ],
    [
     1120,
     342
    ],
    [
     1018,
     342
    ]
   ],
   "size": [
    102,
    114
   ],
   "aspect": 0.8947,
   "file": "content/poster_wave.png",
   "kind": "poster",
   "fit": "cover",
   "filter": ""
  },
  "poster_tiger": {
   "quad": [
    [
     1390,
     154
    ],
    [
     1495,
     154
    ],
    [
     1495,
     298
    ],
    [
     1390,
     298
    ]
   ],
   "size": [
    105,
    144
   ],
   "aspect": 0.7292,
   "file": "content/poster_tiger.png",
   "kind": "poster",
   "fit": "cover",
   "filter": ""
  },
  "poster_cloud": {
   "quad": [
    [
     1526,
     218
    ],
    [
     1601,
     210
    ],
    [
     1602,
     321
    ],
    [
     1527,
     327
    ]
   ],
   "size": [
    75,
    111
   ],
   "aspect": 0.6757,
   "file": "content/poster_cloud.png",
   "kind": "poster",
   "fit": "cover",
   "filter": ""
  }
 },
 "ambient_overlays": {
  "pc_rgb_glow": {
   "file": "03_ambient_overlays/pc_rgb_glow.png",
   "box_xyxy": [
    250,
    578,
    366,
    712
   ],
   "blend": "screen",
   "motion": "pulse 4 s"
  },
  "clock_colon_off": {
   "file": "03_ambient_overlays/clock_colon_off.png",
   "box_xyxy": [
    1576,
    142,
    1592,
    172
   ],
   "blend": "normal",
   "motion": "show 0.5 s every 1 s (colon blink)"
  },
  "monitor_glow": {
   "type": "css",
   "boxes_xyxy": [
    [
     322,
     372,
     486,
     491
    ],
    [
     487,
     376,
     701,
     493
    ]
   ],
   "blend": "screen",
   "motion": "soft flicker while typing"
  }
 },
 "character": {
  "canvas": [
   320,
   440
  ],
  "anchor_px": [
   160,
   430
  ],
  "walk_cycle": {
   "order": [
    "walk_side/walk_01",
    "walk_side/walk_06",
    "walk_side/walk_05",
    "walk_side/walk_04"
   ],
   "advance_px_per_frame": [
    26,
    42,
    40,
    34
   ],
   "fps": 10,
   "note": "Order chosen by planted-foot analysis; advances keep the planted boot within ~±6 px. 10 fps (was 8) — smoother and ~25% faster.",
   "crossfade": 0.35
  },
  "sit_rear": {
   "DROP_px": 58,
   "head_pivot_canvas": [
    163,
    171
   ],
   "parts": [
    "sit_rear/sit_rear_head",
    "sit_rear/sit_rear_head_turn_right",
    "sit_rear/sit_rear_body"
   ],
   "layer_order": "head under body (hood covers the neck seam)",
   "idle_motion": "head rotate ±1.2° around pivot, ~0.9 s; occasional head_turn_right 2–4 s; body breathing scaleY 1.000–1.006 from bottom",
   "rise_sequence": [
    "sit_rear/sit_rear_01",
    "sit_rear/rise_rear_01",
    "sit_rear/rise_rear_02",
    "walk_away/walk_away_01"
   ],
   "rise": "continuous: translate sit rig (head+body) by -DROP over 0.5 s (ease-in-out), legs stay; then switch to walk_away/walk_away_01",
   "occupied_mesh": "01_scene_layers/06b_chair_back_mesh_occupied.png — show while someone is behind the chair"
  },
  "lean_rig": {
   "hip_pivot_canvas": [
    140,
    244
   ],
   "heel_pivot_canvas": [
    154,
    428
   ],
   "torso_angles_deg_ccw": {
    "lean_rig_00_upright": 18,
    "lean_rig_01_half": 9,
    "lean_rig_02_inspect": 0
   },
   "tap_deg_ccw": 7,
   "note": "legs fixed; torso rotates around the hip; front boot rotates around the heel (toe up) for foot tapping",
   "parts": [
    "lean_rig/lean_rig_legs",
    "lean_rig/lean_rig_front_boot",
    "lean_rig/lean_rig_torso"
   ],
   "layer_order": "legs, front boot, torso",
   "frames": [
    "lean_rig/lean_rig_00_upright",
    "lean_rig/lean_rig_01_half",
    "lean_rig/lean_rig_02_inspect",
    "lean_rig/lean_rig_02_inspect_tap"
   ],
   "waiting": "alternate lean_rig_02_inspect (0.30 s) / lean_rig_02_inspect_tap (0.16 s) = foot tapping while the machine stitches"
  },
  "z_rule": "character is above machine layers and below both chair layers"
 },
 "dog": {
  "box_xyxy": [
   262,
   761,
   330,
   865
  ],
  "frames_dir": "09_dog/frames",
  "source_svg": "09_dog/yorkie.svg (+ 06_web_preview/dog.js)",
  "sweater": false,
  "poses": {
   "sleep": {
    "frames": [
     "sleep_a",
     "sleep_b"
    ],
    "period": 1.7
   },
   "awake": {
    "frames": [
     "awake_a",
     "awake_b"
    ],
    "period": 0.8
   },
   "twitch": {
    "frames": [
     "twitch"
    ]
   },
   "tilt-l": {
    "frames": [
     "tilt_l"
    ]
   },
   "tilt-r": {
    "frames": [
     "tilt_r"
    ]
   },
   "ball": {
    "frames": [
     "ball_a",
     "ball_b"
    ],
    "period": 0.17
   },
   "nudge": {
    "frames": [
     "nudge"
    ]
   },
   "happy": {
    "frames": [
     "happy_a",
     "happy_b"
    ],
    "period": 0.17
   },
   "guy": {
    "frames": [
     "guy_a",
     "guy_b"
    ],
    "period": 0.17
   }
  },
  "ball": {
   "center": [
    338,
    846
   ],
   "radius": 15,
   "roll_px": 18,
   "frames": "01_scene_layers/ball/ball_0..7.png (45° steps)"
  },
  "sleep_s": [
   7,
   12
  ],
  "behaviour": "sits in the bed: dozes (eyes closed, head droops) → wakes, twitches ears, tilts head left/right → looks at the ball → nudges it (rolls ~18 px), happy hop + tongue + tail wag → pulls it back → dozes. Blinks; looks at the guy when he stands up. Optional sweater (dog.sweater)."
 },
 "route_points": {
  "sit": [
   476,
   722
  ],
  "turn": [
   525,
   724
  ],
  "profile": [
   560,
   726
  ],
  "walk_start": [
   590,
   728
  ],
  "lane_y": 755,
  "machine_stop": [
   1170,
   755
  ],
  "lean_base": [
   1192,
   755
  ]
 },
 "route": [
  {
   "type": "sit",
   "at": [
    476,
    722
   ],
   "dur": [
    10,
    15
   ],
   "label": "работает за компьютером"
  },
  {
   "type": "rise",
   "at": [
    476,
    722
   ],
   "dur": 0.5,
   "label": "встаёт"
  },
  {
   "type": "hold",
   "frame": "walk_away/walk_away_01",
   "at": [
    476,
    722
   ],
   "dur": 0.3,
   "flip": false,
   "label": null
  },
  {
   "type": "hold",
   "frame": "walk_away/walk_away_02",
   "at": [
    525,
    724
   ],
   "dur": 0.22,
   "flip": false,
   "label": "поворачивается"
  },
  {
   "type": "hold",
   "frame": "idle/idle_profile",
   "at": [
    560,
    726
   ],
   "dur": 0.24,
   "flip": false,
   "label": null
  },
  {
   "type": "walk",
   "from": [
    590,
    728
   ],
   "to": [
    1170,
    755
   ],
   "dir": 1,
   "y_ease_until_x": 820,
   "label": "идёт к машине"
  },
  {
   "type": "lean",
   "at": [
    1192,
    755
   ],
   "angle_from": 18,
   "in_s": 0.55,
   "hold_s": 5.0,
   "out_s": 0.45,
   "taps": [
    [
     0.5,
     2.1
    ],
    [
     2.9,
     4.6
    ]
   ],
   "tap_period": 0.42,
   "tap_deg": 7,
   "label": "смотрит на вышивку, притопывает"
  },
  {
   "type": "hold",
   "frame": "idle/idle_main",
   "at": [
    1180,
    755
   ],
   "dur": 0.36,
   "flip": false,
   "label": "разворачивается"
  },
  {
   "type": "hold",
   "frame": "idle/idle_profile",
   "at": [
    1176,
    755
   ],
   "dur": 0.22,
   "flip": true,
   "label": null
  },
  {
   "type": "walk",
   "from": [
    1150,
    755
   ],
   "to": [
    590,
    728
   ],
   "dir": -1,
   "y_ease_until_x": 820,
   "label": "возвращается"
  },
  {
   "type": "hold",
   "frame": "idle/idle_profile",
   "at": [
    565,
    726
   ],
   "dur": 0.2,
   "flip": true,
   "label": null
  },
  {
   "type": "hold",
   "frame": "walk_away/walk_away_02",
   "at": [
    525,
    724
   ],
   "dur": 0.24,
   "flip": true,
   "label": null
  },
  {
   "type": "hold",
   "frame": "walk_away/walk_away_01",
   "at": [
    476,
    722
   ],
   "dur": 0.3,
   "flip": false,
   "label": null
  },
  {
   "type": "sitdown",
   "at": [
    476,
    722
   ],
   "dur": 0.55,
   "label": "садится"
  }
 ],
 "machine": {
  "needle": {
   "file": "01_scene_layers/02b_machine_needle_active.png",
   "stroke_px": 4,
   "hz": 9
  },
  "head": {
   "file": "01_scene_layers/03_machine_head.png",
   "jitter_px": 0.5
  },
  "run_s": 6.5,
  "pause_s": 1.2
 }
};
