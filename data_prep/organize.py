import os
import shutil


def move_files(src_dir, dest_dir, patterns):
  # if not os.path.exists(dest_dir):
  #   os.makedirs(dest_dir)

  for root, dirs, files in os.walk(src_dir):
    for file in files:
      if not any(pattern in file for pattern in patterns):
        src_file = os.path.join(root, file)
        dest_file = os.path.join(dest_dir, os.path.relpath(src_file, src_dir))
        dest_folder = os.path.dirname(dest_file)
        if not os.path.exists(dest_folder):
          os.makedirs(dest_folder)
        shutil.move(src_file, dest_file)
        print(f"Moved: {src_file} -> {dest_file}")

def find_folders_with_few_files(src_dir, min_files=3):
  for root, dirs, files in os.walk(src_dir):
    # Calculate the relative depth of the current directory
    rel_depth = os.path.relpath(root, src_dir).count(os.sep)

    # Only process directories that are 2 levels deep
    if rel_depth == 2:
      # Count the files in the current directory
      file_count = len(files)
      if file_count < min_files:
        print(f"Folder '{root}' has less than {min_files} files (count: {file_count})")
      # el
      # if file_count > min_files:
      #   print(f"Folder '{root}' has more than {min_files} files (count: {file_count})")

def find_folders_with_few_files_and_generate_links(src_dir, min_files=3, patterns=[]):
  base_url = "http://jsoc.stanford.edu/data/hmi/images"
  for root, dirs, files in os.walk(src_dir):
    # Calculate the relative depth of the current directory
    rel_depth = os.path.relpath(root, src_dir).count(os.sep)

    # Only process directories that are 2 levels deep
    if rel_depth == 2:
      # Count the files in the current directory
      file_count = len(files)
      if file_count < min_files:
        # print(f"Folder '{root}' has less than {min_files*2} files (count: {file_count})")

        # Extract the date part from the folder path
        date_part = os.path.relpath(root, src_dir).replace(os.sep, '/')
        year, month, day = date_part.split('/')

        # Check which patterns are missing
        existing_files = set(files)
        missing_patterns = [pattern for pattern in patterns if not any(pattern in file for file in existing_files)]

        # Generate and print the missing file links
        for pattern in missing_patterns:
          # link = f"{base_url}/{year}/{month}/{day}/{year}{month}{day}{pattern}"
          link = f"{base_url}/{year}/{month}/{day}/"
          print(f"{pattern}: {link}")
        print("\n")

def count_files_with_patterns(src_dir, patterns1, patterns2):
  pattern1_count = 0
  pattern2_count = 0

  for root, dirs, files in os.walk(src_dir):
    for file in files:
      if any(pattern in file for pattern in patterns1):
        pattern1_count += 1
      elif any(pattern in file for pattern in patterns2):
        pattern2_count += 1

  return pattern1_count, pattern2_count

def move_files_and_cleanup(base_path):
  # Iterate over each year folder
  for year in os.listdir(base_path):
    year_path = os.path.join(base_path, year)

    if os.path.isdir(year_path):
      # Iterate over each month folder
      for month in os.listdir(year_path):
        month_path = os.path.join(year_path, month)

        if os.path.isdir(month_path):
          # Iterate over each date folder
          for date in os.listdir(month_path):
            date_path = os.path.join(month_path, date)

            if os.path.isdir(date_path):
              # Move files from date folder to month folder
              for file in os.listdir(date_path):
                _file_path = os.path.join(date_path, file)
                if os.path.isfile(_file_path):
                  try:
                    shutil.move(_file_path, year_path)
                  except Exception as e:
                    print(e)
                  # print(file_path, month_path)
          # Remove the now-empty month folder
          # os.rmdir(month_path)
          # print(f"removing {month_path}")


# Example usage:
# move_files_and_cleanup('/path/to/your/base/folder')


# Define source directory, destination directory and patterns to keep

file_path = os.path.dirname( __file__ )
source_directory = os.path.abspath(os.path.join(file_path, '..', "data", "jsoc", "images"))
destination_directory = os.path.abspath(os.path.join(file_path, '..', "data", "jsoc", "temp_images2"))
patterns_to_keep = ["000000_M_512.jpg", "000000_Ic_flat_512.jpg", "000000_Ic_512.jpg", "000000_M_color_512.jpg"]


# move_files(source_directory, destination_directory, patterns_to_keep)

# find_folders_with_few_files(source_directory)
# find_folders_with_few_files_and_generate_links(source_directory, patterns=patterns_to_keep)


# total_1, total_2 = count_files_with_patterns(source_directory, patterns_to_keep, [])
# print(f"total from pattern 1: {total_1}, pattern 2: {total_2}")

move_files_and_cleanup(source_directory)