const PASSWORD = "1234";
const assets = ["EUR/USD", "GBP/USD", "USD/JPY", "EUR/GBP", "AUD/USD", "AUD/NZD (OTC)", "EUR/CAD (OTC)", "GBP/USD (OTC)", "VISA (OTC)", "APPLE (OTC)", "AMAZON (OTC)", "TOYOTA (OTC)", "BIN IDX", "IMX", "PMX", "ASIA"];
let selectedAsset = assets[0];
const $ = (id)=>document.getElementById(id);
function show(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));$(id).classList.add('active')}
function renderAssets(){ $('assetsList').innerHTML=''; assets.forEach(a=>{ const d=document.createElement('button'); d.className='asset'; d.innerHTML=`<span>${a}</span><b>OPEN</b>`; d.onclick=()=>startAnalyze(a); $('assetsList').appendChild(d); }); }
function startAnalyze(asset){ selectedAsset=asset; $('loadingAsset').textContent=asset; show('loadingScreen'); setTimeout(showResult, 2600); }
function showResult(){ const isBuy=Math.random()>.5; const power=Math.floor(76+Math.random()*18); $('signalText').textContent=isBuy?'BUY':'SELL'; $('arrow').textContent=isBuy?'↑':'↓'; $('arrow').className='arrow '+(isBuy?'up':'down'); $('resultAsset').textContent=selectedAsset; $('strength').textContent=power+'%'; show('resultScreen'); }
$('loginBtn').onclick=()=>{ if($('passwordInput').value===PASSWORD){$('loginError').textContent=''; renderAssets(); show('assetsScreen')} else {$('loginError').textContent='Неверный пароль';} };
$('passwordInput').addEventListener('keydown',e=>{if(e.key==='Enter')$('loginBtn').click()});
$('repeatBtn').onclick=()=>startAnalyze(selectedAsset);
$('backBtn').onclick=()=>show('assetsScreen');
$('logoutBtn').onclick=()=>show('loginScreen');
if(window.Telegram && Telegram.WebApp){Telegram.WebApp.ready();Telegram.WebApp.expand();}
