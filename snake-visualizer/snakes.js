var gameId, state = {board: [[]]};
var canvas = document.getElementById('game');
canvas.width = 640;
canvas.height = 640 * 25 / 40;
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

      if (token === 'R') {
        gfx.fillStyle = '#0035FF'
      }
      if (token === 'B') {
        gfx.fillStyle = '#FF3900';
      }
      if (token === '@') {
        gfx.fillStyle = '#68CC00';
      }

      var cellWidth = canvas.width / map[row].length;
      var cellHeight = canvas.height / map.length;
      var x = col * cellWidth;
      var y = row * cellHeight;
      gfx.fillRect(x, y, cellWidth, cellHeight);
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
