#include <gb/gb.h>
#include <gb/cgb.h>
#include <stdint.h>

#include "plugins/dash/engine/src/dash_assets.h"
static const palette_color_t bgpal[]={
RGB(1,2,4),RGB(6,10,13),RGB(18,25,26),RGB(30,30,26),
RGB(1,2,5),RGB(3,6,9),RGB(6,10,13),RGB(30,24,8),
RGB(5,2,4),RGB(14,5,5),RGB(22,8,7),RGB(31,27,20),
RGB(4,3,4),RGB(12,5,6),RGB(19,7,7),RGB(31,27,20),
RGB(0,4,6),RGB(1,8,10),RGB(3,18,19),RGB(21,30,25),
RGB(1,2,4),RGB(5,9,15),RGB(7,19,29),RGB(27,30,31),
RGB(1,2,4),RGB(16,4,7),RGB(30,10,11),RGB(31,28,26),
RGB(1,2,4),RGB(7,9,10),RGB(16,18,18),RGB(29,29,27)};
static const palette_color_t sp[]={RGB(1,2,4),RGB(4,17,30),RGB(31,23,14),RGB(2,3,5),RGB(1,2,4),RGB(30,6,9),RGB(31,23,14),RGB(2,3,5)};
static uint16_t dist[2],ticks,finish[2];
static uint8_t vel[2],last[2],pose[2],oldkeys,state,countdown;
static void text(uint8_t x,uint8_t y,const char *s){uint8_t t,at;uint8_t row[20]={0};
if(y==16){VBK_REG=0;set_bkg_tiles(0,16,20,1,row);for(t=0;t<20;t++)row[t]=8;VBK_REG=1;set_bkg_tiles(0,16,20,1,row);}
while(*s){t=*s++-32;at=8+((y>=3&&y<=5)?(x<10?5:6):0);VBK_REG=0;set_bkg_tiles(x,y,1,1,&t);VBK_REG=1;set_bkg_tiles(x++,y,1,1,&at);}VBK_REG=0;}
static void number(uint8_t x,uint8_t y,uint16_t v){char s[4];s[0]='0'+v/100%10;s[1]='0'+v/10%10;s[2]='0'+v%10;s[3]=0;text(x,y,s);}
static void timer(uint8_t x,uint8_t y,uint16_t f){char s[6];uint16_t sec=f/60;uint8_t dec=(f%60)*100/60;s[0]='0'+sec/10;s[1]='0'+sec%10;s[2]='.';s[3]='0'+dec/10;s[4]='0'+dec%10;s[5]=0;text(x,y,s);}
static void beep(uint8_t high){NR10_REG=0;NR11_REG=0x80;NR12_REG=0x92;NR13_REG=high?0xe0:0x40;NR14_REG=0x87;}
static void screen(void){uint8_t i;DISPLAY_OFF;HIDE_WIN;SCX_REG=0;SCY_REG=0;
VBK_REG=0;set_bkg_data(0,STADIUM_TILE_COUNT,stadium_tiles);set_bkg_tiles(0,0,20,18,stadium_map);
VBK_REG=1;set_bkg_data(0,96,dash_font);set_bkg_tiles(0,0,20,18,stadium_attrs);VBK_REG=0;
set_sprite_data(0,48,dash_runner);set_bkg_palette(0,8,bgpal);set_sprite_palette(0,2,sp);SPRITES_8x16;
for(i=0;i<40;i++)move_sprite(i,0,0);for(i=0;i<12;i++)set_sprite_prop(i,i<6?0:1);
text(3,0,"DASH // DUEL");text(4,1,"100M SPRINT");text(1,3,"P1 BLUE");text(11,3,"P2 RED");timer(2,4,0);timer(12,4,0);number(2,5,0);number(12,5,0);text(5,5,"M");text(15,5,"M");
text(0,17,"P1 < >    P2 A B");SHOW_BKG;SHOW_SPRITES;DISPLAY_ON;}
static void reset_race(void){uint8_t i;for(i=0;i<2;i++){dist[i]=0;vel[i]=0;last[i]=0;pose[i]=0;finish[i]=0;}ticks=0;countdown=180;state=1;text(3,16,"      3       ");beep(0);}
static void runner(uint8_t i){uint8_t j,x=16+(((dist[i]>>8)*7)>>3),y=i?112:80,t=(pose[i]&3)*12;
for(j=0;j<6;j++){set_sprite_tile(i*6+j,t+j*2);move_sprite(i*6+j,x+(j%3)*8,y+(j/3)*16);}}
void main(void) {
uint8_t keys,edge,i,k;
cpu_fast();NR52_REG=0x80;NR50_REG=0x77;NR51_REG=0xff;screen();state=0;dist[0]=dist[1]=0;pose[0]=pose[1]=0;oldkeys=joypad();text(2,16,"START TO RACE!");
while(1){wait_vbl_done();SCX_REG=0;SCY_REG=0;keys=joypad();edge=keys&~oldkeys;oldkeys=keys;
if((state==0||state==3)&&(edge&J_START))reset_race();
if(state==1){countdown--;if(countdown==120){text(8,16,"  2  ");beep(0);}if(countdown==60){text(8,16,"  1  ");beep(0);}if(!countdown){state=2;text(3,16,"     GO!      ");beep(1);}}
else if(state==2){ticks++;for(i=0;i<2;i++){k=i?(edge&(J_A|J_B)):(edge&(J_LEFT|J_RIGHT));if(k && k!=(i?(J_A|J_B):(J_LEFT|J_RIGHT)) && k!=last[i] && !finish[i]){last[i]=k;vel[i]=vel[i]>48?64:vel[i]+16;pose[i]++;}if(!finish[i]){if(vel[i])vel[i]--;dist[i]+=vel[i];if(dist[i]>=32768u){dist[i]=32768u;finish[i]=ticks;beep(1);}}}
if(finish[0]&&finish[1]){number(2,5,100);number(12,5,100);timer(2,4,finish[0]);timer(12,4,finish[1]);state=3;if(finish[0]==finish[1])text(3,16,"TIE! START AGAIN");else text(2,16,finish[0]<finish[1]?"P1 WINS!  START":"P2 WINS!  START");}
if((ticks&7)==0){number(2,5,(((dist[0]>>7)*25)>>6));number(12,5,(((dist[1]>>7)*25)>>6));timer(2,4,finish[0]?finish[0]:ticks);timer(12,4,finish[1]?finish[1]:ticks);}
}
runner(0);runner(1);
}}
