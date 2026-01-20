NuML_Toolkit
===
### Windows tools for Nuvoton machine learning base on Zephyr platform.
## Tools 
* [NuML_TFLM_Tool](NuML_TFLM_Tool/README.md) : Tool for machine learning project generate, build and flash base on TFLM framework
* vela: Arm model compiler for NPU accelerator  
    Reference: https://gitlab.arm.com/artificial-intelligence/ethos-u/ethos-u-vela
* tools: make, flatc and NuLink command tool
* tflite2cpp: tflite model file convert to CPP hearder file
## Install  
1. Python 3.8 environment  
    For conda:  
    ~~~
    conda env create --file conda\environment.yml
    ~~~  
    For others:  
    ~~~
    pip install -r requirements.txt
    ~~~  

