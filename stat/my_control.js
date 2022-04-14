var lastX = null;
var lastY = null;  
var dwn   = false; 

const wheelEvent = isEventSupported('mousewheel') ? 'mousewheel' : 'wheel';
window.addEventListener(wheelEvent,  wheel);
window.addEventListener('mousemove', quaternion);
window.addEventListener('mousemove', moveCamera); 
window.addEventListener('mousemove', updateXY);    
window.addEventListener('mouseup',   mouseup); 
window.addEventListener('mousedown', mousedown);

  
// FANCTIONS

  
function isEventSupported(eventName) {
    var el = document.createElement('div');
    eventName = 'on' + eventName;
    var isSupported = (eventName in el);
    if (!isSupported) {
        el.setAttribute(eventName, 'return;');
        isSupported = typeof el[eventName] == 'function';
    }
    el = null;
    return isSupported;
}  
  
  
  
function wheel(e) {
  camera.position.z += 0.1 * e.wheelDelta;
  camera.position.y += e.wheelDelta*camera.quaternion.x*10;
  camera.position.x += e.wheelDelta*camera.quaternion.y*10;
} 
  
function quaternion(e) {
  	if (null == lastX) return;

	const speed = dwn ? 0.0005 : 0.0005;
  
	const k = window.innerWidth / window.innerHeight;
	
	const deltaY = lastX - e.clientX;
	const deltaX = lastY - e.clientY;

	camera.quaternion.y += deltaY*speed*k;
	camera.quaternion.x += deltaX*speed*k;
    
}
  
function updateXY(e){
	lastX = e.clientX;
    lastY = e.clientY;
}  
  
function moveCamera(e){
  	if (!dwn) return;
  
    const speed = 2;
	const k = window.innerWidth / window.innerHeight;
	
	const deltaX = lastX - e.clientX;
	const deltaY = lastY - e.clientY;
  
    camera.position.x += deltaX*speed*k;
    camera.position.y -= deltaY*speed*k;;
    camera.position.z += 0.1;
}    
  
function mousedown(e){ dwn = true;  }
function mouseup(e)  { dwn = false; }  