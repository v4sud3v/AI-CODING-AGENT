from functions.write_file import write_file
import os
import shutil

def main():
    # Setup: Ensure the 'calculator' directory exists for testing
    if not os.path.exists("calculator"):
        os.makedirs("calculator")

    # Test Case 1: Simple write
    res1 = write_file("calculator", "calculator/lorem.txt", "wait, this isn't lorem ipsum")
    print(res1)

    # Test Case 2: Write with nested directories
    res2 = write_file("calculator", "calculator/pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(res2)

    # Test Case 3: Unauthorized path (Security check)
    res3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(res3)

    # Optional Cleanup: Uncomment if you want to wipe test files after running
    # shutil.rmtree("calculator/pkg", ignore_errors=True)

if __name__ == "__main__":
    main()