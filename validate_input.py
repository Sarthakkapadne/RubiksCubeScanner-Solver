def validate_cube_state(cube_state):
    """Validate the cube state dictionary"""
    if len(cube_state) != 6:
        print("❌ Invalid number of faces. Must be exactly 6.")
        return False
    
    required_faces = {'U', 'R', 'F', 'D', 'L', 'B'}
    if set(cube_state.keys()) != required_faces:
        print("❌ Missing or extra faces. Required: U, R, F, D, L, B")
        return False
    
    color_counts = {'W': 0, 'R': 0, 'O': 0, 'Y': 0, 'G': 0, 'B': 0}
    
    for face, colors in cube_state.items():
        if len(colors) != 9:
            print(f"❌ Face {face} has {len(colors)} colors (should be 9)")
            return False
        
        for color in colors:
            if color not in color_counts:
                print(f"❌ Invalid color '{color}' in face {face}")
                return False
            color_counts[color] += 1
    
    for color, count in color_counts.items():
        if count != 9:
            print(f"❌ Color {color} appears {count} times (should be 9)")
            return False
    
    # Check center colors are unique
    centers = [colors[4] for colors in cube_state.values()]
    if len(set(centers)) != 6:
        print("❌ Center colors are not unique")
        return False
    
    return True

def is_valid_cube_string(cube_string):
    """Validate the 54-character cube string"""
    if len(cube_string) != 54:
        print("❌ Invalid length. Must be exactly 54 characters.")
        return False
    
    valid_chars = {'U', 'R', 'F', 'D', 'L', 'B'}
    if any(c not in valid_chars for c in cube_string):
        print("❌ Invalid characters in cube string. Only U, R, F, D, L, B allowed.")
        return False
    
    # Each face should have 9 of its center color
    face_counts = {face: cube_string.count(face) for face in valid_chars}
    for face, count in face_counts.items():
        if count != 9:
            print(f"❌ Face {face} appears {count} times (should be 9)")
            return False
    
    return True