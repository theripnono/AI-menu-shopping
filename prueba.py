def control_ids(new_ids: list = None) -> list:
    """
    Controls the usage of ids. If a list of new_ids is provided, it appends them to the file.
    If no list is provided, it reads the ids from the file and returns them.

    Args:
        new_ids (list): A list of new ids to append to the file. If None, the function reads the ids from the file.

    Returns:
        list: The updated list of ids from the file.
    """
    
    file_path = 'logs_ids.txt'

    # If new ids are provided, append them to the file
    if new_ids:
        with open(file_path, "a", encoding="utf-8") as file:  # "a" for append mode
            file.write(','.join(map(str, new_ids)) + ',')  # Append new ids followed by a comma

    # Read the existing ids from the file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip(',')
            existing_ids = content.split(',') if content else []
    except FileNotFoundError:
        existing_ids = []

    return existing_ids  # Return the updated list

# Example usage:

# Adding new ids
for i in range(1,5):
    control_ids([i])

# Reading the updated list of ids
#ids = control_ids()
#print(ids)  # Output: ['10', '20', '30', '40', '50', '60']
