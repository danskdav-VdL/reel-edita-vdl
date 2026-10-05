#!/bin/bash
# build.sh — reconstruye el vídeo de Albarán Digital de principio a fin (Modo B de reel-edita-jhon).
# check → render → SFX CC0 → endcard → loudness → miniatura (frame 0) → versión ligera
set -e
cd "$(dirname "$0")"
S=~/.claude/skills/reel-edita-jhon/scripts
export HYPERFRAMES_SKIP_SKILLS=1
HF="npx -y hyperframes@0.8.93"
( cd motion && $HF check . --at-transitions --caption-zone "x0=0;y0=.84;x1=1;y1=1;severity=error" | grep -E "◇  Check" )
( cd motion && $HF render --quality high -o renders/cuerpo.mp4 | grep -E "rendered in" )
[ -d motion/sfx ] || bash $S/sfx-kit.sh motion/sfx
ffmpeg -v error -y -i motion/renders/cuerpo.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -shortest -map 0:v -map 1:a \
  -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -c:a aac motion/renders/cuerpo-a.mp4
python3 $S/mix-sfx.py --base motion/renders/cuerpo-a.mp4 --sfx-dir motion/sfx --out motion/renders/cuerpo-sfx.mp4 \
 --events '[["impactWood_medium_002",0.2],["card-place-1",0.45],["card-place-2",0.75],["card-slide-2",3.2],["drop_001",3.9],["drop_002",4.3],["card-slide-5",7.2],["click_002",8.55],["impactPlate_light_001",8.85],["card-slide-3",11.8],["switch_004",11.95],["impactGlass_light_002",15.3],["card-slide-7",16.4],["drop_001",16.9],["drop_002",17.4],["drop_003",17.9],["drop_001",18.4],["card-slide-1",20.0],["impactWood_light_001",20.6],["impactBell_heavy_000",21.15]]' \
 --vol '{"impactWood_medium_002":0.8,"card-place-1":0.7,"card-place-2":0.7,"card-slide-2":0.75,"card-slide-5":0.75,"card-slide-3":0.75,"card-slide-7":0.75,"card-slide-1":0.7,"drop_001":0.55,"drop_002":0.55,"drop_003":0.55,"click_002":0.7,"impactPlate_light_001":0.5,"switch_004":0.6,"impactGlass_light_002":0.5,"impactWood_light_001":0.7,"impactBell_heavy_000":0.55}'
bash $S/cierre.sh motion/renders/cuerpo-sfx.mp4 motion/renders/con-cierre.mp4 0.5 | tail -1
ffmpeg -v error -y -i motion/renders/con-cierre.mp4 -c:v copy -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 \
  -c:a aac -b:a 192k -movflags +faststart AF/VIDEO-albaran-digital-FINAL.mp4
bash $S/poster.sh AF/VIDEO-albaran-digital-FINAL.mp4 2.6
ffmpeg -v error -y -i AF/VIDEO-albaran-digital-FINAL.mp4 -c:v libx264 -crf 26 -preset slow -maxrate 8M -bufsize 16M \
  -pix_fmt yuv420p -c:a copy -movflags +faststart AF/VIDEO-albaran-digital-ligero.mp4
ls -la AF
