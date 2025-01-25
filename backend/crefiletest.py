import os

tmp2_dir = os.path.abspath("tmp3")  # Ensure absolute path
if not os.path.exists(tmp2_dir):
    os.makedirs(tmp2_dir)  # Create the directory if it doesn't exist

# Construct the file path
code_file = "test.code"
file_path = os.path.join(tmp2_dir, code_file)
code="testing"
# Write to the file
with open(file_path, "w") as f:
    f.write(code)

# time.sleep(1)  # Wait for the file to be written

if not os.path.exists(file_path):
    raise Exception(f"File {file_path} was not created!")
else:
    print(f"File was created: {file_path}")
