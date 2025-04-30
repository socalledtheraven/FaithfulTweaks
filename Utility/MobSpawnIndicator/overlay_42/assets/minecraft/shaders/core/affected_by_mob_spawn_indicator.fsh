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

in vec2 lightLevel;
in vec2 faceCoords;
in float stairs;

out vec4 fragColor;

#define THICKNESS (sqrt(2) / 2 / 16.0)
#define OUTLINE ((16 - (7.5 * sqrt(2))) / 32.0)
#define CORNER (9.9 / 16.0)

void main() {
    vec4 color = texture(Sampler0, texCoord0);
#ifdef ALPHA_CUTOUT
    if (color.a < ALPHA_CUTOUT) {
        discard;
    }
#endif

    float lightLevelOpacity = 0.45;

    if (lightLevel.x <= 1*16+1) {
        lightLevelOpacity = 1;
        
    } else if (lightLevel.x <= 7*16+1) {
        lightLevelOpacity = 0.7;
    }

    vec4 vtc = vertexColor;

    bool shape = abs(faceCoords.x + faceCoords.y - 1) < THICKNESS || abs(faceCoords.x - faceCoords.y) < THICKNESS;
    bool corners = abs(faceCoords.x + faceCoords.y - 1) < (CORNER * lightLevelOpacity) && abs(faceCoords.x - faceCoords.y) < (CORNER * lightLevelOpacity);

    if (shape && corners && stairs < (1.0 / 255.0)) {
        if (lightLevel.x <= 1*16+1) {
            color *= vec4(4.0,0.0,0.0,1.0); //? RED

        } else if (lightLevel.x <= 7*16+1) {
            color *= vec4(4.0,1.5,0.0,1.0); //? ORANGE

        } else if (lightLevel.x <= 11*16+1) {
            color *= vec4(4.0,4.0,0.0,1.0); //? YELLOW
            
        } 

        vtc = mix(vertexColor, vec4(1.), 0.5);
    }

    color *= vtc * ColorModulator;
    color = clamp(color, 0.0, 1.0);

    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}
