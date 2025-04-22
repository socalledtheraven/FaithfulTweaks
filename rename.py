import os
import shutil
import zipfile
import logging
import time # For potential short delays if needed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_and_extract_zips_recursive(root_dir, marker_file="Selected Packs.txt", delete_zip_after_extract=True):
    """
    Recursively walks through root_dir. Finds .zip files in any subdirectory.
    If a zip contains the marker file, it creates a new folder named after the
    zip (without extension) in the SAME directory as the zip, extracts the
    zip's contents into that new folder, and optionally deletes the zip with retries.

    Args:
        root_dir (str): The absolute path to the main root directory to start scanning from.
        marker_file (str, optional): The filename to look for inside the zip archive.
                                     Defaults to "Selected Packs.txt".
        delete_zip_after_extract (bool, optional): Whether to delete the original .zip
                                                  file after successful extraction.
                                                  Defaults to True.
    """
    logging.info(f"Recursively scanning '{root_dir}' for zip files to extract into named folders...")
    total_zips_found = 0
    total_extracted_count = 0
    zips_processed = 0

    if not os.path.isdir(root_dir):
        logging.error(f"Root directory for scanning not found: {root_dir}")
        return

    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file is a zip file
            if filename.lower().endswith(".zip"):
                total_zips_found += 1
                zip_file_path = os.path.join(dirpath, filename)
                relative_path_for_logging = os.path.relpath(zip_file_path, root_dir)
                logging.info(f"Found zip file: '{relative_path_for_logging}'. Checking for '{marker_file}'...")
                zips_processed += 1

                extract_folder_name = os.path.splitext(filename)[0]
                target_extract_path = os.path.join(dirpath, extract_folder_name)

                try:
                    contains_marker = False
                    # Check for marker
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref_check:
                         if any(f.endswith(marker_file) for f in zip_ref_check.namelist()):
                             contains_marker = True
                             logging.info(f"'{marker_file}' found within '{relative_path_for_logging}'.")
                         else:
                            logging.info(f"'{marker_file}' not found within '{relative_path_for_logging}'. Skipping extraction.")

                    if contains_marker:
                        # Check existence before extraction
                        if os.path.exists(target_extract_path):
                            logging.warning(f"Target extraction folder '{extract_folder_name}' already exists at '{os.path.relpath(target_extract_path, root_dir)}'. Skipping extraction for '{relative_path_for_logging}'.")
                            continue

                        logging.info(f"Creating folder '{extract_folder_name}' and extracting '{relative_path_for_logging}' into it...")
                        os.makedirs(target_extract_path, exist_ok=True)

                        # Extract
                        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref_extract:
                            zip_ref_extract.extractall(target_extract_path)
                            logging.info(f"Successfully extracted '{relative_path_for_logging}' into '{os.path.relpath(target_extract_path, root_dir)}'")
                            total_extracted_count += 1
                        # --- zip_ref_extract is now closed ---

                        # --- Attempt Deletion with Retries ---
                        if delete_zip_after_extract:
                            deleted = False
                            max_retries = 5  # Number of attempts
                            retry_delay = 0.5 # Seconds to wait between attempts
                            for attempt in range(max_retries):
                                try:
                                    logging.info(f"Attempt {attempt + 1}/{max_retries} to delete original zip file: {relative_path_for_logging}")
                                    os.remove(zip_file_path)
                                    logging.info(f"Successfully deleted original zip file: {relative_path_for_logging}")
                                    deleted = True
                                    break # Exit loop if successful
                                except OSError as e_del:
                                    if e_del.winerror == 32 and attempt < max_retries - 1: # Check if it's the specific locking error and not the last attempt
                                        logging.warning(f"Attempt {attempt + 1} failed: File is locked (WinError 32). Retrying in {retry_delay} seconds...")
                                        time.sleep(retry_delay) # Wait before retrying
                                    else: # If it's a different error or the last attempt
                                        logging.error(f"Failed to delete zip file '{relative_path_for_logging}' after extraction: {e_del}")
                                        break # Stop trying on other errors or last attempt failure
                                except Exception as e_del_generic:
                                     logging.error(f"An unexpected error occurred during deletion attempt {attempt + 1} of '{relative_path_for_logging}': {e_del_generic}")
                                     break # Stop trying on unexpected errors
                            if not deleted:
                                logging.error(f"Could not delete zip file '{relative_path_for_logging}' after {max_retries} attempts.")
                        # --- End Deletion Logic ---

                except zipfile.BadZipFile:
                    logging.error(f"Error: '{relative_path_for_logging}' is not a valid zip file or is corrupted.")
                except PermissionError as pe:
                    logging.error(f"Permission denied while processing '{relative_path_for_logging}': {pe}")
                except OSError as e_os:
                    logging.error(f"OS error while processing '{relative_path_for_logging}': {e_os}")
                except Exception as e_proc:
                    logging.error(f"An unexpected error occurred while processing '{relative_path_for_logging}': {e_proc}")

    logging.info(f"Zip extraction scan complete. Found {total_zips_found} zip files, processed {zips_processed}, successfully created folders and extracted for {total_extracted_count}.")


def rename_folders(root_dir):
    """
    Recursively walks the root_dir. If a directory contains a file named
    "Selected Packs.txt", it renames THAT directory based on the content
    of the file (specifically line 4). Assumes the directory to be renamed
    is the one directly containing "Selected Packs.txt".

    Args:
        root_dir (str): The absolute path to the main root directory to start scanning from.
    """
    logging.info(f"Recursively scanning '{root_dir}' for folders to rename based on 'Selected Packs.txt'...")
    renamed_count = 0
    # Use a list to collect folders to rename to avoid modifying structure during os.walk iteration
    folders_to_process = []

    # First pass: Collect potential candidates using os.walk
    for dirpath, _, filenames in os.walk(root_dir):
        if "Selected Packs.txt" in filenames:
            # Check if this dirpath itself should be renamed
            marker_filepath = os.path.join(dirpath, "Selected Packs.txt")
            # Add the directory containing the marker file and the marker file path itself
            folders_to_process.append({'folder_to_rename_path': dirpath, 'marker_path': marker_filepath})
            logging.debug(f"Found potential rename target: {os.path.relpath(dirpath, root_dir)} based on marker file.")

    if not folders_to_process:
        logging.info("No folders found containing 'Selected Packs.txt' for renaming.")
        return

    logging.info(f"Found {len(folders_to_process)} potential folders to rename. Processing...")

    # Second pass: Perform the renaming. Sort by path length (longest first) to process deeper folders first.
    folders_to_process.sort(key=lambda x: len(x['folder_to_rename_path']), reverse=True)

    for item in folders_to_process:
        dirpath = item['folder_to_rename_path']
        marker_filepath = item['marker_path']

        # Check if the directory still exists (it might have been renamed as part of a parent rename)
        if not os.path.isdir(dirpath):
            logging.warning(f"Directory '{os.path.basename(dirpath)}' no longer exists at expected path '{os.path.relpath(dirpath, root_dir)}'. Skipping rename (may have been renamed/deleted already).")
            continue

        current_folder_name = os.path.basename(dirpath)
        parent_dir = os.path.dirname(dirpath)

        logging.info(f"Processing '{os.path.relpath(marker_filepath, root_dir)}' for potential rename of folder '{current_folder_name}'")
        try:
            with open(marker_filepath, "r", encoding='utf-8') as f:
                lines = f.readlines()

            if len(lines) >= 4 and lines[3].strip():
                pack_name_raw = lines[3].strip()
                # --- Pack Name Cleaning ---
                pack_name = pack_name_raw.strip(' -*_.\t\n\r')
                invalid_chars = '<>:"/\\|?*' + ''.join(chr(i) for i in range(32))
                for char in invalid_chars:
                    pack_name = pack_name.replace(char, '_')
                pack_name = pack_name.strip('. ')

                if not pack_name:
                    logging.warning(f"Derived pack name from '{os.path.relpath(marker_filepath, root_dir)}' is empty after cleaning. Skipping rename for '{current_folder_name}'.")
                    continue

                new_dirpath = os.path.join(parent_dir, pack_name)

                # --- Rename Checks ---
                if os.path.abspath(dirpath) == os.path.abspath(new_dirpath):
                    logging.info(f"Folder '{current_folder_name}' already has the correct name '{pack_name}'. Skipping.")
                    continue
                if os.path.exists(new_dirpath):
                    logging.warning(f"Cannot rename '{current_folder_name}' to '{pack_name}' in '{os.path.relpath(parent_dir, root_dir)}' because a folder/file with the target name already exists: '{pack_name}'")
                    continue

                # --- Perform Rename ---
                logging.info(f"Attempting rename: '{os.path.relpath(dirpath, root_dir)}' -> '{os.path.relpath(new_dirpath, root_dir)}'")
                os.rename(dirpath, new_dirpath)
                logging.info(f"Successfully renamed '{current_folder_name}' to '{pack_name}' in '{os.path.relpath(parent_dir, root_dir)}'")
                renamed_count += 1

            else:
                logging.warning(f"Could not determine pack name from '{os.path.relpath(marker_filepath, root_dir)}' in folder '{current_folder_name}'. Expected at least 4 lines with content on line 4.")

        except FileNotFoundError:
             logging.warning(f"Marker file '{os.path.relpath(marker_filepath, root_dir)}' or its directory '{os.path.relpath(dirpath, root_dir)}' not found during rename phase. Skipping.")
        except PermissionError as pe:
            logging.error(f"Permission denied trying to rename '{current_folder_name}' to '{pack_name}' (path: {os.path.relpath(dirpath, root_dir)}): {pe}")
        except Exception as e:
            logging.error(f"An error occurred processing '{os.path.relpath(marker_filepath, root_dir)}' for rename of '{current_folder_name}': {e}")

    logging.info(f"Folder renaming scan complete. Attempted rename based on {len(folders_to_process)} markers, successfully renamed {renamed_count} folders.")


# --- Main execution block ---
if __name__ == "__main__":
    # --- IMPORTANT: Set this to the ACTUAL main directory ---
    # Example: The directory containing 'Terrain', 'GUI', 'Items', etc.
    main_root_directory = r"D:\Minecraft\resourcepacks\FaithfulTweaks\main" #<--- UPDATE THIS PATH

    logging.info(f"Starting script processing for main directory: {main_root_directory}")

    if not os.path.isdir(main_root_directory):
         logging.critical(f"CRITICAL ERROR: Main root directory specified does not exist: {main_root_directory}")
         logging.critical("Script cannot continue. Please correct the 'main_root_directory' variable.")
    else:
        # --- Step 1: Recursively find zips, check marker, extract into NEW named folders ---
        find_and_extract_zips_recursive(main_root_directory,
                                        marker_file="Selected Packs.txt",
                                        delete_zip_after_extract=True) # Deletion is enabled

        # --- Step 2: Recursively find folders with marker, rename the folder based on marker content ---
        rename_folders(main_root_directory)

        logging.info("Script finished.")