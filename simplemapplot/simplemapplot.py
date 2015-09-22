import os
import shutil

default_colors = ["#A6BDDB","#7FA9CF","#2B8CBE","#045A8D"]

svg_file_location = os.path.dirname(__file__)
blank_state_svg = svg_file_location+'/Blank_US_Map.svg'
blank_state_css = svg_file_location+'/Blank_US_Map.css'

def make_us_state_map(data,
    colors=default_colors,
    output_img="output_state_map.svg"):
    if not data: return
    if min(data.values())<0 or max(data.values())>len(colors):
        print("Error: values must range 0 to %s" % len(colors))
        return
    # Determine level for each state in data
    levels = dict( (i, []) for i in range(len(colors)) )
    for key in data:
        level = data[key]
        levels[level].append(key)
    # Create CSS from levels
    css_code = []
    for i, l in enumerate(levels):
        if not levels[l]: continue
        levels[l][0] = "#" + levels[l][0]
        names = ", #".join(levels[l])
        full_string = "%s {\n  fill:%s;\n}" % (names, colors[i])
        css_code.append(full_string)
    # Copy default CSS to local dir
    shutil.copyfile(blank_state_css, "Blank_US_Map.css")
    # Append new style code to CSS file
    style_file = open("Blank_US_Map.css", "a")
    style_file.write("\n".join(css_code))
    style_file.close()
    shutil.copyfile(blank_state_svg, output_img)
    print("Created %s" % output_img)

if __name__ == '__main__':
    example_colors = ["#FC8D59","#FFFFBF","#99D594"]
    state_value = {"TX":2, "WI":1, "IL":1, "AK":0, "MI":0, "HI":2} # key=state abbrev, value=index of color
    make_us_state_map(data=state_value, colors=example_colors)
