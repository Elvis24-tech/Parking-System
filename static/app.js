function updateClock(){const el=document.getElementById('clock');if(el){el.textContent=new Date().toLocaleString('en-KE',{dateStyle:'medium',timeStyle:'medium'});}}updateClock();setInterval(updateClock,1000);
setTimeout(()=>document.querySelectorAll('.alert').forEach(a=>a.style.display='none'),6000);
