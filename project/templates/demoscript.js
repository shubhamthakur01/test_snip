
var canvasfull='No'
var canvasdraw='No';
function getsnap(){
canvasdraw='yes';
element=document.getElementById('videoElement');
resize_canvas(element);
}
function resize_canvas(element)
{
  cv1.width = element.offsetWidth;
  cv1.height = element.offsetHeight;
  cv1.top = element.offsetTop;
  cv1.left = element.offsetLeft;
}
let last_mousex = last_mousey = 0;
let mousex = mousey = 0;
let mousedown = false;
let rect = {};
const ctx = cv1.getContext("2d");

cv1.addEventListener("mouseup", function (e) {
  if(canvasdraw=='yes'){
  mousedown = false;
   VideoToCroppedImage(rect);
   if(canvasfull=='yes'){
   document.getElementById('qwerty').click()
   canvasfull=='no';
  }

    }
    else{}
}, false);

cv1.addEventListener("mousedown", function (e) {

if(canvasdraw=='yes'){
  var vid = document.getElementById("videoElement");
  vid.pause();
  last_mousex = parseInt(e.clientX-cv1.offsetLeft);
  last_mousey = parseInt(e.clientY-cv1.offsetTop);

  mousedown = true;
  }
}, false);

cv1.addEventListener("mousemove", function (e) {
if(canvasdraw=='yes'){

  if(mousedown) {

  mousex = parseInt(e.clientX-cv1.offsetLeft);
  mousey = parseInt(e.clientY-cv1.offsetTop);
      ctx.clearRect(0,0,cv1.width,cv1.height); //clear canvas
      ctx.beginPath();
      var width = mousex-last_mousex;
      var height = mousey-last_mousey;
      ctx.rect(last_mousex,last_mousey,width,height);
      rect = {x: last_mousex, y: last_mousey, width, height};
      ctx.strokeStyle = 'red';
      ctx.lineWidth = 2;
      ctx.stroke();
  }}
}, false);
// snip.addEventListener("click", function(e) {

// })
function VideoToCroppedImage({width, height, x, y}) {
  const aspectRatioY = videoElement.videoHeight / cv1.height;
  const aspectRatioX = videoElement.videoWidth / cv1.width;

  const cv2 = document.getElementById('cv2');
  const ctx2 = cv2.getContext('2d');
  ctx2.fillStyle = "black";
  ctx2.fillRect(0, 0, cv2.width, cv2.height);
  ctx2.drawImage(videoElement, x*aspectRatioX, y*aspectRatioY, width*aspectRatioX, height*aspectRatioY, 0, 0, cv2.width, cv2.height);
  cv2.setAttribute('crossOrigin','anonymous');
    canvasfull='yes'
    canvasdraw='no'
    reset_canvas();
}

function reset_canvas()
{
  cv1.width = 1;
  cv1.height = 1;
  cv1.top = 1;
  cv1.left = 1;
}

document.getElementById('source_one').addEventListener('click', function() {
  document.getElementById('videoElement').src = '/static/STEVE_HARVEY.mp4';
});

document.getElementById('source_two').addEventListener('click', function() {
  document.getElementById('videoElement').src = '/static/Interview.mp4';
});

document.getElementById('source_three').addEventListener('click', function() {
  document.getElementById('videoElement').src = '/static/Ettiquetes.mp4';
});