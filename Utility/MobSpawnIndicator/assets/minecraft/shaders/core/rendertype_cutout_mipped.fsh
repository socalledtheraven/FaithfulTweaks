#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;
in vec4 normal;

in vec2 lightLevel;
in vec2 faceCoords;
flat in float up;
in float stairs;

out vec4 fragColor;

#define THICKNESS sqrt(2) / 2 / 16.0
#define OUTLINE (16 - (7.5 * sqrt(2))) / 32.0
#define CORNER 9.9 / 16.0

#define LEVEL *16+1


void main() {
    vec4 color = texture(Sampler0, texCoord0);
    if (color.a < 0.5) discard;

    float LL = 0.45;

    if (lightLevel.x <= 1 LEVEL) LL = 1;
    else if (lightLevel.x <= 7 LEVEL) LL = 0.7;

    vec4 vtc = vertexColor;

    bool shape = abs(faceCoords.x + faceCoords.y - 1) < THICKNESS || abs(faceCoords.x - faceCoords.y) < THICKNESS;
    bool corners = abs(faceCoords.x + faceCoords.y - 1) < CORNER*LL && abs(faceCoords.x - faceCoords.y) < CORNER*LL;
    if (shape && corners && stairs < (1.0 / 255.0)) {
        if (lightLevel.x <= 1 LEVEL) color *= vec4(4,0,0,1) * ColorModulator; //? RED
        else if (lightLevel.x <= 7 LEVEL) color *= vec4(4,1.5,0,1) * ColorModulator; //? ORANGE
        else if (lightLevel.x <= 11 LEVEL) color *= vec4(4,4,0,1) * ColorModulator; //? YELLOW

        vtc = mix(vertexColor, vec4(1.), 0.5);
    }
    color *= vtc * ColorModulator;
    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}
