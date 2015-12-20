# replicants

Library to mock different devices running various network operating systems.

# Usage

The library has two modes:

 * record - This mode is not going to mock the device but it's going to patch the library of the device to record every interaction with the device. This will be useful later when you want to mock the device for real.
 * play - This mode is going to mock the device and simulate being the device using the mocked data.
 
 
The library is going to use the environment variable ```REPLICANTS_FOLDER``` to store/read the mocked data.

# Examples

Check the examples inside the ```examples``` folder. There are several examples for the different supported devices. Feel free to use the vagrant boxes provided inside the folder ```test/unit/vagrant```, then you can delete the subfolders inside each OS-specific subfolder and run the ```record_*``` examples before the ```play_*``` examples.
