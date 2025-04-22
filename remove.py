import os
import shutil
import logging

# Configure logging for better feedback
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_subdirectories(target_directory=None):
    """
    Finds all immediate subdirectories in the specified directory (or the current
    working directory if None) and removes all files and folders within each
    subdirectory, leaving the subdirectories themselves empty.

    Args:
        target_directory (str, optional): The path to the directory containing
                                          the subdirectories to clean.
                                          Defaults to the current working directory.
    """
    if target_directory is None:
        target_directory = os.getcwd() # Get the directory where the script is run

    logging.info(f"Scanning directory: {target_directory}")

    if not os.path.isdir(target_directory):
        logging.error(f"Error: Target directory '{target_directory}' not found or is not a directory.")
        return

    subdirectories_to_clean = []
    try:
        # List all items (files and folders) in the target directory
        for item_name in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item_name)
            # Check if it's a directory and not a hidden one (like .git)
            if os.path.isdir(item_path) and not item_name.startswith('.'):
                subdirectories_to_clean.append(item_path)
    except OSError as e:
        logging.error(f"Error accessing directory {target_directory}: {e}")
        return

    if not subdirectories_to_clean:
        logging.warning("No non-hidden subdirectories found to clean.")
        return

    logging.info("Found the following subdirectories to potentially clean:")
    for subdir in subdirectories_to_clean:
        logging.info(f"- {os.path.basename(subdir)}")

    # --- SAFETY CONFIRMATION ---
    confirm = input(f"\nWARNING: This will permanently delete all content inside the listed subdirectories in '{target_directory}'.\nType 'YES' to confirm: ")
    if confirm.strip().upper() != 'YES':
        logging.warning("Operation cancelled by user.")
        return
    # --- END SAFETY CONFIRMATION ---

    logging.info("Proceeding with cleaning...")

    cleaned_count = 0
    error_count = 0

    for subdir_path in subdirectories_to_clean:
        subdir_name = os.path.basename(subdir_path)
        logging.info(f"--- Cleaning subdirectory: {subdir_name} ---")
        try:
            items_in_subdir = os.listdir(subdir_path)
            if not items_in_subdir:
                logging.info(f"'{subdir_name}' is already empty.")
                continue

            for item_name in items_in_subdir:
                item_path_to_delete = os.path.join(subdir_path, item_name)
                try:
                    if os.path.isfile(item_path_to_delete) or os.path.islink(item_path_to_delete):
                        os.remove(item_path_to_delete)
                        # logging.debug(f"Deleted file: {item_path_to_delete}") # Optional: more verbose logging
                    elif os.path.isdir(item_path_to_delete):
                        shutil.rmtree(item_path_to_delete)
                        # logging.debug(f"Deleted folder and contents: {item_path_to_delete}") # Optional
                    else:
                        logging.warning(f"Skipping unknown item type: {item_path_to_delete}")

                except Exception as e:
                    logging.error(f"Failed to delete {item_path_to_delete}: {e}")
                    error_count += 1

            # Verify if empty after cleaning attempt
            if not os.listdir(subdir_path):
                 logging.info(f"Successfully cleaned '{subdir_name}'.")
                 cleaned_count +=1
            else:
                 logging.warning(f"'{subdir_name}' may not be completely empty due to errors.")


        except OSError as e:
            logging.error(f"Error accessing or listing contents of subdirectory {subdir_name}: {e}")
            error_count += 1
        logging.info(f"--- Finished cleaning {subdir_name} ---")


    logging.info("="*20 + " Summary " + "="*20)
    logging.info(f"Attempted to clean {len(subdirectories_to_clean)} subdirectories.")
    logging.info(f"Successfully emptied (or found empty): {cleaned_count} subdirectories.")
    if error_count > 0:
        logging.error(f"Encountered {error_count} errors during deletion.")
    logging.info("="*49)

# --- Main execution block ---
if __name__ == "__main__":
    # This part runs only when the script is executed directly
    # You can optionally pass a specific directory path here, e.g.,
    # clean_subdirectories("/path/to/your/folder")
    # If no path is given, it uses the directory where the script is located.
    clean_subdirectories()