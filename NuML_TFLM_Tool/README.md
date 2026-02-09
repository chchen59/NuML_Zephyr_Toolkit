NuML_TFLM_Tool
===
### Machine learning MCU project generate, build and flash utility. Base on TFLM and Zephyr framework. 
## Support list
* Board 
    1. NuMaker-M55M1
    2. NuGestureAI-M55M1
## Usage
* Generate
    ~~~
    python numl_zephyr_tool.py generate --model_file ..\models\vww4_128_128_INT8.tflite --board NuMaker-M55M1 --output_path ..\NuML_Gen
    ~~~  
    * Parameter  
        * model_file: A quantized tflite model. You can refer to the [NuEdgeWise](https://github.com/OpenNuvoton/NuEdgeWise) tutorial to train your model. The "models\vww4_128_128_INT8.tflite" file is only for testing.
        * board: Supported board name  
            * NuMaker_M55M1
            * NuGestureAI-M55M1
        * output_path: Ouput folder path of generated project
        * application [option]: Specify application scenario
            * generic - default
            * imgclass (MobileNetV2)
            * objdet (YOLOv8n 256x256/224x224/192x192) 
            * objdet_yolox (YOLOX-nano) 
        * model_arena_size [option]: Specify the size of arena cache memory in bytes
* Build
    ~~~
    python numl_zephyr_tool.py build --project_path ..\NuML_Gen\ProjGen_NuMaker_M55M1\SampleCode\NN_ModelInference --workspace_path ..\zephyrproject
    ~~~
    * Parameter
        * project_path: Generated project folder path
        * workspace_path: Zephyr workspace path 
* Flash
    ~~~
    python numl_zephyr_tool.py flash --workspace_path ..\zephyrproject --build_path ..\NuML_Gen\ProjGen_NuMaker-M55M1\SampleCode\NN_ModelInference\build
    ~~~
    * Parameter
        * workspace_path: Zephyr workspace path
        * build_path: Build folder path of generated project
* Deploy
    ~~~
    python numl_zephyr_tool.py deploy --output_path ..\NuML_Gen --board NuMaker-M55M1 --workspace_path ..\zephyrproject --model_file ..\models\vww4_128_128_INT8.tflite
    ~~~
    * Parameter
        * model_file: A quantized tflite model. You can refer to the [NuEdgeWise](https://github.com/OpenNuvoton/NuEdgeWise) tutorial to train your model. The "models\vww4_128_128_INT8.tflite" file is only for testing.
        * board: Supported board name  
            * NuMaker_M55M1
            * NuGestureAI-M55M1
        * output_path: Ouput directory path of generated project
        * workspace_path: Zephyr workspace path  
## Example
~~~
python numl_zephyr_tool.py generate --output_path ..\NuML_Gen --board NuMaker-M55M1 --model_file ..\models\vww4_128_128_INT8.tflite
python numl_zephyr_tool.py build --project_path ..\NuML_Gen\ProjGen_NuMaker-M55M1\SampleCode\NN_ModelInference --board NuMaker-M55M1 --workspace_path ..\zephyrproject
python numl_zephyr_tool.py flash --workspace_path ..\zephyrproject --build_path ..\NuML_Gen\ProjGen_NuMaker-M55M1\SampleCode\NN_ModelInference\build
~~~
or
~~~
python numl_zephyr_tool.py deploy --output_path ..\NuML_Gen --board NuMaker-M55M1 --workspace_path ..\zephyrproject --model_file ..\models\vww4_128_128_INT8.tflite
~~~
