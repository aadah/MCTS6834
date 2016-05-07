var mapText = '0 0 0 0 0 0 0 0\n'
              + '0 0 1 0 0 0 0 0\n'
              + '0 0 1 0 0 0 0 0\n'
              + '0 0 1 0 0 0 0 0\n'
              + '0 0 1 2 2 2 2 0\n'
              + '0 0 1 0 0 0 0 0\n'
              + '0 0 1 0 0 0 0 0\n'
              + '0 0 0 0 0 0 0 0'

var map = mapText.split('\n').map(function(line) {
  return line.split(' ').filter(function(token) {
    return token.length > 0;
  });
});

var canvas = document.getElementById('game');
canvas.width = map.length * 16;
canvas.height = map.length * 16;
var gfx = canvas.getContext('2d');

function draw() {
  gfx.fillStyle = 'rgba(0, 0, 0, 0.2)';
  gfx.fillRect(0, 0, canvas.width, canvas.height);

  for (var row = 0; row < map.length; row++) {
    for (var col = 0; col < map[row].length; col++) {
      var token = map[row][col];
      if (token === '0') {
        continue;
      }

      if (token === '1') {
        gfx.fillStyle = '#0035FF'
      }
      if (token === '2') {
        gfx.fillStyle = '#FF3900';
      }
      if (token === '3') {
        gfx.fillStyle = '#68CC00';
      }

      var cellWidth = canvas.width / map.length;
      var cellHeight = canvas.height / map[row].length;
      var x = col * cellHeight;
      var y = row * cellWidth;
      gfx.fillRect(x, y, cellWidth, cellHeight);
    }
  }
  if (Math.random() < 33 / 250) {
    var foodRow = Math.floor(Math.random() * map.length);
    var foodCol = Math.floor(Math.random() * map.length);
    var prev = map[foodRow][foodCol];
    if (prev !== '3') {
      map[foodRow][foodCol] = '3';
      setTimeout(function() {
        map[foodRow][foodCol] = prev;
      }, 250);
    }
  }
  window.requestAnimationFrame(draw);
}

draw()
