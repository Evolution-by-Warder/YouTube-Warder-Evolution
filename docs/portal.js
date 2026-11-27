(()=>{"use strict";
const root=document.documentElement;
const supported=["sk","en","de","ru"];
const buttons=[...document.querySelectorAll("[data-lang]")];
function language(value){
  const lang=supported.includes(value)?value:"sk";
  root.lang=lang;root.dataset.language=lang;
  document.querySelectorAll("span[lang]:is(.sk,.en,.de,.ru)").forEach(el=>{el.hidden=el.getAttribute("lang")!==lang;});
  buttons.forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.lang===lang)));
  for(const [key,attr] of [["aria","aria-label"],["alt","alt"],["content","content"]]){
    document.querySelectorAll("[data-"+key+"-"+lang+"]").forEach(el=>el.setAttribute(attr,el.getAttribute("data-"+key+"-"+lang)));
  }
  document.querySelectorAll("[data-text-"+lang+"]").forEach(el=>el.textContent=el.getAttribute("data-text-"+lang));
  try{localStorage.setItem("warder-language",lang)}catch(e){}
}
let initial="sk";try{initial=localStorage.getItem("warder-language")||"sk"}catch(e){}
language(initial);
buttons.forEach(b=>b.addEventListener("click",()=>language(b.dataset.lang)));
})();

(()=>{"use strict";if(typeof HTMLDialogElement==="undefined")return;document.querySelectorAll(".screenshot-grid").forEach(grid=>{const links=[...grid.querySelectorAll("a[data-caption-en][data-caption-sk]")];if(!links.length)return;links.forEach((link,start)=>link.addEventListener("click",ev=>{if(ev.button!==0||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey)return;ev.preventDefault();const lang=document.documentElement.lang;const labels=({sk:["Galéria snímok","Predchádzajúca snímka","Nasledujúca snímka","Zavrieť"],en:["Screenshot gallery","Previous screenshot","Next screenshot","Close"],de:["Screenshot-Galerie","Vorheriges Bild","Nächstes Bild","Schließen"],ru:["Галерея снимков","Предыдущий снимок","Следующий снимок","Закрыть"]})[lang]||["Galéria snímok","Predchádzajúca snímka","Nasledujúca snímka","Zavrieť"];let index=start;const d=document.createElement("dialog");d.className="screenshot-dialog";d.setAttribute("aria-label",labels[0]);const bar=document.createElement("div");bar.className="screenshot-controls";const make=(label,content)=>{const b=document.createElement("button");b.type="button";b.textContent=content;b.setAttribute("aria-label",label);return b};const prev=make(labels[1],"←"),next=make(labels[2],"→"),close=make(labels[3],"×");const caption=document.createElement("span");caption.className="screenshot-caption";caption.setAttribute("aria-live","polite");const img=document.createElement("img");bar.append(prev,caption,next,close);d.append(bar,img);document.body.append(d);function show(){const item=links[index];img.src=item.getAttribute("href");img.alt=item.getAttribute("data-caption-"+lang)||item.dataset.captionSk;caption.textContent=(index+1)+" / "+links.length+" — "+img.alt;prev.disabled=index===0;next.disabled=index===links.length-1}function go(delta){index=Math.min(links.length-1,Math.max(0,index+delta));show()}prev.addEventListener("click",()=>go(-1));next.addEventListener("click",()=>go(1));close.addEventListener("click",()=>d.close());d.addEventListener("keydown",e=>{if(e.key==="ArrowLeft"||e.key==="ArrowRight"){e.preventDefault();go(e.key==="ArrowLeft"?-1:1)}});d.addEventListener("close",()=>{d.remove();link.focus()});show();d.showModal();close.focus()}))})})();
