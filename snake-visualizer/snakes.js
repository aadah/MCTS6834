var gameId, state = {board: [[]]};
var canvas = document.getElementById('game');
var cellSize = 28;
canvas.width = cellSize * 40;
canvas.height = cellSize * 25;
var gfx = canvas.getContext('2d');

function update() {
  if (!gameId) {
    gameId = state.gameId;
  }
  if (state.gameId != gameId) {
    return;
  }
}

function draw() {
  gfx.fillStyle = 'rgba(0, 0, 0, 0.2)';
  gfx.fillRect(0, 0, canvas.width, canvas.height);

  var map = state.board;

  for (var row = 0; row < map.length; row++) {
    for (var col = 0; col < map[row].length; col++) {
      var token = map[row][col];
      if (token === ' ') {
        continue;
      }

      switch (token) {
      case 'R':
      case '+':
        gfx.fillStyle = '#FF3900';
        break;
      case 'B':
      case 'x':
        gfx.fillStyle = '#0035FF'
        break;
      case '@':
        gfx.fillStyle = '#68CC00';
        break;
      }

      var x = col * cellSize;
      var y = row * cellSize;


      if (token !== '+' && token !== 'x') {
        gfx.fillRect(x, y, cellSize, cellSize);
        continue;
      }
      var dir = state.rDir;
      if (token === 'x') {
        dir = state.bDir;
      }
      var cellWidth = cellSize;
      var cellHeight = cellSize;
      var centerX = x + cellSize / 2;
      var centerY = y + cellSize / 2;
      var dirAngle = 0;
      switch (dir) {
      case 0:
        break;
      case 3:
        cellWidth /= 2;
        dirAngle = 0;
        break;
      case 2:
        cellHeight /= 2;
        dirAngle = Math.PI / 2;
        break;
      case 1:
        x = centerX;
        cellWidth /= 2;
        dirAngle = Math.PI;
        break;
      case 4:
        y = centerY;
        cellHeight /= 2;
        dirAngle = 3 * Math.PI / 2;
        break;
      }
      var startAngle = dirAngle - Math.PI / 2;
      var endAngle = dirAngle + Math.PI / 2;
      gfx.beginPath()
      gfx.arc(centerX, centerY, cellSize / 2, startAngle, endAngle);
      gfx.closePath();
      gfx.fill();
      gfx.fillRect(x, y, cellWidth, cellHeight);

      gfx.fillStyle = 'white';
      gfx.translate(centerX, centerY);
      gfx.rotate(dirAngle);

      gfx.beginPath();
      gfx.arc(cellSize * 0.2, -cellSize * 0.2, cellSize * 0.17, 0, 2 * Math.PI);
      gfx.fill();
      gfx.beginPath();
      gfx.arc(cellSize * 0.2, cellSize * 0.2, cellSize * 0.17, 0, 2 * Math.PI);
      gfx.fill();

      gfx.fillStyle = 'black';
      gfx.beginPath();
      gfx.arc(0.23 * cellSize, -0.2 * cellSize, cellSize * 0.1, 0, 2 * Math.PI);
      gfx.fill();
      gfx.beginPath();
      gfx.arc(0.23 * cellSize, 0.2 * cellSize, cellSize * 0.1, 0, 2 * Math.PI);
      gfx.fill();
      gfx.setTransform(1, 0, 0, 1, 0, 0);
    }
  }

  window.requestAnimationFrame(draw);
}

function pullState() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '../vis/game-state.json', true);
  xhr.overrideMimeType('text/plain');
  xhr.onload = function() {
    window.requestAnimationFrame(pullState);
    var newState = JSON.parse(xhr.responseText);
    // Hacky deduplication
    if (JSON.stringify(state) === JSON.stringify(newState)) {
      return;
    }
    state = newState;
    update();
  };
  xhr.send();
}

draw();
pullState();
