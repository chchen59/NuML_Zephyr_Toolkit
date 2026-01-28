import os
import re
import shutil
import subprocess

def add_flash_parser(subparsers, _):
    """Include parser for 'flash' subcommand"""
    parser = subparsers.add_parser("flash", help="flash binary code")
    parser.set_defaults(func=project_flash)
    parser.add_argument("--workspace_path", help="specify zephyr workspace path")
    parser.add_argument("--build_path", help="specify project build path")

def project_flash(args):
    workspace_path = args.workspace_path
    workspace_path = os.path.abspath(workspace_path)
    build_dir = args.build_path

    cur_work_dir = os.getcwd()
    os.chdir(workspace_path)

    print("Build directory at: ", build_dir)
    print("Using workspace path: ", workspace_path)

    flash_cmd = ['west', 'flash', '-d', build_dir]

    ret = subprocess.run(flash_cmd, shell=True)
    if ret.returncode == 0:
        print('flash MCU done')
    else:
        print('unable flash MCU')
        return 7

    os.chdir(cur_work_dir)
    return 0