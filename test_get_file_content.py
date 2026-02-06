from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info

def main():
    print("root director contents:")
    print(get_file_content("calculator", "lorem.txt"))

    # print("pkg directory contents:")
    # print(get_files_info("calculator", "pkg"))
    
    # print("bin director contents:")
    # print(get_files_info("calculator", "/bin"))

    # print("../ director contents:")
    # print(get_files_info("calculator", "../"))

main()

