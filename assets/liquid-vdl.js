// liquid-vdl.js — Fondo LIQUID VdL v2 (2026-10-02): campo de flujo en WebGL con cintas de seda, función pura del tiempo (determinista).
// Uso: const L = liquidVdL(canvas, {scale:0.5}); L.draw(t)   (t en segundos; determinista)
// Paleta: navy profundo #00002B → navy #00004b → violeta #3a2770 → magenta #b41e82 → lila #c865d1; lime #aae05a solo en brillos.
window.liquidVdL = function (canvas, opts) {
  opts = opts || {};
  const S = opts.scale || 0.5;
  const W = Math.round(1080 * S), H = Math.round(1920 * S);
  canvas.width = W; canvas.height = H;
  const gl = canvas.getContext("webgl", { preserveDrawingBuffer: true, antialias: false, premultipliedAlpha: false });
  const vs = "attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}";
  const fs = `
precision highp float;
uniform vec2 uRes; uniform float uT; uniform float uEnergy; uniform float uLime; uniform vec2 uGlow;
float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);
  return mix(mix(h(i),h(i+vec2(1,0)),u.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),u.x),u.y);}
float fbm(vec2 p){float v=0.,a=.55;mat2 m=mat2(1.7,1.1,-1.1,1.7);for(int i=0;i<4;i++){v+=a*n(p);p=m*p+vec2(3.1,1.7);a*=.48;}return v;}
vec3 deep=vec3(0.,0.,.169), navy=vec3(0.,0.,.294), violet=vec3(.227,.153,.439), mag=vec3(.706,.118,.510),
     lilac=vec3(.784,.396,.820), lime=vec3(.667,.878,.353);
void main(){
  vec2 uv=gl_FragCoord.xy/uRes;                       // (0,0) abajo-izquierda
  vec2 p=(uv-.5)*vec2(uRes.x/uRes.y,1.)*1.15;
  float t=uT*uEnergy;
  // campo de flujo lento a gran escala (domain warp suave)
  vec2 q=vec2(fbm(p*.85+vec2(t*.030,t*.012)), fbm(p*.85+vec2(4.3,1.9)-vec2(t*.018,t*.026)));
  vec2 w=p+1.35*(q-.5);
  float d=fbm(w*1.25+vec2(-t*.02,t*.015));
  // cintas de seda (aurora): tres familias de ondas deformadas por el flujo, cada una a su velocidad
  float s1=sin(w.y*5.2+w.x*1.6+d*5.0-t*.21);
  float s2=sin(w.y*4.6-w.x*2.3+d*4.0+t*.15+1.7);
  float s3=sin(w.y*7.9+w.x*.9+d*6.5-t*.27+4.1);
  float rib1=pow(smoothstep(.20,1.,s1),2.2);
  float rib2=pow(smoothstep(.35,1.,s2),2.0);
  float fil1=exp(-abs(s1-.86)*26.);               // filo de luz fino (pliegue de seda)
  float fil3=exp(-abs(s3-.92)*34.)*smoothstep(.3,.7,d);
  // base: navy profundo arriba -> navy -> horizonte violeta abajo
  vec3 col=mix(navy, deep, smoothstep(.10,1.,uv.y));
  float hor=exp(-pow((uv.y-.08)*2.4,2.))*(.6+.4*d);
  col=mix(col, violet, hor*.70);
  float gl=exp(-dot((uv-uGlow)*vec2(1.,1.6),(uv-uGlow)*vec2(1.,1.6))*5.);
  col=mix(col, violet, gl*.50);
  // cintas: magenta (más presencia abajo), violeta claro, filos lila
  col=mix(col, mag, rib1*(.26+.40*(1.-uv.y)+.42*gl)*(.6+.4*d));
  col=mix(col, violet*1.35, rib2*(.42+.30*gl));
  col+=lilac*fil1*.10*(.4+.6*(1.-uv.y));
  col+=lilac*fil3*.07;
  // lime: destello raro en el filo más alto (nunca un charco)
  col+=lime*fil1*smoothstep(.50,.82,d)*.30*uLime;
  // barrido de luz diagonal muy lento (sensación de cristal)
  float sw=exp(-pow((uv.x*.55+uv.y*.85)-fract(uT*.028)*2.4+.4,2.)*22.);
  col+=vec3(.45,.42,.85)*sw*.03;
  // viñeta + grano fino sin patrón (hash entero por frame)
  float vig=smoothstep(1.3,.2,length((uv-vec2(.5,.45))*vec2(1.,.85)));
  col*=.60+.40*vig;
  float fr=mod(floor(uT*30.),64.);
  vec2 gp=floor(gl_FragCoord.xy)+vec2(fr*13.,fr*29.);
  float g=fract(sin(dot(mod(gp,vec2(997.,991.)),vec2(12.9898,78.233)))*43758.5453);
  col+=(g-.5)*.020;
  gl_FragColor=vec4(col,1.);
}`;
  function sh(type, src) { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; }
  const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(pr); gl.useProgram(pr);
  const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(pr, "a"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const uRes = gl.getUniformLocation(pr, "uRes"), uT = gl.getUniformLocation(pr, "uT"),
        uE = gl.getUniformLocation(pr, "uEnergy"), uL = gl.getUniformLocation(pr, "uLime"), uG = gl.getUniformLocation(pr, "uGlow");
  gl.viewport(0, 0, W, H); gl.uniform2f(uRes, W, H);
  const state = { energy: 1, lime: 1, gx: .5, gy: .6 };
  function draw(t) {
    gl.uniform1f(uT, t); gl.uniform1f(uE, state.energy); gl.uniform1f(uL, state.lime); gl.uniform2f(uG, state.gx, state.gy);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  draw(0);
  return { draw, state };
};
