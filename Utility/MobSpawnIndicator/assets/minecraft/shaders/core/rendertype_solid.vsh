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

out vec2 lightLevel;
out vec2 faceCoords;
out float stairs;

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

    if (!(fract(Position.x) >= 0.7 || fract(Position.z) >= 0.7) && (fract(Position.x) > 0 || fract(Position.z) > 0)) {
        stairs = 1.0;
    } else {
        stairs = 0.0;
    }

    lightLevel = UV2;
    
    const vec2[4] corners = vec2[4](
        vec2(0, 1),
        vec2(0, 0),
        vec2(1, 0),
        vec2(1, 1)
    );

    faceCoords = corners[gl_VertexID % 4];
}
