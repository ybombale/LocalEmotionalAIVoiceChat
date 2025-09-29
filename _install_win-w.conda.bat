@echo off

conda create -y --prefix=./.LocalEmotional python=3.10.9
conda activate ./.LocalEmotional
:: where python

:: Set Python path (adjust this if needed)
set PYTHON_EXE=.\.LocalEmotional\python.exe



echo Installing EmotionalLocalVoiceChat...
setlocal enabledelayedexpansion

:: Set current directory
cd /d %~dp0

echo Starting installation process...

:: Create and activate virtual environment
echo Creating and activating virtual environment...
%PYTHON_EXE% -m venv venv
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install other requirements
echo Installing other requirements...
python -m pip install -r requirements.txt

:: Detect CUDA version
echo Detecting CUDA version...
for /f "tokens=* USEBACKQ" %%F in (`nvcc --version ^| findstr /C:"release"`) do (
    set nvcc_output=%%F
)
echo NVCC Output: !nvcc_output!

if not "!nvcc_output!"=="" (
    echo !nvcc_output! | findstr /C:"11.8" >nul
    if !errorlevel! equ 0 (
        echo CUDA 11.8 detected. Installing PyTorch for CUDA 11.8...
        python -m pip install torch==2.5.1+cu118 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu118
    ) else (
        echo CUDA 12.x detected. Installing PyTorch for CUDA 12.1...
        python -m pip install torch==2.5.1+cu121 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

        # Now Install Deepspeed for python 3.10 / compiled with torch=2.5.1+cuda==12.1
        python -m pip install deepspeed/deepspeed-0.15.2+cuda121-cp310-cp310-win_amd64.whl
    )
) else (
    echo CUDA not detected. Skipping PyTorch CUDA installation.
)

:: Downgrade transformers pip (v4.55.0 also seems to work) ← (Added by YB)
echo Transformers downgrading...
python -m pip install transformers==4.55.4

echo Installation completed.
pause
