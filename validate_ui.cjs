const fs=require('fs'),vm=require('vm'),assert=require('assert');
const el={innerHTML:'',textContent:'',value:'',addEventListener(){},classList:{add(){},remove(){},toggle(){}}};
const context={console,localStorage:{getItem(){return null},setItem(){}},location:{hash:''},document:{querySelector(){return el},querySelectorAll(){return []},activeElement:{tagName:'BODY'}},history:{},setTimeout(){},clearTimeout(){},setInterval(){},clearInterval(){},navigator:{}};
context.window=context;context.addEventListener=()=>{};context.scrollTo=()=>{};vm.createContext(context);
for(const name of ['curriculum','neetcode','topics','app','stories','studio'])vm.runInContext(fs.readFileSync(`dist/${name}.js`,'utf8'),context,{filename:name+'.js'});
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
// Authored stories must agree with independently verified lesson results.
vm.runInContext(`
let storyCount=0,sceneCount=0;
for(const p of data){const story=getStory(p);if(!story)continue;storyCount++;
 const expected=p.track==='neetcode'?p.traceResult:p.trace.at(-1).value;
 if(JSON.stringify(story.result)!==JSON.stringify(expected))throw Error('Story result mismatch: '+p.title+' '+JSON.stringify(story.result)+' != '+JSON.stringify(expected));
 for(let i=0;i<story.scenes.length;i++){storyIndex=i;storyLesson=p.id;const markup=storyPanel(p,true);if(!markup.includes('WHY IT STAYS CORRECT'))throw Error('Missing teaching explanation');sceneCount++;}
}
console.log(JSON.stringify({verifiedStories:storyCount,verifiedScenes:sceneCount}));
`,context);
