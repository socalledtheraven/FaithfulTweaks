#version 150

#moj_import <light.glsl>
#moj_import <fog.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in ivec2 UV2;
in vec3 Normal;

uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform vec3 ChunkOffset;
uniform int FogShape;

out float vertexDistance;
out vec4 vertexColor;
out vec2 texCoord0;
out vec4 normal;

out vec2 lightLevel;
out vec2 faceCoords;
flat out float up;
out float stairs;
// out vec2 faceWorldCoords;

vec2 generateFaceCoords(){
    if (gl_VertexID % 4 == 0) return vec2(1.0,0.0);
    else if (gl_VertexID % 4 == 1) return vec2(1.0,1.0);
    else if (gl_VertexID % 4 == 2) return vec2(0.0,1.0);
    else if (gl_VertexID % 4 == 3) return vec2(0.0,0.0);
}

void main() {
    vec3 pos = Position + ChunkOffset;
    gl_Position = ProjMat * ModelViewMat * vec4(pos, 1.0);
    vertexDistance = fog_distance(ModelViewMat, pos, FogShape);
    vertexColor = Color * minecraft_sample_lightmap(Sampler2, UV2);
    texCoord0 = UV0;
    normal = ProjMat * ModelViewMat * vec4(Normal, 0.0);

    if (!(fract(Position.x) >= 0.7 || fract(Position.z) >= 0.7) && (fract(Position.x) > 0 || fract(Position.z) > 0) || fract(Position.y) == 0.5) stairs = 1.0;
    else stairs = 0.0;

    if (Normal == vec3(0,1,0) && fract(Position.y) < 0.1) up = 1;
    else up = 0;

    lightLevel = UV2;
    faceCoords = generateFaceCoords();

    // if (Normal == vec3(1,0,0) || Normal == vec3(-1,0,0)) faceWorldCoords = vec2(Position.y, Position.z);
    // else if (Normal == vec3(0,0,1) || Normal == vec3(0,0,-1)) faceWorldCoords = vec2(Position.x, Position.y);
    // else faceWorldCoords = vec2(Position.x, Position.z);
}
