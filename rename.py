import os

def rename_folders(root_dir):
    """
    Renames folders based on the "Selected Packs.txt" file content.

    Args:
        root_dir (str): The root directory containing the folders.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "Selected Packs.txt" in filenames:
            filepath = os.path.join(dirpath, "Selected Packs.txt")
            try:
                with open(filepath, "r") as f:
                    lines = f.readlines()

                if len(lines) == 4:
                    pack_name = lines[3].strip()  # Get the pack name from line 4
                    if pack_name.startswith("    "):
                        pack_name = pack_name[4:] #remove the 4 leading spaces
                    parent_dir = os.path.dirname(dirpath)
                    new_dirpath = os.path.join(parent_dir, pack_name)

                    os.rename(dirpath, new_dirpath)
                    print(f"Renamed '{os.path.basename(dirpath)}' to '{pack_name}'")
                else:
                    print(f"Incorrect number of lines in '{filepath}':")
                    for line in lines:
                        print(line.strip())
            except FileNotFoundError:
                print(f"File not found: {filepath}")
            except Exception as e:
                print(f"An error occurred with '{filepath}': {e}")

# Example usage:
root_directory = "D:\\Minecraft\\resourcepacks\\FaithfulTweaks\\main\\"  # Replace with your actual directory path
rename_folders(root_directory)