# RAYN Vision System Analytics

![Screenshot of the RVS-A user interface](img/RVS-A_interface_example.png)

## Description
RAYN Vision System (RVS) Analytics is an open-source application for the processing
and analysis of hyper- and multispectral images from multiple sources, including RVS Cameras
online in the same network. It is based on [PlantCV](https://github.com/danforthcenter/plantcv),
an open-source image analysis software package targeted for plant phenotyping.

## Usage
Analyse hyper/multispectral images using PlantCV workflows in a graphical user interface. The application
provides different dialogues to e.g. select image source, regions of interest as well as masks 
in a graphical user interface.

Please refer to the [User Guide]() for more details.

## Setup
It is recommended to run the application in a virtual environment.
Required libraries and versions:
- python v3.10
- plantCV
- jupyterlab
- ipympl
- nodejs
- stackprinter
- paho-mqtt
- plotly
- watchdog
- kaleido (v0.1.0, other versions do not work)
- pyside6

Here are the steps to set up everything to run the application using conda.

```bash
conda create -n rvs python=3.10 # create virtual environment named "rvs" with python v3.10
conda activate rvs # activate virtual environment
conda install --channel=conda-forge plantcv plotly jupyterlab ipympl nodejs stackprinter paho-mqtt plotly watchdog
pip install kaleido==0.1.0
pip install pyside6
```
You can run the application from the repository with the following command:
```bash
conda activate rvs # activate environment
cd PATH/TO/REPOSITORY # navigate to the repository
cd Application # enter Application folder - important for relative paths
python cameraapp.py
```

## Support
If you experience any problems or have feedback on the analysis scripts, please add an issue to this repository or 
contact [RAYN Vision Support](mailto:RAYNVisionSupport@rayngrowingsystems.com).

## Contributing
Whether it's fixing bugs, adding functionality to existing features or adding entirely new features, we welcome 
contributions.

Please add any suggestions/issues/bugs as issues in the [RVS Analytics Repository](https://github.com/rayngrowingsystems/RVS_Analytics/issues).

## License and Copyright
© 2024 RAYN Growing Systems, All Rights Reserved. Licensed under the Apache License, Version 2.0

Trademark and patent info: [rayngrowingsystems.com/ip](https://rayngrowingsystems.com/ip/) \
Third-party license agreement info: [etcconnect.com/licenses](https://www.etcconnect.com/licenses/). \
Product and specifications subject to change.

