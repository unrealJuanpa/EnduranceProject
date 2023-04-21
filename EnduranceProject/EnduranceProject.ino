// servos
#include <Servo.h>
Servo hix, hiy, cix, ciy, mix, miy;// brazo - izquierda
Servo hdx, hdy, cdx, cdy, mdx, mdy;// brazo - derecha
Servo dpx, dix, dmx, dax, dzx, dpy, diy, dmy, day, dzy;// mano - derecha
Servo ipx, iix, imx, iax, izx, ipy, iiy, imy, iay, izy;// mano - izquierdo
//

// control
int a,c;
char e;
bool b=true;
//

void setup() {
  Serial1.begin(9600);

  ipx.attach(44); ipy.attach(49);
  iix.attach(45); iiy.attach(50);
  imx.attach(46); imy.attach(51);
  iax.attach(47); iay.attach(52);
  izx.attach(48); izy.attach(53);
//attach
  // brazo izquierdo
  //hix.attach(22); hiy.attach(23);
  //cix.attach(24); ciy.attach(25);
  //mix.attach(26); miy.attach(27);
  
  // brazo derecho
  hdx.attach(28); hdy.attach(29);
  cdx.attach(30); cdy.attach(31);
  mdx.attach(32); mdy.attach(33);
  // mano derecha
  dpx.attach(34); dpy.attach(39);
  dix.attach(35); diy.attach(40);
  dmx.attach(36); dmy.attach(41);
  dax.attach(37); day.attach(42);
  dzx.attach(38); dzy.attach(43);
//fin attach

// escritura inicial
  // lado izquierdo
  /*
  hix.write(0);
  hiy.write(126);
  cix.write(115);
  ciy.write(85);
  mix.write(126);
  miy.write(150);
  */
  // lado derecho
  hdx.write(180);
  hdy.write(126);
  cdx.write(115);
  cdy.write(85);
  mdx.write(126);
  mdy.write(150);
  
  ipx.write(95); ipy.write(0);
  iix.write(100); iiy.write(0);
  imx.write(100); imy.write(0);
  iax.write(90); iay.write(0);
  izx.write(75); izy.write(0);
  // mano derecha
  dpx.write(90); dpy.write(90);
  dix.write(90); diy.write(90);
  dmx.write(90); dmy.write(90);
  dax.write(90); day.write(90);
  dzx.write(90); dzy.write(90);
  
//
}

void Wr(int x, int y) {
  /*
  if (x==0) hix.write(y);
  if (x==1) hiy.write(y);
  if (x==2) cix.write(y);
  if (x==3) ciy.write(y);
  if (x==4) mix.write(y);
  if (x==5) miy.write(y);
  */
  if (x==6) hdx.write(y);
  if (x==7) hdy.write(y);
  if (x==8) cdx.write(y);
  if (x==9) cdy.write(y);
  if (x==10) mdx.write(y);
  if (x==11) mdy.write(y);

  if (x==12) dpx.write(y);
  if (x==13) dpy.write(y);
  if (x==14) dix.write(y);
  if (x==15) diy.write(y);
  if (x==16) dmx.write(y);
  if (x==17) dmy.write(y);
  if (x==18) dax.write(y);
  if (x==19) day.write(y);
  if (x==20) dzx.write(y);
  if (x==21) dzy.write(y);

  if (x==22) ipy.write(y);
  if (x==23) iiy.write(y);
  if (x==24) imy.write(y);
  if (x==25) iay.write(y);
  if (x==26) izy.write(y);
}

void loop() {
  if (Serial1.available()>0) {
    e=Serial1.read();
    if (e>=32) {
      if (b) {
        a=e;
        a-=32;
      }
      else {
        c=e;
        c=(c-32)*1.91489;
        Wr(a,c);
      }
      b=!b;
    }
  }
}
