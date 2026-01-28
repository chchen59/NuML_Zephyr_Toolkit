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
2. Install Zephyr dependence window tools  
    a. Open a Command Prompt(cmd.exe) or PowerShell terminal window. Press the Windows key, type ```cmd.exe``` or PowerShell and click on thre result.  
    b. Use winget to install the required dependencies:
    ~~~
    winget install Kitware.CMake Ninja-build.Ninja oss-winget.gperf Git.Git oss-winget.dtc wget 7zip.7zip
    ~~~
3. Setup Zephyr workspace including Zephyr source, toolchain and Python dependence packages.
    ~~~
    python setup_zephyr.py
    ~~~


