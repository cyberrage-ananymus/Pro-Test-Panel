# pages.py - Cyber-Rage v2.0
# Login, Dashboard, Public subscription page
# Font: Space Grotesk + JetBrains Mono
# Icons: Phosphor Icons

import json
from urllib.parse import quote

def get_public_page_html(uuid_key: str) -> str:
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cyber-Rage</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/regular/style.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Space Grotesk',system-ui,sans-serif;background:#0a0a1a;color:#e0f0ff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.card{background:rgba(15,25,50,0.8);border:1px solid rgba(0,240,255,0.12);border-radius:20px;padding:32px;max-width:520px;width:100%;backdrop-filter:blur(24px)}
h1{font-size:22px;font-weight:700;margin-bottom:6px;background:linear-gradient(135deg,#00f0ff,#ff00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{color:#667;font-size:13px;margin-bottom:20px;line-height:1.5}
.locked{background:rgba(255,0,100,0.08);border:1px solid rgba(255,0,100,0.2);border-radius:14px;padding:24px;text-align:center}
.locked input{background:rgba(0,0,0,0.3);border:1px solid rgba(0,240,255,0.2);border-radius:10px;padding:11px 16px;color:#fff;width:100%;margin:12px 0;font-size:14px;font-family:inherit}
.locked button{background:linear-gradient(135deg,#00f0ff,#8b5cf6);color:#fff;border:none;border-radius:10px;padding:11px 28px;cursor:pointer;font-size:14px;font-family:inherit;font-weight:600}
.link-item{background:rgba(0,0,0,0.2);border:1px solid rgba(0,240,255,0.08);border-radius:12px;padding:16px;margin-bottom:10px}
.link-name{font-weight:700;margin-bottom:6px;display:flex;align-items:center;gap:8px}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.dot.g{background:#00f0ff}.dot.r{background:#ff0066}
.link-info{font-size:12px;color:#8899aa;line-height:1.8}
.link-url{font-size:11px;color:#00f0ff;background:rgba(0,240,255,0.06);padding:8px 12px;border-radius:8px;margin-top:10px;word-break:break-all;font-family:'JetBrains Mono',monospace;cursor:pointer;transition:.15s}
.link-url:hover{background:rgba(0,240,255,0.12)}
.btn{display:inline-block;background:linear-gradient(135deg,#00f0ff,#8b5cf6);color:#fff;border:none;border-radius:10px;padding:9px 18px;cursor:pointer;font-size:12px;font-weight:600;margin-top:10px;text-decoration:none;font-family:inherit}
.progress-bar{height:4px;background:rgba(0,240,255,0.1);border-radius:4px;margin-top:8px;overflow:hidden}
.progress-fill{height:100%;background:linear-gradient(90deg,#00f0ff,#8b5cf6);border-radius:4px;transition:width .3s}
</style>
</head>
<body>
<div class="card" id="app">
<div id="loading" style="text-align:center;padding:40px"><div style="font-size:16px;color:#889">Loading...</div></div>
</div>
<script>
const UK='""" + uuid_key + r"""';
async function init(){
  try{
    const r=await fetch('/api/public/sub/'+UK);
    const d=await r.json();
    if(d.locked){
      document.getElementById('app').innerHTML=`<div class="locked"><h1 style="margin-bottom:10px;-webkit-text-fill-color:#fff">${d.name}</h1><p style="color:#889;font-size:13px">This group is password protected</p><input type="password" id="pw" placeholder="Enter password"><button onclick="unlock()">Unlock</button></div>`;
      return;
    }
    render(d);
  }catch(e){document.getElementById('app').innerHTML='<div style="text-align:center;padding:40px;color:#ff4488">Error loading</div>';}
}
async function unlock(){
  const pw=document.getElementById('pw').value;
  const r=await fetch('/api/public/sub/'+UK+'?pw='+encodeURIComponent(pw));
  const d=await r.json();
  if(d.locked){alert('Wrong password');return;}
  render(d);
}
function render(d){
  let html=`<h1>${d.name}</h1><div class="sub">${d.desc||''} &bull; ${d.total_used_fmt} used &bull; ${d.active_connections} active</div>`;
  d.links.forEach(l=>{
    const status=l.active?'<span class="dot g"></span>':'<span class="dot r"></span>';
    const pct=l.limit_bytes>0?Math.min(100,(l.used_bytes/l.limit_bytes)*100):0;
    const bar=l.limit_bytes>0?`<div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>`:'';
    html+=`<div class="link-item"><div class="link-name">${status} ${l.label}</div><div class="link-info">${l.used_fmt} / ${l.limit_fmt} &bull; ${l.protocol} &bull; ${l.connections} connections</div>${bar}<div class="link-url" onclick="copy(this)">${l.vless_link}</div><a class="btn" href="${l.sub_url}" target="_blank">Sub Link</a></div>`;
  });
  document.getElementById('app').innerHTML=html;
}
function copy(el){navigator.clipboard.writeText(el.textContent).then(()=>{el.style.background='rgba(0,240,255,0.2)';setTimeout(()=>{el.style.background=''},800)});}
init();
</script>
</body></html>"""


LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cyber-Rage | Login</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/regular/style.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0a1a;--card:rgba(15,25,50,0.85);--accent:#00f0ff;--accent2:#8b5cf6;--text:#e0f0ff;--dim:#556688;--mid:#8899aa;--border:rgba(0,240,255,0.12)}
body{font-family:'Space Grotesk',system-ui,sans-serif;background:var(--bg);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;overflow:hidden}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(0,240,255,0.06),transparent 70%),var(--bg);z-index:0}
.grid{position:fixed;inset:0;background-image:linear-gradient(rgba(0,240,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,240,255,0.03) 1px,transparent 1px);background-size:50px 50px;z-index:0}
.orb{position:fixed;border-radius:50%;filter:blur(100px);z-index:0;animation:float 10s ease-in-out infinite}
.o1{width:400px;height:400px;background:rgba(0,240,255,0.06);top:-120px;right:-100px}
.o2{width:300px;height:300px;background:rgba(255,0,255,0.04);bottom:-80px;left:-80px;animation-delay:5s}
.o3{width:250px;height:250px;background:rgba(139,92,246,0.05);top:50%;left:50%;animation-delay:3s}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)}}
.wrap{position:relative;z-index:10;width:100%;max-width:420px}
.card{background:var(--card);border:1px solid var(--border);border-radius:24px;padding:40px 36px 36px;backdrop-filter:blur(30px);box-shadow:0 0 100px rgba(0,240,255,0.05),0 25px 60px rgba(0,0,0,.6)}
.brand{display:flex;align-items:center;gap:14px;margin-bottom:30px}
.brand-icon{width:52px;height:52px;border-radius:14px;background:linear-gradient(135deg,#00f0ff,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:#fff;box-shadow:0 0 30px rgba(0,240,255,0.3),0 0 20px rgba(139,92,246,0.2)}
.brand-name{font-size:18px;font-weight:700;color:var(--text);letter-spacing:-.02em}
.brand-sub{font-size:11px;color:var(--dim);margin-top:2px;letter-spacing:.05em}
h1{font-size:24px;font-weight:700;color:var(--text);margin-bottom:6px;letter-spacing:-.02em}
.sub{font-size:13px;color:var(--mid);margin-bottom:26px;line-height:1.6}
.hint{display:flex;align-items:center;gap:12px;background:rgba(0,240,255,0.05);border:1px solid rgba(0,240,255,0.1);border-radius:12px;padding:12px 16px;margin-bottom:22px}
.hint-label{font-size:11px;color:var(--dim);flex:1}
.hint-val{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:700;color:var(--accent);background:rgba(0,240,255,0.08);border:1px solid rgba(0,240,255,0.2);padding:4px 14px;border-radius:8px;cursor:pointer;transition:.15s;letter-spacing:.08em}
.hint-val:hover{background:rgba(0,240,255,0.18)}
.field{margin-bottom:20px}
.field label{display:block;font-size:11px;font-weight:600;color:var(--mid);margin-bottom:8px;text-transform:uppercase;letter-spacing:.08em}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:14px 46px 14px 18px;border-radius:12px;border:1px solid var(--border);background:rgba(0,0,0,.3);color:var(--text);font-family:inherit;font-size:15px;outline:none;transition:.2s}
input[type=password]:focus{border-color:rgba(0,240,255,.4);background:rgba(0,0,0,.4);box-shadow:0 0 0 4px rgba(0,240,255,.08)}
.ic{position:absolute;left:16px;top:50%;transform:translateY(-50%);color:var(--dim);font-size:18px;transition:.2s}
input:focus~.ic{color:var(--accent)}
.err{display:none;background:rgba(255,0,100,.08);border:1px solid rgba(255,0,100,.2);border-radius:12px;padding:12px 16px;margin-bottom:16px;font-size:13px;color:#ff6688;align-items:center;gap:8px}
.err.show{display:flex}
.btn{width:100%;padding:14px;border-radius:12px;border:none;cursor:pointer;background:linear-gradient(135deg,#00f0ff,#8b5cf6);color:#fff;font-family:inherit;font-size:15px;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 24px rgba(0,240,255,.3);transition:.2s;position:relative;overflow:hidden}
.btn::before{content:'';position:absolute;inset:0;background:rgba(255,255,255,.08);opacity:0;transition:.2s}
.btn:hover::before{opacity:1}
.btn:disabled{opacity:.5;cursor:not-allowed}
.footer{margin-top:24px;text-align:center;font-size:11px;color:var(--dim)}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg"></div><div class="grid"></div>
<div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>
<div class="wrap">
  <div class="card">
    <div class="brand">
      <div class="brand-icon">CR</div>
      <div><div class="brand-name">Cyber-Rage</div><div class="brand-sub">v2.0 GATEWAY</div></div>
    </div>
    <h1>Access Panel</h1>
    <p class="sub">Enter your password to access the dashboard</p>
    <div class="err" id="err"><span id="err-text"></span></div>
    <div class="hint">
      <span class="hint-label">Default password</span>
      <span class="hint-val" onclick="document.getElementById('pw').value='CYBERRAGE';document.getElementById('pw').focus()">CYBERRAGE</span>
    </div>
    <form id="form">
      <div class="field">
        <label>Password</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="Enter your password" autofocus required>
          <span class="ic ph ph-lock"></span>
        </div>
      </div>
      <button class="btn" type="submit" id="btn"><i class="ph ph-arrow-right"></i> Login to Dashboard</button>
    </form>
    <div class="footer">Cyber-Rage &bull; VLESS Gateway</div>
  </div>
</div>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<span style="animation:spin 1s linear infinite;display:inline-block"><i class="ph ph-spinner"></i></span> Authenticating...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'Error');}
    location.href='/dashboard';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ph ph-arrow-right"></i> Login to Dashboard';
  }
});
</script>
</body></html>"""


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cyber-Rage</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/regular/style.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0a0a1a;--bg2:#0e1225;--bg3:#141a30;
  --card:#0f1932;--card-b:rgba(0,240,255,0.08);--card-bh:rgba(0,240,255,0.2);
  --accent:#00f0ff;--accent2:#8b5cf6;--accent-d:rgba(0,240,255,0.06);
  --green:#00f0aa;--green-bg:rgba(0,240,170,0.08);--green-t:#00d4a0;
  --red:#ff0066;--red-bg:rgba(255,0,100,0.08);--red-t:#ff4488;
  --amber:#ffaa00;--amber-bg:rgba(255,170,0,0.08);--amber-t:#ffcc44;
  --purple:#8b5cf6;--purple-bg:rgba(139,92,246,0.08);
  --t1:#e0f0ff;--t2:#8899aa;--t3:#556688;
  --sidebar-w:260px;--radius:16px;
  --shadow:0 4px 24px rgba(0,0,0,0.4);
}
[data-theme="light"]{
  --bg:#f0f4fa;--bg2:#e4edf9;--bg3:#d5e3f5;
  --card:#ffffff;--card-b:rgba(0,150,200,0.1);--card-bh:rgba(0,150,200,0.25);
  --accent:#0096c8;--accent2:#7c3aed;--accent-d:rgba(0,150,200,0.06);
  --green:#059669;--green-bg:rgba(5,150,105,0.08);--green-t:#065f46;
  --red:#dc2626;--red-bg:rgba(220,38,38,0.08);--red-t:#991b1b;
  --amber:#d97706;--amber-bg:rgba(217,119,6,0.08);--amber-t:#92400e;
  --purple:#7c3aed;--purple-bg:rgba(124,58,237,0.08);
  --t1:#0f172a;--t2:#334155;--t3:#64748b;
  --shadow:0 4px 20px rgba(0,0,0,0.08);
}
html,body{height:100%}
body{font-family:'Space Grotesk',system-ui,sans-serif;background:var(--bg);color:var(--t1);min-height:100vh;display:flex;font-size:14px;transition:background .3s,color .3s}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:3px}
a{color:inherit;text-decoration:none}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--bg2);border-left:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:background .3s,border-color .3s,transform .25s}
.logo{display:flex;align-items:center;gap:12px;padding:22px 18px 18px;border-bottom:1px solid var(--card-b)}
.logo-icon{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#00f0ff,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;color:#fff;box-shadow:0 0 20px rgba(0,240,255,0.3);flex-shrink:0}
.logo-name{font-size:15px;font-weight:700;color:var(--t1)}
.logo-sub{font-size:10px;color:var(--t3);margin-top:2px;letter-spacing:.05em}
.sb-close{display:none;position:absolute;left:12px;top:22px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:32px;height:32px;border-radius:8px;font-size:16px;align-items:center;justify-content:center;cursor:pointer}
.nav-wrap{flex:1;overflow-y:auto;padding:8px 0}
.nav-sec{padding:16px 16px 6px;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--t3);font-weight:700}
.nav-it{display:flex;align-items:center;gap:10px;padding:10px 16px;color:var(--t3);font-size:13px;cursor:pointer;border-right:2px solid transparent;transition:all .15s;margin:1px 8px;border-radius:8px 0 0 8px}
.nav-it:hover{background:var(--accent-d);color:var(--t2)}
.nav-it.on{background:var(--accent-d);color:var(--t1);border-right-color:var(--accent);font-weight:600}
.nav-it i{font-size:18px;width:20px;text-align:center;flex-shrink:0}
.nav-badge{margin-right:auto;background:rgba(0,240,255,0.1);color:var(--accent);font-size:10px;padding:2px 8px;border-radius:20px;font-weight:700}
.sb-foot{padding:14px 16px;border-top:1px solid var(--card-b)}
.sb-btn{display:flex;align-items:center;justify-content:center;gap:8px;border-radius:10px;padding:10px;font-size:12.5px;font-weight:500;font-family:inherit;border:1px solid var(--card-b);cursor:pointer;width:100%;transition:.15s;margin-bottom:6px;color:var(--t2)}
.sb-btn:hover{filter:brightness(1.2);background:var(--accent-d)}
.sb-logout{background:var(--red-bg);color:var(--red-t);border-color:rgba(255,0,100,0.15)}
.sb-logout:hover{background:rgba(255,0,100,0.15)}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:54px;background:var(--bg2);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 16px;transition:background .3s}
.mob-top .ml{display:flex;align-items:center;gap:10px}
.mob-logo{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#00f0ff,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:#fff}
.mob-title{color:var(--t1);font-size:14px;font-weight:700}
.mob-right{display:flex;gap:8px}
.menu-btn,.theme-mob{background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:36px;height:36px;border-radius:9px;font-size:18px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:190;backdrop-filter:blur(4px)}
.overlay.show{display:block}
.main{margin-right:var(--sidebar-w);flex:1;padding:30px 30px 70px;min-width:0;transition:margin .25s}
.pg{display:none}
.pg.on{display:block;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:20px;font-weight:700;color:var(--t1);letter-spacing:-.02em;display:flex;align-items:center;gap:8px}
.tb-title i{color:var(--accent);font-size:22px}
.tb-sub{font-size:12px;color:var(--t3);margin-top:4px}
.tb-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.badge{font-size:10px;padding:4px 12px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent)}
.bg-amber{background:var(--amber-bg);color:var(--amber-t)}
.bg-red{background:var(--red-bg);color:var(--red-t)}
.bg-purple{background:var(--purple-bg);color:var(--purple)}
.dot{width:6px;height:6px;border-radius:50%;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}.da{background:var(--amber)}.db{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}
.metric{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:18px;transition:all .2s;position:relative;overflow:hidden;cursor:default}
.metric::after{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--accent);opacity:0;transition:.2s}
.metric:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.metric:hover::after{opacity:1}
.metric.suc::after{background:var(--green)}
.metric.dan::after{background:var(--red)}
.m-icon{width:36px;height:36px;border-radius:10px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;margin-bottom:12px;color:var(--accent);font-size:18px}
.m-icon.suc{background:var(--green-bg);color:var(--green)}
.m-icon.dan{background:var(--red-bg);color:var(--red)}
.m-icon.pur{background:var(--purple-bg);color:var(--purple)}
.m-label{font-size:11px;color:var(--t3);margin-bottom:4px;font-weight:600;text-transform:uppercase;letter-spacing:.06em}
.m-val{font-size:26px;font-weight:700;color:var(--t1);line-height:1;letter-spacing:-.02em}
.m-unit{font-size:13px;font-weight:400;color:var(--t3)}
.m-sub{font-size:11px;color:var(--t3);margin-top:6px;display:flex;align-items:center;gap:3px}
.vless-box{background:linear-gradient(135deg,var(--bg3) 0%,var(--bg2) 100%);border:1px solid var(--card-b);border-radius:18px;padding:22px;margin-bottom:20px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.vless-box::before{content:'';position:absolute;top:-50px;left:-50px;width:200px;height:200px;background:radial-gradient(circle,rgba(0,240,255,0.06),transparent 70%);pointer-events:none}
.vl-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px}
.vl-title{color:var(--t2);font-size:12px;display:flex;align-items:center;gap:6px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.vl-title i{color:var(--accent);font-size:16px}
.vl-code{background:rgba(0,0,0,.2);border:1px solid var(--card-b);border-radius:10px;padding:14px 16px;font-size:11.5px;font-family:'JetBrains Mono',monospace;color:var(--accent);word-break:break-all;line-height:1.8;letter-spacing:.01em}
[data-theme="light"] .vl-code{background:rgba(0,0,0,.04)}
.vl-actions{display:flex;gap:8px;margin-top:14px;flex-wrap:wrap}
.btn{font-family:inherit;font-size:12.5px;font-weight:500;border-radius:9px;padding:9px 16px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border:none;transition:all .15s;white-space:nowrap}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-p{background:linear-gradient(135deg,#00f0ff,#8b5cf6);color:#fff;box-shadow:0 2px 14px rgba(0,240,255,.25)}
.btn-p:hover{box-shadow:0 4px 18px rgba(0,240,255,.35)}
.btn-o{background:transparent;border:1px solid var(--card-b);color:var(--t2)}
.btn-o:hover{background:var(--accent-d);border-color:rgba(0,240,255,.25)}
.btn-g{background:var(--accent-d);color:var(--accent);border:1px solid rgba(0,240,255,.1)}
.btn-g:hover{background:rgba(0,240,255,.15)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(255,0,100,.15)}
.btn-d:hover{background:rgba(255,0,100,.15)}
.btn-sm{padding:6px 10px;font-size:11px;border-radius:7px}
.card{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:20px;transition:border-color .2s,background .3s}
.card:hover{border-color:var(--card-bh)}
.card-title{font-size:13px;font-weight:700;color:var(--t1);margin-bottom:16px;display:flex;align-items:center;gap:8px}
.card-title i{font-size:17px;color:var(--accent)}
.ml-auto{margin-right:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:18px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:18px}
.mb18{margin-bottom:18px}
.sr{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(0,240,255,0.04);font-size:12.5px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:6px}
.sr-v{color:var(--t1);font-weight:600;font-size:12px}
.ch{position:relative;height:240px}
.ch-lg{position:relative;height:340px}
.ch-sm{position:relative;height:195px}
.exp-chip{font-size:9.5px;padding:3px 10px;border-radius:6px;font-weight:700;display:inline-flex;align-items:center;gap:3px}
.ec-ok{background:var(--green-bg);color:var(--green-t)}
.ec-warn{background:var(--amber-bg);color:var(--amber-t)}
.ec-exp{background:var(--red-bg);color:var(--red-t)}
.ec-inf{background:var(--accent-d);color:var(--accent)}
.form-row{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end}
.fg{display:flex;flex-direction:column;gap:6px;flex:1;min-width:120px}
.fg label{font-size:10.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.fi,.fs{padding:10px 14px;border-radius:10px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:13px;outline:none;transition:.15s}
[data-theme="light"] .fi,[data-theme="light"] .fs{background:rgba(0,0,0,.04)}
.fi::placeholder{color:var(--t3)}
.fi:focus,.fs:focus{border-color:rgba(0,240,255,.35);box-shadow:0 0 0 3px rgba(0,240,255,.06)}
.fs option{background:var(--bg2)}
.list-item{display:flex;align-items:center;gap:12px;padding:14px;border:1px solid var(--card-b);border-radius:12px;margin-bottom:8px;transition:.15s;cursor:default}
.list-item:hover{border-color:var(--card-bh);background:rgba(0,240,255,0.02)}
[data-theme="light"] .list-item:hover{background:rgba(0,150,200,0.03)}
.list-icon{width:36px;height:36px;border-radius:10px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;color:var(--accent);font-size:16px;flex-shrink:0}
.list-info{flex:1;min-width:0}
.list-name{font-size:13px;font-weight:600;color:var(--t1);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;align-items:center;gap:8px}
.list-sub{font-size:11px;color:var(--t3);margin-top:3px}
.list-actions{display:flex;gap:6px;flex-shrink:0}
.progress-bar{height:4px;background:var(--accent-d);border-radius:4px;margin-top:8px;overflow:hidden;max-width:200px}
.progress-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));border-radius:4px;transition:width .3s}
.progress-text{font-size:10px;color:var(--t3);margin-top:4px;font-family:'JetBrains Mono',monospace}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:300;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
.modal-bg.show{display:flex}
.modal{background:var(--bg2);border:1px solid var(--card-b);border-radius:20px;padding:28px;width:90%;max-width:520px;max-height:85vh;overflow-y:auto;transition:background .3s}
.modal h2{font-size:18px;font-weight:700;margin-bottom:18px;display:flex;align-items:center;gap:8px}
.modal h2 i{color:var(--accent)}
.modal .form-row{margin-bottom:14px}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--green);color:#fff;padding:12px 24px;border-radius:12px;font-size:13px;font-weight:600;z-index:999;animation:slideUp .3s ease;box-shadow:0 4px 20px rgba(0,240,170,.3)}
@keyframes slideUp{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
.empty{text-align:center;padding:40px;color:var(--t3);font-size:13px}
.empty i{font-size:40px;color:var(--t3);margin-bottom:12px;display:block;opacity:.3}
.conn-row{display:flex;align-items:center;gap:12px;padding:11px 14px;border-bottom:1px solid rgba(0,240,255,0.04);font-size:12.5px}
.conn-row:last-child{border-bottom:none}
.conn-ip{font-family:'JetBrains Mono',monospace;color:var(--accent);font-weight:600;min-width:120px}
.conn-label{color:var(--t2);flex:1}
.conn-bytes{color:var(--t1);font-weight:600;font-family:'JetBrains Mono',monospace;font-size:11px}
.conn-sessions{color:var(--t3);font-size:11px}
.log-entry{padding:8px 12px;border-bottom:1px solid rgba(0,240,255,0.03);font-size:12px;display:flex;gap:10px;align-items:flex-start}
.log-entry:last-child{border-bottom:none}
.log-time{color:var(--t3);font-family:'JetBrains Mono',monospace;font-size:10px;white-space:nowrap;flex-shrink:0}
.log-msg{color:var(--t2);flex:1}
.log-ok .log-msg{color:var(--green-t)}
.log-err .log-msg{color:var(--red-t)}
.log-warn .log-msg{color:var(--amber-t)}
@media(max-width:900px){
  .sidebar{transform:translateX(100%)}
  .sidebar.open{transform:translateX(0)}
  .sb-close{display:flex}
  .mob-top{display:flex}
  .main{margin-right:0;padding-top:74px}
  .metrics{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:520px){
  .metrics{grid-template-columns:1fr}
  .g2,.g3{grid-template-columns:1fr}
  .form-row{flex-direction:column}
  .fg{min-width:0}
}
</style>
</head>
<body>
<div class="mob-top">
  <div class="ml"><div class="mob-logo">CR</div><div class="mob-title">Cyber-Rage</div></div>
  <div class="mob-right">
    <button class="theme-mob" onclick="toggleTheme()"><i class="ph ph-moon"></i></button>
    <button class="menu-btn" onclick="toggleSidebar()"><i class="ph ph-list"></i></button>
  </div>
</div>
<div class="overlay" id="overlay" onclick="toggleSidebar()"></div>

<aside class="sidebar" id="sidebar">
  <div class="logo">
    <div class="logo-icon">CR</div>
    <div><div class="logo-name">Cyber-Rage</div><div class="logo-sub">v2.0 GATEWAY</div></div>
    <button class="sb-close" onclick="toggleSidebar()"><i class="ph ph-x"></i></button>
  </div>
  <div class="nav-wrap">
    <div class="nav-sec">Main</div>
    <div class="nav-it on" data-pg="overview" onclick="showPg(this)"><i class="ph ph-squares-four"></i> Overview</div>
    <div class="nav-it" data-pg="connections" onclick="showPg(this)"><i class="ph ph-gear-six"></i> Connections <span class="nav-badge" id="conn-badge">0</span></div>
    <div class="nav-sec">Management</div>
    <div class="nav-it" data-pg="links" onclick="showPg(this)"><i class="ph ph-link"></i> Configs <span class="nav-badge" id="links-badge">0</span></div>
    <div class="nav-it" data-pg="subs" onclick="showPg(this)"><i class="ph ph-folder"></i> Groups <span class="nav-badge" id="subs-badge">0</span></div>
    <div class="nav-sec">Monitoring</div>
    <div class="nav-it" data-pg="traffic" onclick="showPg(this)"><i class="ph ph-chart-line-up"></i> Traffic</div>
    <div class="nav-it" data-pg="activity" onclick="showPg(this)"><i class="ph ph-notebook"></i> Activity</div>
    <div class="nav-it" data-pg="errors" onclick="showPg(this)"><i class="ph ph-warning"></i> Errors</div>
  </div>
  <div class="sb-foot">
    <button class="sb-btn" onclick="toggleTheme()"><i class="ph ph-moon"></i> Toggle Theme</button>
    <button class="sb-btn sb-logout" onclick="logout()"><i class="ph ph-sign-out"></i> Logout</button>
  </div>
</aside>

<main class="main">
<!-- OVERVIEW -->
<div class="pg on" id="pg-overview">
  <div class="topbar"><div><div class="tb-title"><i class="ph ph-squares-four"></i> Dashboard</div><div class="tb-sub">Cyber-Rage Gateway &bull; <span id="uptime">--:--:--</span></div></div></div>
  <div class="metrics">
    <div class="metric"><div class="m-icon"><i class="ph ph-gear-six"></i></div><div class="m-label">Active Connections</div><div class="m-val" id="m-conn">0</div></div>
    <div class="metric suc"><div class="m-icon suc"><i class="ph ph-chart-line-up"></i></div><div class="m-label">Total Traffic</div><div class="m-val" id="m-traffic">0 <span class="m-unit">MB</span></div></div>
    <div class="metric"><div class="m-icon pur"><i class="ph ph-link"></i></div><div class="m-label">Configs</div><div class="m-val" id="m-links">0</div><div class="m-sub"><span id="m-active" style="color:var(--green)">0</span> active &bull; <span id="m-expired" style="color:var(--red)">0</span> expired</div></div>
    <div class="metric dan"><div class="m-icon dan"><i class="ph ph-warning"></i></div><div class="m-label">Errors</div><div class="m-val" id="m-errors">0</div><div class="m-sub"><span id="m-reqs">0</span> requests</div></div>
  </div>
  <div class="vless-box" id="default-link-box">
    <div class="vl-header"><div class="vl-title"><i class="ph ph-link"></i> Default VLESS Link</div><span class="badge bg-green"><span class="dot dg pulse"></span> Active</span></div>
    <div class="vl-code" id="default-link-code">Loading...</div>
    <div class="vl-actions">
      <button class="btn btn-p" onclick="copyDefaultLink()"><i class="ph ph-copy"></i> Copy Link</button>
      <button class="btn btn-o" onclick="copySubUrl()"><i class="ph ph-link"></i> Copy Sub URL</button>
    </div>
  </div>
  <div class="g3">
    <div class="card"><div class="card-title"><i class="ph ph-chart-line-up"></i> Traffic (Last 24h)</div><div class="ch-lg"><canvas id="trafficChart"></canvas></div></div>
    <div class="card"><div class="card-title"><i class="ph ph-notebook"></i> Recent Activity</div><div id="recent-activity" style="max-height:340px;overflow-y:auto"></div></div>
  </div>
</div>

<!-- CONNECTIONS -->
<div class="pg" id="pg-connections">
  <div class="topbar"><div><div class="tb-title"><i class="ph ph-gear-six"></i> Live Connections</div><div class="tb-sub">Real-time active connections grouped by IP</div></div></div>
  <div class="card" id="conn-list"><div class="empty"><i class="ph ph-gear-six"></i>No active connections</div></div>
</div>

<!-- LINKS -->
<div class="pg" id="pg-links">
  <div class="topbar">
    <div><div class="tb-title"><i class="ph ph-link"></i> Config Management</div><div class="tb-sub">Create, edit, and manage VLESS configs</div></div>
    <button class="btn btn-p" onclick="showCreateLink()"><i class="ph ph-plus"></i> New Config</button>
  </div>
  <div id="links-list"></div>
</div>

<!-- SUBS -->
<div class="pg" id="pg-subs">
  <div class="topbar">
    <div><div class="tb-title"><i class="ph ph-folder"></i> Subscription Groups</div><div class="tb-sub">Group configs and generate public pages</div></div>
    <button class="btn btn-p" onclick="showCreateSub()"><i class="ph ph-plus"></i> New Group</button>
  </div>
  <div id="subs-list"></div>
</div>

<!-- TRAFFIC -->
<div class="pg" id="pg-traffic">
  <div class="topbar"><div><div class="tb-title"><i class="ph ph-chart-line-up"></i> Traffic Analysis</div><div class="tb-sub">Hourly traffic breakdown</div></div></div>
  <div class="card"><div class="ch-lg"><canvas id="trafficChartFull"></canvas></div></div>
</div>

<!-- ACTIVITY -->
<div class="pg" id="pg-activity">
  <div class="topbar"><div><div class="tb-title"><i class="ph ph-notebook"></i> Activity Log</div><div class="tb-sub">Recent system events and actions</div></div></div>
  <div class="card" id="activity-list"><div class="empty"><i class="ph ph-notebook"></i>No activity yet</div></div>
</div>

<!-- ERRORS -->
<div class="pg" id="pg-errors">
  <div class="topbar"><div><div class="tb-title"><i class="ph ph-warning"></i> Error Log</div><div class="tb-sub">Recent errors and warnings</div></div></div>
  <div class="card" id="errors-list"><div class="empty"><i class="ph ph-warning"></i>No errors</div></div>
</div>
</main>

<!-- MODALS -->
<div class="modal-bg" id="modal-create-link">
  <div class="modal">
    <h2><i class="ph ph-link"></i> New Config</h2>
    <div class="form-row">
      <div class="fg"><label>Label</label><input class="fi" id="cl-label" placeholder="My Config"></div>
      <div class="fg"><label>Protocol</label><select class="fs" id="cl-proto"><option value="vless-ws">VLESS + WebSocket</option><option value="xhttp-packet-up">XHTTP (packet-up)</option><option value="xhttp-stream-up">XHTTP (stream-up)</option></select></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>Fingerprint</label><select class="fs" id="cl-fp"><option value="chrome">Chrome</option><option value="firefox">Firefox</option><option value="safari">Safari</option><option value="ios">iOS</option><option value="android">Android</option><option value="edge">Edge</option><option value="random">Random</option><option value="randomized">Randomized</option></select></div>
      <div class="fg"><label>Port</label><input class="fi" id="cl-port" type="number" value="443" min="1" max="65535"></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>ALPN</label><input class="fi" id="cl-alpn" placeholder="http/1.1"></div>
      <div class="fg"><label>IP Limit (0=unlimited)</label><input class="fi" id="cl-ip" type="number" value="0" min="0"></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>Volume Limit</label><input class="fi" id="cl-vol" placeholder="e.g. 10GB (0=unlimited)"></div>
      <div class="fg"><label>Speed Limit (Mbps)</label><input class="fi" id="cl-spd" type="number" value="0" min="0"></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>Expiry (days, 0=never)</label><input class="fi" id="cl-exp" type="number" value="0" min="0"></div>
      <div class="fg"><label>Note</label><input class="fi" id="cl-note" placeholder="Optional note"></div>
    </div>
    <div class="form-row" style="margin-top:8px">
      <button class="btn btn-p" onclick="createLink()"><i class="ph ph-check"></i> Create Config</button>
      <button class="btn btn-o" onclick="closeModal('modal-create-link')"><i class="ph ph-x"></i> Cancel</button>
    </div>
  </div>
</div>

<div class="modal-bg" id="modal-edit-link">
  <div class="modal">
    <h2><i class="ph ph-pencil-simple"></i> Edit Config</h2>
    <input type="hidden" id="el-uid">
    <div class="form-row">
      <div class="fg"><label>Label</label><input class="fi" id="el-label"></div>
      <div class="fg"><label>Protocol</label><select class="fs" id="el-proto"><option value="vless-ws">VLESS + WebSocket</option><option value="xhttp-packet-up">XHTTP (packet-up)</option><option value="xhttp-stream-up">XHTTP (stream-up)</option></select></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>Fingerprint</label><select class="fs" id="el-fp"><option value="chrome">Chrome</option><option value="firefox">Firefox</option><option value="safari">Safari</option><option value="ios">iOS</option><option value="android">Android</option><option value="edge">Edge</option><option value="random">Random</option><option value="randomized">Randomized</option></select></div>
      <div class="fg"><label>Port</label><input class="fi" id="el-port" type="number" min="1" max="65535"></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>ALPN</label><input class="fi" id="el-alpn"></div>
      <div class="fg"><label>IP Limit</label><input class="fi" id="el-ip" type="number" min="0"></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>Volume Limit</label><input class="fi" id="el-vol"></div>
      <div class="fg"><label>Speed Limit (Mbps)</label><input class="fi" id="el-spd" type="number" min="0"></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>Expiry (days)</label><input class="fi" id="el-exp" type="number" min="0"></div>
      <div class="fg"><label>Note</label><input class="fi" id="el-note"></div>
    </div>
    <div class="form-row" style="margin-top:8px">
      <button class="btn btn-p" onclick="updateLink()"><i class="ph ph-check"></i> Save Changes</button>
      <button class="btn btn-o" onclick="closeModal('modal-edit-link')"><i class="ph ph-x"></i> Cancel</button>
    </div>
  </div>
</div>

<div class="modal-bg" id="modal-create-sub">
  <div class="modal">
    <h2><i class="ph ph-folder-plus"></i> New Subscription Group</h2>
    <div class="form-row">
      <div class="fg"><label>Group Name</label><input class="fi" id="cs-name" placeholder="My Group"></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>Description</label><input class="fi" id="cs-desc" placeholder="Optional description"></div>
    </div>
    <div class="form-row">
      <div class="fg"><label>Password (optional)</label><input class="fi" id="cs-pw" type="password" placeholder="Leave empty for no password"></div>
    </div>
    <div class="form-row" style="margin-top:8px">
      <button class="btn btn-p" onclick="createSub()"><i class="ph ph-check"></i> Create Group</button>
      <button class="btn btn-o" onclick="closeModal('modal-create-sub')"><i class="ph ph-x"></i> Cancel</button>
    </div>
  </div>
</div>

<script>
const $=s=>document.querySelector(s);
const $$=s=>document.querySelectorAll(s);
let linksData=[],subsData=[],trafficChart=null,trafficChartFull=null,defaultLink=null;
let isDark=true;

function toggleSidebar(){$('#sidebar').classList.toggle('open');$('#overlay').classList.toggle('show')}
function toggleTheme(){
  isDark=!isDark;
  if(isDark){document.documentElement.removeAttribute('data-theme')}
  else{document.documentElement.setAttribute('data-theme','light')}
  $$('.theme-mob i,.sb-btn i').forEach(i=>{i.className=isDark?'ph ph-moon':'ph ph-sun'});
}
function showPg(el){$$('.nav-it').forEach(n=>n.classList.remove('on'));el.classList.add('on');$$('.pg').forEach(p=>p.classList.remove('on'));$('#pg-'+el.dataset.pg).classList.add('on');if(el.dataset.pg==='traffic')loadTrafficFull()}
function closeModal(id){$('#'+id).classList.remove('show')}
function showToast(msg){const t=document.createElement('div');t.className='toast';t.textContent=msg;document.body.appendChild(t);setTimeout(()=>t.remove(),2500)}

async function api(url,opts={}){
  const r=await fetch(url,{headers:{'Content-Type':'application/json'},...opts});
  if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'Error');}
  return r.json();
}

async function loadStats(){
  try{
    const d=await api('/stats');
    $('#m-conn').textContent=d.active_connections;
    $('#m-traffic').innerHTML=d.total_traffic_mb+' <span class="m-unit">MB</span>';
    $('#m-links').textContent=d.links_count;
    $('#m-active').textContent=d.active_links;
    $('#m-expired').textContent=d.expired_links;
    $('#m-errors').textContent=d.total_errors;
    $('#m-reqs').textContent=d.total_requests;
    $('#uptime').textContent=d.uptime;
    $('#conn-badge').textContent=d.active_connections;
    $('#links-badge').textContent=d.links_count;
    updateTrafficChart(d.hourly);
  }catch(e){}
}

async function loadLinks(){
  try{
    const d=await api('/api/links');
    linksData=d.links;
    renderLinks();
    const dl=linksData.find(l=>l.is_default)||linksData[0];
    if(dl){
      defaultLink=dl;
      $('#default-link-code').textContent=dl.vless_link;
    }
  }catch(e){}
}

async function loadSubs(){
  try{
    const d=await api('/api/subs');
    subsData=d.subs;
    renderSubs();
    $('#subs-badge').textContent=subsData.length;
  }catch(e){}
}

async function loadConnections(){
  try{
    const d=await api('/api/connections');
    const el=$('#conn-list');
    if(!d.connections.length){el.innerHTML='<div class="empty"><i class="ph ph-gear-six"></i>No active connections</div>';return;}
    let h=d.connections.map(c=>`<div class="conn-row"><span class="conn-ip">${c.ip}</span><span class="conn-label">${c.label}</span><span class="conn-bytes">${c.bytes_fmt}</span><span class="conn-sessions">${c.sessions} sess</span></div>`).join('');
    el.innerHTML=h;
  }catch(e){}
}

async function loadActivity(){
  try{
    const d=await api('/api/activity');
    const el=$('#activity-list');
    if(!d.logs.length){el.innerHTML='<div class="empty"><i class="ph ph-notebook"></i>No activity yet</div>';return;}
    let h=d.logs.reverse().map(l=>{
      const cls=l.level==='err'?'log-err':l.level==='warn'?'log-warn':'log-ok';
      const t=l.time?l.time.split('T')[1]?.split('.')[0]||'':'';
      return `<div class="log-entry ${cls}"><span class="log-time">${t}</span><span class="log-msg">${l.message}</span></div>`;
    }).join('');
    el.innerHTML=h;
  }catch(e){}
}

function renderLinks(){
  const el=$('#links-list');
  if(!linksData.length){el.innerHTML='<div class="empty"><i class="ph ph-link"></i>No configs yet. Create one!</div>';return;}
  el.innerHTML=linksData.map(l=>{
    const status=l.active&&!l.expired?'<span class="dot dg pulse"></span>':'<span class="dot dr"></span>';
    const badge=l.expired?'<span class="exp-chip ec-exp">Expired</span>':!l.active?'<span class="exp-chip ec-warn">Disabled</span>':'<span class="exp-chip ec-ok">Active</span>';
    const limit=l.limit_bytes===0?'Unlimited':l.limit_bytes>=1073741824?(l.limit_bytes/1073741824).toFixed(1)+' GB':(l.limit_bytes/1048576).toFixed(0)+' MB';
    const used=l.used_bytes||0;
    const total=l.limit_bytes||0;
    const pct=total>0?Math.min(100,(used/total)*100):0;
    const bar=total>0?`<div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div><div class="progress-text">${l.used_fmt||'0 B'} / ${limit} (${pct.toFixed(1)}%)</div>`:`<div class="progress-text">${l.used_fmt||'0 B'} / Unlimited</div>`;
    const ex=l.expiry;
    let expBlock='';
    if(ex){
      const passed=Math.min(ex.total_days,Math.floor(ex.elapsed_days));
      const remTxt=ex.remaining_days>0?`${Math.ceil(ex.remaining_days)}d left`:`expired ${Math.ceil(Math.abs(ex.remaining_days))}d ago`;
      const fillCss=l.expired?'background:var(--red)':ex.percent>=90?'background:var(--amber)':'';
      expBlock=`<div class="progress-bar"><div class="progress-fill" style="width:${ex.percent}%;${fillCss}"></div></div><div class="progress-text"><i class="ph ph-calendar-check"></i> ${passed}/${ex.total_days} days (${ex.percent.toFixed(1)}%) &bull; ${remTxt}</div>`;
    }
    return `<div class="list-item">
      <div class="list-icon">${status}</div>
      <div class="list-info">
        <div class="list-name">${l.label} ${badge}</div>
        <div class="list-sub">${l.protocol} &bull; ${l.fingerprint} &bull; Port ${l.port} &bull; ${l.connected_ips||0} IPs</div>
        ${bar}
        ${expBlock}
      </div>
      <div class="list-actions">
        <button class="btn btn-sm btn-g" onclick="copyText('${l.vless_link.replace(/'/g,"\\'")}')" title="Copy Link"><i class="ph ph-copy"></i></button>
        <button class="btn btn-sm btn-o" onclick="editLink('${l.uuid}')" title="Edit"><i class="ph ph-pencil-simple"></i></button>
        <button class="btn btn-sm ${l.active?'btn-o':'btn-g'}" onclick="toggleLink('${l.uuid}',${!l.active})" title="${l.active?'Disable':'Enable'}"><i class="ph ${l.active?'ph-pause':'ph-play'}"></i></button>
        <button class="btn btn-sm btn-d" onclick="deleteLink('${l.uuid}')" title="Delete"><i class="ph ph-trash"></i></button>
      </div>
    </div>`;
  }).join('');
}

function renderSubs(){
  const el=$('#subs-list');
  if(!subsData.length){el.innerHTML='<div class="empty"><i class="ph ph-folder"></i>No groups yet. Create one!</div>';return;}
  el.innerHTML=subsData.map(s=>{
    return `<div class="list-item">
      <div class="list-icon"><i class="ph ph-folder"></i></div>
      <div class="list-info">
        <div class="list-name">${s.name} ${s.has_password?'<i class="ph ph-lock" style="color:var(--amber);font-size:12px"></i>':''}</div>
        <div class="list-sub">${s.links_count} configs &bull; ${s.total_used_fmt} used &bull; <a href="${s.public_url}" target="_blank" style="color:var(--accent)">Public Page</a></div>
      </div>
      <div class="list-actions">
        <button class="btn btn-sm btn-g" onclick="copyText('${s.sub_url.replace(/'/g,"\\'")}')" title="Copy Sub URL"><i class="ph ph-copy"></i></button>
        <button class="btn btn-sm btn-d" onclick="deleteSub('${s.sub_id}')" title="Delete"><i class="ph ph-trash"></i></button>
      </div>
    </div>`;
  }).join('');
}

function updateTrafficChart(hourly){
  const labels=Array.from({length:24},(_,i)=>String(i).padStart(2,'0')+':00');
  const data=labels.map((_,i)=>hourly[String(i).padStart(2,'0')+':00']||0);
  const ctx=$('#trafficChart');
  if(trafficChart){trafficChart.data.datasets[0].data=data.map(v=>v/1024/1024);trafficChart.update();return;}
  trafficChart=new Chart(ctx,{type:'line',data:{labels,datasets:[{label:'Traffic (MB)',data:data.map(v=>v/1024/1024),borderColor:'#00f0ff',backgroundColor:'rgba(0,240,255,0.08)',fill:true,tension:.4,pointRadius:2,pointBackgroundColor:'#00f0ff',borderWidth:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{color:'rgba(0,240,255,0.04)'},ticks:{color:'#556688',font:{size:10,family:'Space Grotesk'}}},y:{grid:{color:'rgba(0,240,255,0.04)'},ticks:{color:'#556688',font:{size:10,family:'Space Grotesk'},callback:v=>v.toFixed(1)}}}}});
}

async function loadTrafficFull(){
  try{
    const d=await api('/stats');
    const labels=Array.from({length:24},(_,i)=>String(i).padStart(2,'0')+':00');
    const data=labels.map((_,i)=>(d.hourly[String(i).padStart(2,'0')+':00']||0)/1024/1024);
    const ctx=$('#trafficChartFull');
    if(trafficChartFull){trafficChartFull.data.datasets[0].data=data;trafficChartFull.update();return;}
    trafficChartFull=new Chart(ctx,{type:'bar',data:{labels,datasets:[{label:'Traffic (MB)',data,backgroundColor:'rgba(0,240,255,0.3)',borderColor:'#00f0ff',borderWidth:1,borderRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{color:'rgba(0,240,255,0.04)'},ticks:{color:'#556688',font:{size:10,family:'Space Grotesk'}}},y:{grid:{color:'rgba(0,240,255,0.04)'},ticks:{color:'#556688',font:{size:10,family:'Space Grotesk'},callback:v=>v.toFixed(1)}}}}});
  }catch(e){}
}

function copyText(t){navigator.clipboard.writeText(t).then(()=>showToast('Copied!'))}
function copyDefaultLink(){if(defaultLink)copyText(defaultLink.vless_link)}
function copySubUrl(){if(defaultLink)copyText(defaultLink.sub_url)}

function showCreateLink(){$('#modal-create-link').classList.add('show')}
function showCreateSub(){$('#modal-create-sub').classList.add('show')}

async function createLink(){
  const vol=$('#cl-vol').value.trim();
  let lv=0,lu='GB';
  if(vol){const m=vol.match(/^([\d.]+)\s*(GB|MB|KB)?$/i);if(m){lv=parseFloat(m[1]);lu=(m[2]||'GB').toUpperCase();}}
  await api('/api/links',{method:'POST',body:JSON.stringify({
    label:$('#cl-label').value||'New Config',protocol:$('#cl-proto').value,fingerprint:$('#cl-fp').value,
    port:parseInt($('#cl-port').value)||443,alpn:$('#cl-alpn').value,
    limit_value:lv,limit_unit:lu,speed_limit_value:parseFloat($('#cl-spd').value)||0,
    ip_limit:parseInt($('#cl-ip').value)||0,expires_days:parseInt($('#cl-exp').value)||0,
    note:$('#cl-note').value
  })});
  closeModal('modal-create-link');showToast('Config created!');loadLinks();loadStats();
}

function editLink(uid){
  const l=linksData.find(x=>x.uuid===uid);if(!l)return;
  $('#el-uid').value=uid;$('#el-label').value=l.label;$('#el-proto').value=l.protocol;
  $('#el-fp').value=l.fingerprint;$('#el-port').value=l.port;$('#el-alpn').value=l.alpn||'';
  $('#el-ip').value=l.ip_limit||0;$('#el-note').value=l.note||'';
  $('#el-spd').value=l.speed_limit_bytes?Math.round(l.speed_limit_bytes*8/1024/1024):0;
  $('#el-vol').value=l.limit_bytes?fmtBytesShort(l.limit_bytes):'';
  $('#el-exp').value=l.expires_at?Math.max(0,Math.ceil((new Date(l.expires_at)-new Date())/(86400000))):0;
  $('#modal-edit-link').classList.add('show');
}
function fmtBytesShort(b){if(b>=1073741824)return(b/1073741824).toFixed(1)+'GB';return(b/1048576).toFixed(0)+'MB';}

async function updateLink(){
  const uid=$('#el-uid').value;
  const vol=$('#el-vol').value.trim();
  let lv=0,lu='GB';
  if(vol){const m=vol.match(/^([\d.]+)\s*(GB|MB|KB)?$/i);if(m){lv=parseFloat(m[1]);lu=(m[2]||'GB').toUpperCase();}}
  await api('/api/links/'+uid,{method:'PATCH',body:JSON.stringify({
    label:$('#el-label').value,protocol:$('#el-proto').value,fingerprint:$('#el-fp').value,
    port:parseInt($('#el-port').value)||443,alpn:$('#el-alpn').value,
    limit_value:lv,limit_unit:lu,speed_limit_value:parseFloat($('#el-spd').value)||0,
    ip_limit:parseInt($('#el-ip').value)||0,expires_days:parseInt($('#el-exp').value)||0,
    note:$('#el-note').value
  })});
  closeModal('modal-edit-link');showToast('Config updated!');loadLinks();
}

async function toggleLink(uid,active){
  await api('/api/links/'+uid,{method:'PATCH',body:JSON.stringify({active})});
  showToast(active?'Config enabled':'Config disabled');loadLinks();
}

async function deleteLink(uid){
  if(!confirm('Delete this config? This cannot be undone.'))return;
  await api('/api/links/'+uid,{method:'DELETE'});
  showToast('Config deleted');loadLinks();loadStats();
}

async function createSub(){
  await api('/api/subs',{method:'POST',body:JSON.stringify({
    name:$('#cs-name').value||'New Group',desc:$('#cs-desc').value,password:$('#cs-pw').value
  })});
  closeModal('modal-create-sub');showToast('Group created!');loadSubs();
}

async function deleteSub(sid){
  if(!confirm('Delete this group?'))return;
  await api('/api/subs/'+sid,{method:'DELETE'});
  showToast('Group deleted');loadSubs();
}

async function logout(){
  await api('/api/logout',{method:'POST'});
  location.href='/login';
}

// Auto-refresh
loadStats();loadLinks();loadSubs();loadActivity();loadConnections();
setInterval(()=>{loadStats();loadConnections();loadActivity();},5000);
setInterval(()=>{loadLinks();loadSubs();},15000);
</script>
</body></html>"""
