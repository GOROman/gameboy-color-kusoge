from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
random.seed(7)
root=Path(__file__).resolve().parents[1]
# Each 8x8 tile is authored within one four-colour palette.
pals=[[(9,17,32),(52,80,102),(151,205,211),(242,242,214)],[(10,20,40),(26,47,72),(53,81,105),(244,193,65)],[(42,23,32),(113,45,45),(183,69,56),(255,221,167)],[(38,25,38),(101,43,52),(158,60,62),(255,221,167)],[(6,33,48),(10,71,84),(26,151,155),(174,240,204)],[(9,17,32),(40,77,121),(57,153,233),(220,246,255)],[(9,17,32),(133,39,62),(247,86,94),(255,230,215)],[(9,17,32),(57,73,87),(128,145,146),(235,239,219)]]
im=Image.new('RGB',(160,144),pals[0][0]);d=ImageDraw.Draw(im);attr=[]
font=ImageFont.truetype('/System/Library/Fonts/Monaco.ttf',9)
# palette map by tile, consistent per 8x8 tile
for ty in range(18):
 for tx in range(20):
  pal=0 if ty<6 or ty>=16 else 1 if ty<8 else 2 if ty<12 else 3
  if ty in (3,4,5):pal=5 if tx<10 else 6
  attr.append(pal)
  d.rectangle((tx*8,ty*8,tx*8+7,ty*8+7),fill=pals[pal][0 if ty<8 or ty>=16 else 2])
# angled title accents
for x in range(0,160,8):
 d.line((x,0,x+6,6),fill=pals[0][1]);d.line((x,15,x+4,11),fill=pals[0][1])
d.rectangle((0,16,159,17),fill=pals[0][2])
# Individual scoreboard borders in blue and red
for start,p in ((0,5),(80,6)):
 d.rectangle((start,24,start+79,47),outline=pals[p][1]);d.rectangle((start+1,25,start+3,46),fill=pals[p][2])
# crowd: two rows of people + rail
for y in (48,56):
 for x in range(0,160,4):
  c=pals[1][random.choice([2,3])];d.rectangle((x+1,y+1,x+2,y+2),fill=c);d.rectangle((x,y+3,x+3,y+6),fill=pals[1][random.choice([1,2])])
d.line((0,63,159,63),fill=pals[1][3])
# clay athletics lanes, perspective hatch and lane markers
for y0,p in ((64,2),(96,3)):
 d.rectangle((0,y0,159,y0+31),fill=pals[p][2]);d.line((0,y0,159,y0),fill=pals[p][3]);d.line((0,y0+30,159,y0+30),fill=pals[p][3]);d.line((0,y0+31,159,y0+31),fill=pals[p][0])
 for x in range(0,160,24):
  d.line((x,y0+29,x+9,y0+1),fill=pals[p][1])
 for y in range(y0+1,y0+29,4):
  for x in range(136,144,4):
   d.rectangle((x,y,x+3,y+3),fill=pals[p][3 if ((x//4+y//4)&1) else 0])
 d.line((18,y0+1,18,y0+29),fill=pals[p][3])
# convert to local palette indexed tile data and dedup
tiles=[];tilemap=[]
for ty in range(18):
 for tx in range(20):
  pal=pals[attr[ty*20+tx]];data=[]
  for y in range(8):
   vals=[pal.index(im.getpixel((tx*8+x,ty*8+y))) for x in range(8)]
   data += [sum((v&1)<<(7-x) for x,v in enumerate(vals)),sum(((v>>1)&1)<<(7-x) for x,v in enumerate(vals))]
  t=bytes(data)
  if t not in tiles:tiles.append(t)
  tilemap.append(tiles.index(t))
assert len(tiles)<=256,len(tiles)
im.save(root/'art/stadium.png')
# Custom thick 6px readable type, generated into independent VRAM bank.
ft=[]
for c in range(32,128):
 a=Image.new('1',(8,8));ad=ImageDraw.Draw(a);ad.text((1,-2),chr(c),font=font,fill=1,stroke_width=0)
 for y in range(8):
  n=sum(1<<(7-x) for x in range(8) if a.getpixel((x,y)));ft += [n,n]
# Original 24x32 runners. Four distinct sprint poses, solid jersey and skin silhouettes.
sprite=[];sheet=Image.new('RGB',(96,32),(9,17,32))
spal=[(9,17,32),(34,137,243),(250,186,117),(20,30,47)]
for frame in range(4):
 a=Image.new('P',(24,32),0);ad=ImageDraw.Draw(a)
 # rear limbs, bent at elbow/knee
 arms=[[(11,14),(6,12),(4,17)],[(11,14),(6,17),(2,14)],[(11,14),(7,18),(4,16)],[(11,14),(5,13),(3,17)]]
 legs=[([(12,23),(6,26),(2,30)],[(14,23),(19,26),(21,31)]), ([(12,23),(10,28),(15,30)],[(14,23),(20,23),(22,26)]), ([(12,23),(19,27),(22,31)],[(14,23),(8,26),(4,30)]), ([(12,23),(19,23),(21,26)],[(14,23),(10,28),(15,30)])]
 ad.line(arms[frame],fill=3,width=4);ad.line(arms[frame],fill=2,width=2)
 for leg in legs[frame]:ad.line(leg,fill=3,width=4);ad.line(leg,fill=2,width=2);ex,ey=leg[-1];ad.rectangle((ex-1,ey-1,min(23,ex+2),ey),fill=3)
 # shorts and torso leaning forward
 ad.polygon([(10,10),(16,11),(15,21),(10,24),(7,21)],fill=3);ad.polygon([(11,11),(16,12),(14,20),(8,20)],fill=1);ad.rectangle((10,14,13,17),fill=2)
 # neck, face, hair, eye, forward arm
 ad.rectangle((14,8,17,11),fill=2);ad.ellipse((13,2,20,9),fill=3);ad.rectangle((14,4,20,8),fill=2);ad.rectangle((14,2,19,4),fill=3);ad.point((19,5),fill=3);ad.point((21,7),fill=2)
 front=[[(15,12),(19,17),(23,14)],[(15,12),(21,11),(22,7)],[(15,12),(20,10),(21,6)],[(15,12),(20,17),(23,14)]][frame]
 ad.line(front,fill=3,width=4);ad.line(front,fill=2,width=2)
 for x in range(24):
  for y in range(32):sheet.putpixel((frame*24+x,y),spal[a.getpixel((x,y))])
 # tiles in 8x16 hardware sprite pairs, six sprites per runner
 for ty in (0,16):
  for tx in (0,8,16):
   for y in range(ty,ty+16):
    vals=[a.getpixel((tx+x,y)) for x in range(8)];sprite += [sum((v&1)<<(7-x) for x,v in enumerate(vals)),sum(((v>>1)&1)<<(7-x) for x,v in enumerate(vals))]
sheet.save(root/'art/runners.png')
def arr(name,seq):return 'const unsigned char '+name+'[]={'+','.join(map(str,seq))+'};\n'
out=arr('dash_font',ft)+arr('stadium_tiles',b''.join(tiles))+arr('stadium_map',tilemap)+arr('stadium_attrs',attr)+arr('dash_runner',sprite)+f'#define STADIUM_TILE_COUNT {len(tiles)}\n'
(root/'plugins/dash/engine/src/dash_assets.h').write_text(out)
print('Stadium:',len(tiles),'tiles; sprites:',len(sprite)//16,'tiles')
