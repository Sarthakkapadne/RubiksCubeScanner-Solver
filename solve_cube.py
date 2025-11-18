import kociemba
from validate_input import is_valid_cube_string

def solve_cube():
    try:
        with open("cube_string.txt", "r") as file:
            cube_string = file.read().strip()
        
        if not is_valid_cube_string(cube_string):
            print("❌ Cannot solve - invalid cube string")
            return
        
        print(f"\nSolving cube: {cube_string}")
        solution = kociemba.solve(cube_string)
        
        print("\n✅ Solution Steps:")
        print(solution)
        
        # Save solution to file
        with open("solution.txt", "w") as f:
            f.write(solution)
        print("\n💾 Solution saved to solution.txt")
        
    except FileNotFoundError:
        print("❌ cube_string.txt not found. Run capture_faces.py first.")
    except Exception as e:
        print(f"❌ Error solving cube: {e}")

if __name__ == "__main__":
    solve_cube()