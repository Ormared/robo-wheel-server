const { ipcRenderer } = require('electron');

let moveInterval;
const moveDelay = 100; // Send move command every 100ms

// Update speed display when the slider is moved
const velocitySlider = document.getElementById('velocity');
const speedDisplay = document.getElementById('speed-display');

velocitySlider.addEventListener('input', function() {
  speedDisplay.textContent = `${this.value} m/s`; // Update with "m/s"
});

function startMoving(dx, dy) {
  const velocity = velocitySlider.value;

  moveInterval = setInterval(() => {
    const data = {
      dx: dx,
      dy: dy,
      velocity: parseFloat(velocity)
    };
    ipcRenderer.send('send-data', data);
  }, moveDelay);
}

// Stop sending direction and velocity data
function stopMoving() {
  clearInterval(moveInterval);
}

// Set up event listeners for press-and-hold behavior
function setupButtonListeners(buttonId, dx, dy) {
  const button = document.getElementById(buttonId);
  button.addEventListener('mousedown', () => startMoving(dx, dy));
  button.addEventListener('mouseup', stopMoving);
  button.addEventListener('mouseleave', stopMoving);
  button.addEventListener('touchstart', () => startMoving(dx, dy)); // For mobile touch
  button.addEventListener('touchend', stopMoving);                  // For mobile touch
}

// Initialize directional buttons with the specified direction vectors
setupButtonListeners('btn-up-left', -1, 1);   // ↖
setupButtonListeners('btn-up', 0, 1);           // ↑
setupButtonListeners('btn-up-right', 1, 1);     // ↗
setupButtonListeners('btn-left', -1, 0);        // ←
setupButtonListeners('btn-right', 1, 0);        // →
setupButtonListeners('btn-down-left', -1, -1);  // ↙
setupButtonListeners('btn-down', 0, -1);        // ↓
setupButtonListeners('btn-down-right', 1, -1);  // ↘

const camera_img = document.getElementById('camera_img');
ipcRenderer.on('camera-feed', (event, data) => {
  const img = new Image();
  img.src = `data:image/jpeg;base64,${data}`;
  img.onload = () => {
    camera_img.src = img.src;
  };
});

