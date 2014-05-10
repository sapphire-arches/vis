#version 120

void main() {
  vec4 position = gl_Vertex;
//  position.x *= 0.1;
//  position.y *= 0.1;
//  position.z *= 0.1;
  gl_Position = gl_ModelViewMatrix * position;
  gl_FrontColor = gl_Color;
}
