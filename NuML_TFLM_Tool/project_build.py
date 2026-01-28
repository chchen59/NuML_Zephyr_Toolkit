import os
import re
import shutil
import subprocess

board_list = [
    #board name, zephry baoard name, MCU
    ['NuMaker-M55M1', 'numaker_m55m1', 'M55M1'],   
    ['NuGestureAI-M55M1', 'numaker_gai_m55m1', 'M55M1'],   
]

def find_files_with_extension(directory, extension):
    result = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            result.append(filename)
    return result

def add_build_parser(subparsers, _):
    """Include parser for 'build' subcommand"""
    parser = subparsers.add_parser("build", help="build ml project")
    parser.set_defaults(func=project_build)
    parser.add_argument("--project_path", help="specify prjoect path", required=True)
    parser.add_argument("--workspace_path", help="specify zephyr workspace path")
    parser.add_argument("--board", help="specify target board name", required=True)

def project_build(args):
    project_path = args.project_path
    project_path = os.path.abspath(project_path)
    workspace_path = args.workspace_path
    workspace_path = os.path.abspath(workspace_path)
    build_path = os.path.join(project_path, 'build')

    for board_info in board_list:
        if board_info[0] == args.board:
            board_found = True
            break

    if board_found == False:
        print("board not support")
        return 'unable_generate'

    cur_work_dir = os.getcwd()
    os.chdir(workspace_path)

    print("Building project at: ", project_path)
    print("Using workspace path: ", workspace_path)

    dtc_files = find_files_with_extension(project_path, '.overlay')
    print("DTC overlay files: ", dtc_files)

    build_cmd = ['west', 'build', '-b', board_info[1], project_path, '-d', build_path]

    dtc_overlap_files_str = '-DDTC_OVERLAY_FILE=\"'

    if dtc_files:
        for dtc_file in dtc_files:
            dtc_overlap_files_str += dtc_file + ';'
        dtc_overlap_files_str = dtc_overlap_files_str.strip() + '\"'
        build_cmd.extend(['--', dtc_overlap_files_str])

    build_cmd = ' '.join(build_cmd)
    print("Build command: ", build_cmd)

    ret = subprocess.run(build_cmd, shell=True)
    if ret.returncode == 0:
        print("Build completed successfully.")
    else:
        print("Build failed.")

    binary_path = os.path.join(build_path, 'zephyr', 'zephyr.bin')
    if os.path.exists(binary_path):
        print("Binary file located at: ", binary_path)
        os.chdir(cur_work_dir)
        return build_path
    else:
        print("Binary file not found.")
        os.chdir(cur_work_dir)
        return None
