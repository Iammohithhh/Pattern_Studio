const fs=require('fs'),vm=require('vm'),assert=require('assert');
const el={innerHTML:'',textContent:'',value:'',addEventListener(){},classList:{add(){},remove(){},toggle(){}}};
const context={console,localStorage:{getItem(){return null},setItem(){}},location:{hash:''},document:{querySelector(){return el},querySelectorAll(){return []},activeElement:{tagName:'BODY'}},history:{},setTimeout(){},clearTimeout(){},setInterval(){},clearInterval(){},navigator:{}};
context.window=context;context.addEventListener=()=>{};context.scrollTo=()=>{};vm.createContext(context);
for(const name of ['curriculum','neetcode','topics','app','studio'])vm.runInContext(fs.readFileSync(`dist/${name}.js`,'utf8'),context,{filename:name+'.js'});
vm.runInContext(`
let rendered=0, snapshots=0;
for(const p of data){
 currentTrack=p.track;approach=p.recommended??1;
 for(const section of ['learn','code','patterns','notes','visual']){lessonTab=section;step=0;const html=lesson(p);if(!html.includes(p.title.replace(/&/g,'&amp;')))throw Error('Missing title '+p.id);rendered++;}
 for(let i=0;i<p.trace.length;i++){step=i;visual(p);snapshots++;}
}
for(const name of Object.keys(TOPICS)){topicPage(name);}
console.log(JSON.stringify({lessons:data.length,rendered,snapshots,guides:Object.keys(TOPICS).length,truncated:NEETCODE.filter(p=>p.trace.length>=10000 || p.trace.at(-1).event!=='return').map(p=>p.title)}));
`,context);
