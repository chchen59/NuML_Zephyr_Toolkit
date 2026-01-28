NuML_Zephyr_Toolkit
===
### Windows command line tools for Nuvoton machine learning platform base on Zephyr.
## Tools 
* [NuML_TFLM_Tool](NuML_TFLM_Tool/README.md) : Tool for machine learning project generate, build and flash base on TFLM framework
* vela: Arm model compiler for NPU accelerator  
    Reference: https://gitlab.arm.com/artificial-intelligence/ethos-u/ethos-u-vela
* tools: make, flatc and NuLink command tool
* tflite2cpp: tflite model file convert to CPP hearder file
## Install  
1. Python 3.10 environment  
    For conda:  
    ~~~
    conda env create --name myenv python=3.10
    conda activate myenv
    pip install -r requirements.txt
    ~~~  
    For others:  
    ~~~
    pip install -r requirements.txt
    ~~~  

