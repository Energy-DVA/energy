*** Fall 2022 - CSE6242 Data and Visual Analytics Project***
*** Kansas Oil and Gas Exploration and Forecasting ***
*** Team 29: Efrain Rodriguez, Nikhil Kanoor, Geetak Ingle, Jagath Jonnalagedda, Oscar Cortez, Sheena Abraham​ ***

1) DESCRIPTION
This package contains Team 29's project submission. It contains the Final Report, Project Poster, and the source code for a Web Application that allows users to explore and predict the Oil and Gas Production for the state of Kansas. Refer to the Final Report for more details

The DOC folder contains all the documentation. It contains the Final Report and the Poster

The CODE folder contains all the source code that is required to run the Web App. Follow the INSTALLATION section below to setup the environment and data files. The source code is split into many folders and files for easier development, but the entry point for the app is through 'index.py'. Any execution of the Web App requires execution through this CODE folder

2) INSTALLATION
This procedure assumes an Anaconda distribution is installed on the machine. If not, please first install the appropriate Anaconda distribution from 
https://www.anaconda.com/products/distribution prior to following the instruction below

The following procedure will walk the user through the setup of the conda environment and download of the required database file for the Web Application. 

The base folder for the Web App setup will be the accompanying 'CODE' folder. Please use this whenever 'base folder' or 'CODE folder' is mentioned

    1. Download the required SQLite database file 'kansas_oil_gas.db' from https://u.pcloud.link/publink/show?code=XZqCUhVZ06tGAN7yeC8CtNr3oe1TyXSSoVc7

    2. Place the downloaded 'kansas_oil_gas.db' file into filepath 'CODE/data/' and verify that it's size is approximately 1.85 GB
    
    3. Start a Command Prompt/Terminal and navigate to 'CODE' folder path

    4. Run the command "conda env create -f environment.yml" in the Command Prompt/Terminal
        - This installs the required Python Packages in a new conda environment called 'dva_team29'
    
    5. Ensure all packages have installed successfully
    
    6. Run the command "activate dva_team29" in the Command Prompt/Terminal and ensure the environment 'dva_team29' activates successfully

The environment is now ready for execution

3) EXECUTION
The Web App is built upon the Dash framework. As such, a Flask Server first needs to be initialized that serves the Web App. Use the instructions below to start-up the Web App. Please ensure all INSTALLATION steps above have been completed.

    1. Start a Command Prompt/Terminal and navigate to 'CODE' folder path

    2. Run the command "activate dva_team29" in the Command Prompt/Terminal to run the environment

    3. Run the command "python -m index" to initialize the Web App. Wait until you see the message 'Running on http://127.0.0.1:8888' 

    4. Open your favorite web browser (Chrome, Firefox, etc.) and enter the link 'http://127.0.0.1:8888' and press Enter
    
The Web Application has now successfully been served on 'localhost' at port 8888 and is ready for use.


4) DEMO VIDEO
See video located at LINKLINKLINKLINKLINKLINKLINK for a demo on installation and execution of the Web Application