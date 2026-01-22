import argparse
import logging
import sys
import os
import pathlib
import shutil
import subprocess

from generic_codegen.generic_codegen import GenericCodegen

PROJECT_GEN_DIR_PREFIX = 'ProjGen_'

board_list = [
    #board name, zephry baoard name, MCU
    ['NuMaker-M55M1', 'numaker-m55m1', 'M55M1'],   
    ['NuGestureAI-M55M1', 'numaker_gai_m55m1', 'M55M1'],   
]

application = {
    "generic"   : {
                    "board": ['NuMaker-M55M1', 'NuGestureAI-M55M1'],
                    "example_tmpl_dir": "generic_template",
                    "example_tmpl_proj": "NN_ModelInference"
                  },
    "imgclass"  : {
                    "board": ['NuMaker-M55M1', 'NuGestureAI-M55M1'],
                    "example_tmpl_dir": "imgclass_template",
                    "example_tmpl_proj": "NN_ImgClassInference"
                  },
    "objdet"    : {
                    "board": ['NuMaker-M55M1'],
                    "example_tmpl_dir": "objdet_template",
                    "example_tmpl_proj": "NN_ObjDetInference"
                  },
    "objdet_yolox"    : {
                    "board": ['NuMaker-M55M1', 'NuGestureAI-M55M1'],
                    "example_tmpl_dir": "objdet_yolox_template",
                    "example_tmpl_proj": "NN_ObjDetInference"
                  },
}

# add project generate argument parser
def add_generate_parser(subparsers, _):
    """Include parser for 'generate' subcommand"""
    parser = subparsers.add_parser("generate", help="generate ml project")
    parser.set_defaults(func=project_generate)
    parser.add_argument("--model_file", help="specify tflte file", required=True)
    parser.add_argument("--output_path", help="specify output file path", required=True)
    parser.add_argument("--board", help="specify target board name", required=True)
    parser.add_argument("--templates_path", help="specify template path")
    parser.add_argument("--zephyrproject_path", help="specify zephyr project path")
    parser.add_argument("--model_arena_size", help="specify the size of arena cache memory in bytes", default='0')
    parser.add_argument("--vela_extra_option", help="specify vela extra options")
    parser.add_argument("--application", help="specify application scenario generic/imgclass/objdet/objdet_yolox", default='generic')

# INT8 model compile by vela
def model_compile(board_info, output_path, vela_dir_path, model_file, model_arena_size, extra_option):
    cur_work_dir = os.getcwd()
    os.chdir(output_path)
    vela_exe = os.path.join(vela_dir_path, 'vela-4_0_1.exe')    
    vela_conf_file = os.path.join(vela_dir_path, 'default_vela.ini')
    vela_conifg_option = '--config='+vela_conf_file
    print(output_path)
    print(vela_conifg_option)
    print(model_file)
    print(model_arena_size)
    print(vela_exe)

    vela_cmd = [vela_exe, model_file, '--accelerator-config=ethos-u55-256', '--optimise=Performance', vela_conifg_option, '--memory-mode=Shared_Sram', '--system-config=Ethos_U55_High_End_Embedded', '--output-dir=.']

    if int(model_arena_size) > 0:
        vela_cmd.extend(['--arena-cache-size', model_arena_size])

    if extra_option != None:
        print(extra_option)
        extra_option_parts = extra_option.split()
        vela_cmd.extend(extra_option_parts)

    print(vela_cmd)
    ret =subprocess.run(vela_cmd)
    if ret.returncode == 0:
        print('vela compile done')
    else:
        print('Unable compile failee')
        return False

    os.chdir(cur_work_dir)
    return True

#parse vela summary file to get memory usage information
def vela_summary_parse(summary_file):
    usecols = ['sram_memory_used', 'off_chip_flash_memory_used']
    df = pandas.read_csv(summary_file, usecols=usecols)
    return df.iloc[0,0]*1024, df.iloc[0,1]*1024 

#generate tflite cpp file
def generate_model_cpp(output_path, tflite2cpp_dir_path, model_file):
    cur_work_dir = os.getcwd()
    print(cur_work_dir)
    os.chdir(output_path)
    model2cpp_exe = os.path.join(tflite2cpp_dir_path, 'gen_model_cpp.exe')
    template_dir = os.path.join(tflite2cpp_dir_path, 'templates')
    model2cpp_cmd = [model2cpp_exe, '--tflite_path', model_file, '--output_dir','.', '--template_dir', template_dir, '-ns', 'arm', '-ns', 'app', '-ns', 'nn']   
    print(model2cpp_cmd)

    ret =subprocess.run(model2cpp_cmd)
    if ret.returncode == 0:
        print('tflite2cpp done')
    else:
        print('Unable generate cpp')
        return False

    os.chdir(cur_work_dir)
    return True

def prepare_proj_resource(board_info, project_path, templates_path, vela_model_file, vela_model_cc_file, example_tmpl_dir, example_tmpl_proj):
    print('copy resources to autogen project directory')

    example_patch_src_path = os.path.join(templates_path, board_info[2], 'patch')
    example_dest_path = os.path.join(project_path, board_info[2])
    print(example_dest_path)
    print(example_patch_src_path)

    example_template_path = os.path.join(templates_path, board_info[2], board_info[0], example_tmpl_dir)
    example_project_path = os.path.join(example_dest_path, 'SampleCode')
    example_project_src_path = os.path.join(example_template_path, example_tmpl_proj)

    print(example_template_path)
    print(example_project_src_path)
    print(example_project_path)

    if os.path.exists(example_patch_src_path):
        print('copy example patch to autogen project directory')
        shutil.copytree(example_patch_src_path, example_dest_path, dirs_exist_ok = True)

    print('copy example template project to autogen project directory')
    example_project_path = os.path.join(example_project_path, example_tmpl_proj)
    shutil.copytree(example_project_src_path, example_project_path, dirs_exist_ok = True)

    example_project_model_cpp_file = os.path.join(example_project_path, 'src', 'Model', 'NN_Model_INT8.tflite.cpp')
    example_project_model_dir = os.path.join(example_project_path, 'src', 'Model')
    shutil.copyfile(vela_model_cc_file, example_project_model_cpp_file)
    shutil.copy(vela_model_file, example_project_model_dir)

    return example_project_path

#project generate main function
def project_generate(args):
    templates_path = args.templates_path 
    zephyrproject_path = args.zephyrproject_path
    application_usage = args.application

    if not application_usage in application:
        print("applicaiton not found! using generic instead")
        application_usage = "generic"

    application_param = application[application_usage]

    if templates_path == None:
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')

    if zephyrproject_path == None:
        zephyrproject_path = os.path.join(os.path.dirname(__file__), '..', 'zephyrproject')

    print("Using templates path: ", templates_path)
    print("Using zephyrproject path: ", zephyrproject_path)

    board_found = False

    for board_info in board_list:
        if board_info[0] == args.board:
            for supported_board in application_param["board"]:
                if supported_board == args.board:
                    board_found = True
                    break
        if board_found == True:
            break

    if board_found == False:
        print("board not support")
        return 'unable_generate'

    #create ouput directory, if output directory is not exist
    if not os.path.exists(args.output_path):
        os.mkdir(args.output_path)

    #generated project directory
    project_path = os.path.join(args.output_path, PROJECT_GEN_DIR_PREFIX + args.board)
    if not os.path.exists(project_path):
        os.mkdir(project_path)

    print("Generating project in ", project_path)

    #model compile by vela
    arena_size = args.model_arena_size
    vela_dir_path = os.path.join(os.path.dirname(__file__), '..', 'vela')

    """ temp del for testing
    """
    ret = model_compile(board_info, args.output_path, vela_dir_path, os.path.abspath(args.model_file), arena_size, args.vela_extra_option)
    if ret == False:
        return 'unable_generate'

    vela_model_basename = os.path.splitext(os.path.basename(args.model_file))[0]
    vela_model_file_path = os.path.join(args.output_path, vela_model_basename + '_vela.tflite')
    vela_summary_file_path = os.path.join(args.output_path, vela_model_basename + '_summary_Ethos_U55_High_End_Embedded.csv')
    print(vela_model_file_path)

    #generate model cc file
    tflite2cpp_dir_path = os.path.join(os.path.dirname(__file__), '..', 'tflite2cpp')
    print(tflite2cpp_dir_path)
    generate_model_cpp(args.output_path, tflite2cpp_dir_path, os.path.abspath(vela_model_file_path)) 
    vela_model_cc_file = os.path.join(args.output_path, vela_model_basename + '_vela.tflite.cc')
    print(vela_model_cc_file)

    #prepare project resource
    example_tmpl_dir = application_param["example_tmpl_dir"]
    example_tmpl_proj = application_param["example_tmpl_proj"]

    project_example_path = prepare_proj_resource(board_info, project_path, templates_path, vela_model_file_path, vela_model_cc_file, example_tmpl_dir, example_tmpl_proj)
    print(project_example_path)

    # Generate model.hpp/cpp or main.cpp
    if application_usage == 'generic':
        codegen = GenericCodegen.from_args(vela_model_file_path, project_example_path, vela_summary_file_path, app='generic')

    codegen.code_gen()

    os.remove(vela_model_file_path)
    os.remove(vela_model_cc_file)

    print(f'Example project completed at {os.path.abspath(project_example_path)}')
    return project_example_path
