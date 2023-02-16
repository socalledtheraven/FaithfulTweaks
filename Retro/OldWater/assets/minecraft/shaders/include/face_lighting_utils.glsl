#version 150

// Checks if something is *roughly* equal to something else, helps stop jank.

bool roughly_equal(float inputValue, float target) {
	
	float targetLess = target - 0.01;
	float targetMore = target + 0.01;
	return (inputValue > targetLess && inputValue < targetMore);
	
}

// Gets the dimension that an object is in, -1 for The Nether, 0 for The Overworld, 1 for The End.

float get_dimension(vec4 minLightColor) {
	
	if (minLightColor.r == minLightColor.g && minLightColor.g == minLightColor.b) return 0.0; // Shadows are grayscale in The Overworld
	else if (minLightColor.r > minLightColor.g) return -1.0; // Shadows are more red in The Nether
	else return 1.0; // Shadows are slightly green in The End
	
}

// Gets the lighting of a face and returns it.

vec4 get_face_lighting(float dimension, vec4 inColor) { 
	
	vec4 changedColor = inColor;
	
	float top = 229.0 / 255.0;
	float bottom = 127.0 / 255.0;
	float east = 153.0 / 255.0;
	float north = 204.0 / 255.0;
	
	// Bottom (only do if not Nether)
	if (!roughly_equal(dimension, -1.0)) { changedColor /= vec4(bottom, bottom, bottom, 1.0);
	if (!(changedColor.r > 1.0 || changedColor.g > 1.0 || changedColor.b > 1.0)) return vec4(bottom, bottom, bottom, 1.0);
	changedColor = inColor; }

	// East-West
	changedColor /= vec4(east, east, east, 1.0);
	if (!(changedColor.r > 1.0 || changedColor.g > 1.0 || changedColor.b > 1.0)) return vec4(east, east, east, 1.0);
	changedColor = inColor;

	// North-South
	changedColor /= vec4(north, north, north, 1.0);
	if (!(changedColor.r > 1.0 || changedColor.g > 1.0 || changedColor.b > 1.0)) return vec4(north, north, north, 1.0);
	changedColor = inColor;
	
	// Top (only required in the Nether)
	if (roughly_equal(dimension, -1.0)) { changedColor /= vec4(top, top, top, 1.0);
	if (!(changedColor.r > 1.0 || changedColor.g > 1.0 || changedColor.b > 1.0)) return vec4(top, top, top, 1.0);
	changedColor = inColor; }

	return vec4(1.0, 1.0, 1.0, 1.0);
}


// Gets the lighting of a face and returns it.

vec4 get_face_lighting_normal(vec3 normal, float dimension) { 
	
	vec4 faceLighting = vec4(1.0, 1.0, 1.0, 1.0);
	vec3 absNormal = abs(normal);
	
	float top = 229.0 / 255.0;
	float bottom = 127.0 / 255.0;
	float east = 153.0 / 255.0;
	float north = 204.0 / 255.0;
	
	// Top (only required in the Nether)
	if (normal.y > normal.z && normal.y > normal.x && roughly_equal(dimension, -1.0)) faceLighting = vec4(top, top, top, 1.0);
	
	// Bottom
	if (normal.y < normal.z && normal.y < normal.x && !roughly_equal(dimension, -1.0)) faceLighting = vec4(bottom, bottom, bottom, 1.0);
	else if (normal.y < normal.z && normal.y < normal.x && roughly_equal(dimension, -1.0)) faceLighting = vec4(top, top, top, 1.0);

	// East-West
	if (absNormal.x > absNormal.z && absNormal.x > absNormal.y) faceLighting = vec4(east, east, east, 1.0);

	// North-South
	if (absNormal.z > absNormal.x && absNormal.z > absNormal.y) faceLighting = vec4(north, north, north, 1.0);

	return faceLighting;
}