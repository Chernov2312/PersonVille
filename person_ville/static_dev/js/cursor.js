const circle = document.createElement('div');
circle.className = 'cursor-circle';
document.body.appendChild(circle);

document.addEventListener('mousemove', (e) => {
  circle.style.left = e.pageX + 'px';
  circle.style.top = e.pageY + 'px';
});