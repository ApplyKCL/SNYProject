# Ultrasound Transducer Build Tracker - UI design

This is Application module - UI part.

### Setup enviroment for PyQt5 and QtDesginer
#### 1. Install Pycharm and activite Pycharm
The first step is to install Pycharm into your computer. You can use [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/) to manage all IDLE you installed. As we are Dalhousie students, we don't need activation code.\
But don't forget [register account](https://www.jetbrains.com/shop/eform/students) through Dal email.

#### 2. Install Anaconda platform
[Anaconda](https://www.anaconda.com/products/distribution) is a powerful open source package platform which allows you to download any version and any type of open-source packages. \
Please download it through the link. 

### Be careful, when you entered `Advanced Options` click `Add Anaconda3 to the system PATH enviroment variable` as well !!!

Also anaconda support different enviorments of python which means you also don't need to download python individually.\
After you finished downloading, please check you have `Anaconda Prompt (anaconda3)` through windowns search.

#### 3. Setup enviroment of PyCharm
- Create a new project.
- Choose Conda as New enviroment using. 
- Set Python version as 3.7.
- Click Create

After you create a new project, click python packages on the bottom line. Search for PyQt5, you should see Pypi has this package,\
click on that and install it. It will pop up a warning that Pycharm failed installation. Don't worry that is what we need. \
Click on the detail of failure. In the Troubleshooting steps, Pycharm already give you cmdlet to help you to fix this issue.\
copy the first line of code to somewhere. Then open `Commands Prompt` paste the code you copied earlier. 
```
conda activate C:\Users\ch243\anaconda3\envs\pythonProject1
```
It will shows that you entered in
```
(pythonProject1) C:\Users\ch243>
```
You may have different project and address names with me. That's fine. Enter the code below to install the PyQt and tools.
```
pip install PyQt5
pip install PyQt5-tools
```
Hoooo... You are almost there. Now follow the link I attached to setup the [External Tools](https://blog.csdn.net/qiqiqi20/article/details/123700108). You can start from No.2 Qt Designer and PyUIC.
You can click on this [Link](https://blog.csdn.net/qq_55957975/article/details/117709038) to set up PyRcc.
- Qt Designer is a application to create UI files
- PyUIC work on translating the UI file made by QT designer to Python code
- Pyrcc to transfer the resource files that you used in UI to a Python code

Congratulation! You are finished on enviorment setting. Now you can start your UI design project. 
#### Good luck! Have fun!

By the way, I also uploaded my file into `Github`, please downloaded it for further design project.