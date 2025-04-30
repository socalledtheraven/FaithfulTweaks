#version 150

in vec3 Position;
in vec4 Color;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;

out vec4 vertexColor;
out float isSpyglass;

void main() {

    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);

    float depth = (ModelViewMat * vec4(Position, 1.0)).z;
    
    isSpyglass = 0;
    if (-11100 < depth && depth < -11075) {
        isSpyglass = 1.0;
    }

    vertexColor = Color;
}
