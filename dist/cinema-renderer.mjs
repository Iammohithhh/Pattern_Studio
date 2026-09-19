import * as THREE from './vendor/three.module.js';
import {OrbitControls} from './vendor/OrbitControls.js';
// A single retained WebGL scene. State updates move existing meshes instead of
// replacing the stage, preserving spatial continuity between algorithm steps.
export class ClassroomRenderer {
 constructor(host){
  this.host=host;this.items=new Map();this.edges=[];this.disposed=false;this.reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  this.renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,powerPreference:'low-power'});
  this.renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));this.renderer.setClearColor(0x101a2c);this.renderer.shadowMap.enabled=true;this.renderer.shadowMap.type=THREE.PCFSoftShadowMap;this.renderer.outputColorSpace=THREE.SRGBColorSpace;
  host.append(this.renderer.domElement);this.renderer.domElement.setAttribute('aria-label','Interactive 3D algorithm scene. Drag to orbit. Use the camera buttons to change view.');this.renderer.domElement.setAttribute('role','img');
  this.scene=new THREE.Scene();this.scene.background=new THREE.Color('#101a2c');this.scene.fog=new THREE.Fog('#101a2c',24,65);
  this.camera=new THREE.PerspectiveCamera(38,1,.1,100);this.camera.position.set(10,14,19);
  this.controls=new OrbitControls(this.camera,this.renderer.domElement);this.controls.target.set(0,.4,0);this.controls.enableDamping=!this.reduced;this.controls.enablePan=false;this.controls.minDistance=8;this.controls.maxDistance=38;this.controls.maxPolarAngle=Math.PI*.47;this.controls.autoRotate=false;
  this.scene.add(new THREE.HemisphereLight(0xd8ebff,0x2b3751,2.3));const key=new THREE.DirectionalLight(0xffffff,3);key.position.set(5,12,7);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.camera.left=-16;key.shadow.camera.right=16;key.shadow.camera.top=16;key.shadow.camera.bottom=-16;key.shadow.normalBias=.05;this.scene.add(key);const rim=new THREE.DirectionalLight(0x8ba5ff,2);rim.position.set(-8,5,-5);this.scene.add(rim);
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(100,100),new THREE.MeshStandardMaterial({color:0x142137,roughness:.85}));floor.rotation.x=-Math.PI/2;floor.position.y=-.16;floor.receiveShadow=true;this.scene.add(floor);
  const grid=new THREE.GridHelper(40,40,0x354564,0x223249);grid.position.y=-.14;grid.material.transparent=true;grid.material.opacity=.6;this.scene.add(grid);
  this.observer=new ResizeObserver(()=>this.resize());this.observer.observe(host);this.resize();this.animate=this.animate.bind(this);this.raf=requestAnimationFrame(this.animate);
 }
 resize(){if(this.disposed)return;const w=this.host.clientWidth,h=this.host.clientHeight;this.renderer.setSize(w,h,false);this.viewWidth=w>700?w*.69:w;this.camera.aspect=this.viewWidth/Math.max(1,h);this.camera.updateProjectionMatrix();}
 label(text,color='#ecf3ff'){
  const canvas=document.createElement('canvas');canvas.width=512;canvas.height=128;const c=canvas.getContext('2d');c.clearRect(0,0,512,128);c.textAlign='center';c.textBaseline='middle';c.fillStyle=color;c.font='600 38px system-ui';let lines=String(text).split('\n');lines.forEach((s,i)=>c.fillText(s.length>25?s.slice(0,23)+'…':s,256,lines.length===1?64:38+i*50,490));
  const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;const mat=new THREE.SpriteMaterial({map:texture,depthTest:false,transparent:true});const sprite=new THREE.Sprite(mat);sprite.scale.set(2.3,.58,1);sprite.renderOrder=10;return sprite;
 }
 clearObject(group){group.traverse(obj=>{obj.geometry?.dispose();const materials=Array.isArray(obj.material)?obj.material:[obj.material];materials.filter(Boolean).forEach(m=>{m.map?.dispose();m.dispose();});});}
 setFrame(frame){
  if(this.disposed)return;const ids=new Set(frame.objects.map(o=>o.id));for(const [id,item]of this.items)if(!ids.has(id)){this.scene.remove(item.group);this.clearObject(item.group);this.items.delete(id);}
  for(const o of frame.objects){let item=this.items.get(o.id);if(!item){
   const group=new THREE.Group(),size=o.size||{x:1,y:.65,z:.85};const geom=o.type==='sphere'?new THREE.SphereGeometry(.46,24,16):new THREE.BoxGeometry(size.x,size.y,size.z);const mat=new THREE.MeshStandardMaterial({color:o.color,roughness:.32,metalness:.12,transparent:o.type==='water',opacity:o.type==='water'?.4:1});const mesh=new THREE.Mesh(geom,mat);mesh.castShadow=true;mesh.receiveShadow=true;group.add(mesh);group.position.set(o.x,this.reduced?o.y:o.y-.4,o.z);group.scale.setScalar(this.reduced?1:.82);this.scene.add(group);item={group,mesh,target:new THREE.Vector3(),size,type:o.type};this.items.set(o.id,item);
   }item.target.set(o.x,o.y,o.z);item.mesh.material.color.set(o.color);item.mesh.material.emissive.set(o.role==='current'?o.color:'#000000');item.mesh.material.emissiveIntensity=o.role==='current'?.13:0;
   const nextSize=o.size||{x:1,y:.65,z:.85};item.mesh.scale.set(nextSize.x/item.size.x,nextSize.y/item.size.y,nextSize.z/item.size.z);
   const text=o.value+'\n'+o.label;if(item.text!==text){if(item.sprite){item.group.remove(item.sprite);this.clearObject(item.sprite);}item.sprite=this.label(text,o.role==='current'?'#f0ffc8':'#e6edf9');item.group.add(item.sprite);item.text=text;}item.sprite.position.y=nextSize.y/2+.53;
   if(this.reduced){item.group.position.copy(item.target);item.group.scale.setScalar(1);}
  }
  this.edges.forEach(e=>{this.scene.remove(e);this.clearObject(e);});this.edges=[];
  for(const e of frame.links){const a=this.items.get(e.from),b=this.items.get(e.to);if(!a||!b)continue;const vec=new THREE.Vector3().subVectors(b.target,a.target),length=vec.length();if(length<.01)continue;const arrow=new THREE.ArrowHelper(vec.clone().normalize(),a.target.clone(),Math.max(.1,length-.45),0xb1a2ee,.19,.13);this.scene.add(arrow);this.edges.push(arrow);}
  if(!this.initialized){const distance=Math.max(12,frame.extent*1.25);this.camera.position.set(distance*.22,distance*.65,distance);this.controls.target.set(0,.4,0);this.controls.update();this.controls.saveState();this.initialized=true;}
 }
 view(kind){if(kind==='reset'){this.controls.reset();return;}const distance=this.camera.position.distanceTo(this.controls.target);if(kind==='top')this.camera.position.set(.001,distance,.001);if(kind==='front')this.camera.position.set(0,distance*.25,distance);if(kind==='angle')this.camera.position.set(distance*.4,distance*.6,distance*.8);this.controls.update();}
 animate(){if(this.disposed)return;if(!this.host.isConnected){this.dispose();return;}if(!document.hidden){for(const item of this.items.values()){item.group.position.lerp(item.target,this.reduced?1:.15);item.group.scale.lerp(new THREE.Vector3(1,1,1),.15);}this.controls.update();this.renderer.setViewport(0,0,this.host.clientWidth,this.host.clientHeight);this.renderer.clear();this.renderer.setViewport(0,0,this.viewWidth,this.host.clientHeight);this.renderer.render(this.scene,this.camera);}this.raf=requestAnimationFrame(this.animate);}
 dispose(){if(this.disposed)return;this.disposed=true;cancelAnimationFrame(this.raf);this.observer.disconnect();this.controls.dispose();this.clearObject(this.scene);this.scene.clear();this.items.clear();this.renderer.dispose();this.renderer.forceContextLoss();this.renderer.domElement.remove();}
}
