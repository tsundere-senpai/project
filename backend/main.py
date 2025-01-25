from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional 
import docker
import uuid
import os
import time
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
client = docker.from_env()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

# Define request body structure
# class CodeSubmission(BaseModel):
#     language: str
#     code: str

LANGUAGE_CONFIG = {
    "python": {"image": "python:3.8", "cmd": "python3"},
    "cpp": {"image": "gcc:latest", "cmd": "g++ -o main"},
    "java": {"image": "openjdk:latest", "cmd": "javac"},
    "c":{"image": "gcc:latest", "cmd": "gcc -o main"},
}
 
class CodeSubmission(BaseModel):
    language: str
    code: str
    stdin: Optional[str] = None  # New field for standard input

@app.post("/submit")
def submit_code(submission: CodeSubmission):
    language = submission.language
    code = submission.code
    stdin_input = submission.stdin 
     # Capture stdin input from frontend

    if language not in LANGUAGE_CONFIG:
        raise HTTPException(status_code=400, detail="Unsupported language")

    container_id = str(uuid.uuid4())
    tmp2_dir = "/tmp"  # Explicitly using host-mounted /tmp

    code_file = f"{container_id}.code"
    input_file = f"{container_id}.input"
    file_path = os.path.join(tmp2_dir, code_file)
    input_path = os.path.join(tmp2_dir, input_file)

    with open(file_path, "w") as f:
        f.write(code)
    if stdin_input:
        with open(input_path, "w") as f:
            f.write(stdin_input)

    try:
        config = LANGUAGE_CONFIG[language]
        container = client.containers.run(
            image=config["image"],
            command = f"/bin/sh -c 'echo \"{stdin_input}\" | {config['cmd']} /tmp/{code_file}'" if stdin_input else f"/bin/sh -c '{config['cmd']} /tmp/{code_file}'",
            volumes={tmp2_dir: {'bind': '/tmp', 'mode': 'rw'}},
            working_dir="/tmp",
            stdin_open=True,
            tty=True,
            detach=True
        )

        container.wait()
        result = container.logs().decode().strip()
        container.remove(force=True)

    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # Clean up

    return {"output": result}

# @app.post("/submit/")
# def submit_code(submission: CodeSubmission):
#     language = submission.language
#     code = submission.code
#     print("check1:" + code)

#     if language not in LANGUAGE_CONFIG:
#         raise HTTPException(status_code=400, detail="Unsupported language")

#     container_id = str(uuid.uuid4())
#     tmp2_dir = "/tmp"  # Explicitly using host-mounted /tmp

#     code_file = f"{container_id}.code"
#     file_path = os.path.join(tmp2_dir, code_file)

    
#     with open(file_path, "w") as f:
#         f.write(code)

#     # time.sleep(1) 

#     if not os.path.exists(file_path):
#         raise Exception(f"File {file_path} was not created!")
#     else:
#         print(f"File was created: {file_path}")

#     try:
#         config = LANGUAGE_CONFIG[language]
#         print(f"Host file path: {file_path}")
#         print(f"Directory being mounted: {tmp2_dir}")
#         print(f"Expected container path: /tmp/{code_file}")
#         if(language == "python"):
#             container = client.containers.run(
#                 image=config["image"],
#                 # command=f"/bin/sh -c 'ls /tmp && cat /tmp/{code_file}'",
#                 command=f"/bin/sh -c '{config['cmd']} /tmp/{code_file}'",
#                 volumes={tmp2_dir: {'bind': '/tmp', 'mode': 'rw'}},
#                 working_dir="/tmp",
#                 mem_limit="128m",
#                 cpu_period=100000,
#                 cpu_quota=50000,
#                 network_disabled=True,
#                 detach=True,
#                 stdin_open=True,  # Allow standard input
#                 tty=True          # Allocate a pseudo-TTY for interactive mode
#             )
#             container.wait() 
#             result = container.logs().decode().strip()
#             container.remove(force=True)
#         elif(language == "cpp"):
#             code_file=f"{container_id}.cpp"
#             file_path2 = os.path.join(tmp2_dir, code_file)
#             with open(file_path2, "w") as f:
#                 f.write(code)
#             container = client.containers.run(
#                 image=config["image"],
#                 command=f"/bin/sh -c '{config['cmd']} /tmp/{code_file} && ./main'",
#                 volumes={tmp2_dir: {'bind': '/tmp', 'mode': 'rw'}},
#                 working_dir="/tmp",
#                 mem_limit="128m",
#                 cpu_period=100000,
#                 cpu_quota=50000,
#                 network_disabled=True,
#                 detach=True
#             )
#             container.wait() 
#             result = container.logs().decode().strip()
#             container.remove(force=True)
#             time.sleep(0.1)
#             # os.remove(file_path2)
#             # os.remove("/tmp/main")
#         elif(language == "java"):
#             code_file=f"{container_id}.java"
#             file_path2 = os.path.join(tmp2_dir, code_file)
#             with open(file_path2, "w") as f:
#                 f.write(code)
#             container = client.containers.run(
#                 image=config["image"],
#                 # command=f"/bin/sh -c 'ls /tmp && cat /tmp/{code_file}'",
#                 command=f"/bin/sh -c '{config['cmd']} /tmp/{code_file} && ls /tmp'",
#                 volumes={tmp2_dir: {'bind': '/tmp', 'mode': 'rw'}},
#                 working_dir="/tmp",
#                 mem_limit="128m",
#                 cpu_period=100000,
#                 cpu_quota=50000,
#                 network_disabled=True,
#                 detach=True
#             )
#             container.wait() 
#             result = container.logs().decode().strip()
#             container.remove(force=True)
#             os.remove(file_path2)
#         elif(language == "c"):
#             code_file=f"{container_id}.c"
#             file_path2 = os.path.join(tmp2_dir, code_file)
#             with open(file_path2, "w") as f:
#                 f.write(code)
#             container = client.containers.run(
#                 image=config["image"],
#                 # command=f"/bin/sh -c 'ls /tmp && cat /tmp/{code_file}'",
#                 command=f"/bin/sh -c '{config['cmd']} /tmp/{code_file} && ./main'",
#                 volumes={tmp2_dir: {'bind': '/tmp', 'mode': 'rw'}},
#                 working_dir="/tmp",
#                 mem_limit="128m",
#                 cpu_period=100000,
#                 cpu_quota=50000,
#                 network_disabled=True,
#                 detach=True
#             )
#             container.wait() 
#             result = container.logs().decode().strip()
#             container.remove(force=True)
#             time.sleep(0.1)
#             # os.remove(file_path2)
#             # os.remove("/tmp/main")

#         # container.wait() 
#         # result = container.logs().decode().strip()
#         # container.remove(force=True)
#         print("check3: " + result)
#     except Exception as e:
#         print("check2: " + str(e))
#         return {"error": str(e)}
#     # time.sleep(0.5)
#     finally:
#         os.remove(file_path)  # Clean up the file
#     return {"output": result}

# @app.post("/submit/")
# def submit_code(submission: CodeSubmission):
#     language = submission.language
#     code = submission.code
#     print("check1:" + code)

#     if language not in LANGUAGE_CONFIG:
#         raise HTTPException(status_code=400, detail="Unsupported language")

#     container_id = str(uuid.uuid4())
#     tmp_dir = "/tmp"
    
#     # Construct the file path
#     filename = f"{container_id}.cpp" if language == "cpp" else f"{container_id}.py"
#     file_path = os.path.join(tmp_dir, filename)

#     # Write to the file
#     with open(file_path, "w") as f:
#         f.write(code)

#     time.sleep(1)  # Wait for the file to be written

#     if not os.path.exists(file_path):
#         raise Exception(f"File {file_path} was not created!")
#     else:
#         print(f"File was created: {file_path}")

#     try:
#         config = LANGUAGE_CONFIG[language]
#         container = client.containers.run(
#             image=config["image"],
#             command=f"/bin/sh -c '{config['cmd'].format(filename=filename)}'",
#             volumes={tmp_dir: {'bind': '/tmp', 'mode': 'rw'}},
#             working_dir="/tmp",
#             mem_limit="128m",
#             cpu_period=100000,
#             cpu_quota=50000,
#             network_disabled=True,
#             detach=True
#         )
#         container.wait()  # Wait for the container to finish execution
#         result = container.logs().decode().strip()
#         print("check3: " + result)
#     except Exception as e:
#         print("check2: " + str(e))
#         return {"error": str(e)}

#     return {"output": result}
