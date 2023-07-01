#version 330
#extension GL_ARB_seperate_shadder_objects : enable

layout (location=0) in vec3 vertexColour;
layout (location=1) in vec3 texCoords;

uniform camplerCube skyBox;

layout (location=0) out vec4 regular_colour;
layout (location=1) out vec4 bright_colour;

void main()
{
    //return pixel colour
    regular_colour = vec4(fragmentColour * vec3(texture(skyBox, texCoords)), 0.1);
    bright_colour = vec4(vec3(0.0), 0.1);
}