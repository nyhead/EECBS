import os
import re

# Define the directory path and prefix
project_dir = "."  # Root directory of your project
prefix = 'PREFIX_'  # Replace with your desired prefix

# List of symbols you want to prefix
conflicting_symbols = [
    'Constraint',     # Example class name
    'Conflict',  # Example variable name
    'Path',
    'heuristics_type'  # Example function name
    # Add all the symbols you need to prefix
]

def prefix_symbols_in_files():
    # Collect all .cpp and .h files in the project directory
    source_files = []
    for root, _, files in os.walk(project_dir):
        for file_name in files:
            if file_name.endswith(('.cpp', '.h')):
                file_path = os.path.join(root, file_name)
                source_files.append(file_path)
    
    # For each symbol, replace it with the prefixed version in all files
    for symbol in conflicting_symbols:
        prefixed_symbol = f"{prefix}{symbol}"
        # Regex pattern to match whole words only
        word_pattern = rf'\b{re.escape(symbol)}\b'
        
        for file_path in source_files:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            new_lines = []
            modified = False
            for line in lines:
                # Skip lines that are #include directives
                if re.match(r'^\s*#\s*include', line):
                    new_lines.append(line)
                    continue

                # Replace symbol occurrences in other lines
                new_line = re.sub(word_pattern, prefixed_symbol, line)
                if new_line != line:
                    modified = True
                new_lines.append(new_line)
            
            if modified:
                with open(file_path, 'w') as file:
                    file.writelines(new_lines)
                print(f"Prefixed '{symbol}' to '{prefixed_symbol}' in {file_path}")

# Run the function
if __name__ == "__main__":
    prefix_symbols_in_files()
