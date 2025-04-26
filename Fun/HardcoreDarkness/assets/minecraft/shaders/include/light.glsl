#version 150

#define MINECRAFT_LIGHT_POWER   (0.6)
#define MINECRAFT_AMBIENT_LIGHT (0.4)

vec4 minecraft_mix_light(vec3 lightDir0, vec3 lightDir1, vec3 normal, vec4 color) {
    lightDir0 = normalize(lightDir0);
    lightDir1 = normalize(lightDir1);
    float light0 = max(0.0, dot(lightDir0, normal));
    float light1 = max(0.0, dot(lightDir1, normal));
    float lightAccum = min(1.0, (light0 + light1) * MINECRAFT_LIGHT_POWER + MINECRAFT_AMBIENT_LIGHT);
    return vec4(color.rgb * lightAccum, color.a);
}

vec4 minecraft_sample_lightmap(sampler2D lightMap, ivec2 uv) {
	float blockLight = uv.x / 16.0;
	float skyLight = uv.y / 16.0;
	
	float darknessMultiplier = ((blockLight / 10.0) + 0.3) * smoothstep(0.0, 7.0, blockLight); // Darker light levels are made more dark for a smoother transition.
	vec4 darkColor = vec4(darknessMultiplier, darknessMultiplier, darknessMultiplier, 1.0); // The "color" of the cave darkness.
	
	vec4 defaultLightColor = texture(lightMap, clamp(uv / 256.0, vec2(0.5 / 16.0), vec2(15.5 / 16.0))); // Gets what the light color would be in vanilla.
	vec4 pureSkyLight = texture(lightMap, clamp(vec2(0.0, 240.0) / 256.0, vec2(0.5 / 16.0), vec2(15.5 / 16.0))); // Gets the light color at block light 0, sky light 15.
	vec4 light0 = texture(lightMap, clamp(vec2(0.0, 0.0) / 256.0, vec2(0.5 / 16.0), vec2(15.5 / 16.0))); // Gets the light color at light level 0.
	
	float nightness = smoothstep(0.1, 0.25, pureSkyLight.r); // Gets how close to night it should be. Also helps with compatibility for different brightnesses.
	vec4 nightColor = (vec4(0.2, 0.225, 0.275, 1.0) + vec4(nightness, nightness, nightness, 1.0)) * smoothstep(9.0, 16.0, (16.0 - blockLight)); // The darkness the game adds at night.
	nightColor = nightColor.r + darkColor.r > 1.0 ? vec4(1.0, 1.0, 1.0, 1.0) - vec4(darkColor.rgb, 0.0) : nightColor; // Prevents the night color from making the game brighter instead of darker. I speak from experience.
	nightness = 1.0 - nightness; // Flip nightness after its purpose in math is finished, to make it more human understandable.
	
	if (blockLight < 8.0 && light0.r > 0.5) blockLight = 8.0; // If it's that bright at light level 0, you probably have night vision on.
	
	vec4 newLightColor = defaultLightColor;
	
	if (blockLight == 0.0 && skyLight == 0.0) newLightColor = vec4(0.0, 0.0, 0.0, 1.0); // If there's no light, make it pitch black. A bit redundant after smoothing darknessMultiplier but I'm just making sure.
	else if (blockLight <= 7.0 && skyLight == 0.0) newLightColor *= darkColor; // If there is low block light and there is no sky light, make it darker.
	else if (blockLight <= 7.0 && skyLight > 0.0 && nightness > 0.0) newLightColor *= darkColor + nightColor; // If there is low block light and it is night, make it darker.
	
	newLightColor.a = 1.0; // Ensures transparency won't break.
	
	return newLightColor; // After all is said and done, return the new light color.
}
