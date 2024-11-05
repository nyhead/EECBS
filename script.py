import os
import re

# Define the directory paths and prefix
project_dir = "."
src_dir = os.path.join(project_dir, 'src')
prefix = 'PREFIX_'  # Replace with your desired prefix

# Regular expressions to detect symbols
class_pattern = r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)'
variable_pattern = r'\b([A-Za-z_][A-Za-z0-9_]*)\s+[A-Za-z_][A-Za-z0-9_]*\s*(?:=|;)'
forbidden = ["class", "int", "auto", "bool", "string", "return", "size_t", "uint64_t", "for", "double", "clock_t"]

def add_prefix_to_symbols():
    # Traverse header files and add prefix to detected classes and variables
    for root, dirs, files in os.walk(project_dir):
        for file_name in files:
            if file_name.endswith('.h'):
                file_path = os.path.join(root, file_name)
                
                with open(file_path, 'r') as file:
                    content = file.read()
                
                # Temporarily replace #include lines to skip them during prefixing
                includes = re.findall(r'#include\s+[<"].+[>"]', content)
                content = re.sub(r'#include\s+[<"].+[>"]', "__INCLUDE__", content)

                # Find and replace class names
                class_matches = re.findall(class_pattern, content)
                for class_name in class_matches:
                    if any(class_name.startswith(x) for x in forbidden):
                        continue
                    prefixed_class_name = f"{prefix}{class_name}"
                    content = re.sub(rf'\bclass\s+{class_name}\b', f'class {prefixed_class_name}', content)
                    update_source_files(class_name, prefixed_class_name)
                
                # Find and replace variable definitions (ignoring functions)
                variable_matches = re.findall(variable_pattern, content)
                for var_type in variable_matches:
                    if any(var_type.startswith(x) for x in forbidden):
                        continue
                    prefixed_var_type = f"{prefix}{var_type}"
                    content = re.sub(rf'\b{var_type}\b', prefixed_var_type, content)
                    update_source_files(var_type, prefixed_var_type)
                
                # Restore #include lines
                for include in includes:
                    content = content.replace("__INCLUDE__", include, 1)
                
                with open(file_path, 'w') as file:
                    file.write(content)
                print(f"Processed {file_path}")

def update_source_files(original_symbol, prefixed_symbol):
    # Traverse all source files to replace symbol usages with prefixed versions
    for root, dirs, files in os.walk(src_dir):
        for file_name in files:
            if file_name.endswith('.cpp'):
                file_path = os.path.join(root, file_name)
                
                with open(file_path, 'r') as file:
                    content = file.read()
                
                # Temporarily replace #include lines to skip them during prefixing
                includes = re.findall(r'#include\s+[<"].+[>"]', content)
                content = re.sub(r'#include\s+[<"].+[>"]', "__INCLUDE__", content)
                
                # Replace occurrences of the symbol with the prefixed symbol
                content = re.sub(rf'\b{original_symbol}\b', prefixed_symbol, content)
                
                # Restore #include lines
                for include in includes:
                    content = content.replace("__INCLUDE__", include, 1)
                
                with open(file_path, 'w') as file:
                    file.write(content)
                print(f"Updated {original_symbol} to {prefixed_symbol} in {file_path}")

# Run the prefixing function
add_prefix_to_symbols()
