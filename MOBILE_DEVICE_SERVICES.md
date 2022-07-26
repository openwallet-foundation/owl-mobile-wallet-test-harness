# MOBILE DEVICE SERVICES (Local & Cloud)<!-- omit in toc -->
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
  
## Contents<!-- omit in toc -->

### Summary

There are many devices and device services we wish to support with the Aries Mobile Test Harness. They would not only include cloud services like Sauce Labs and BrowserStack, but also local devices like connected real iOS and Android devices, or Emulators and Simulators running on the local machine or in a container. All of these services have differing ways to do certain actions, like image injection for QR Code scanning, or biometrics handling, or just the way the capabilities are setup are different between them. Running with a local device allows test development and exection without having to pay for and maintain a cloud based device service like Sauce Labs, but will not give you streamlined pipeline exection across varying devices and platforms that services like Sauce Labs provide. 

To simplify the complexity of supporting these device services for a given set of tests, a Device Service Handler interface and factory has been created to obfuscate the specific implementations of these differences from them tests and supporting page objects. 

### Design
```mermaid
classDiagram
   DeviceServiceHandlerInterface <|-- SauceLabsHandler :implements
   DeviceServiceHandlerInterface <|-- LocalDeviceHandler :implements
   LocalDeviceHandler <|-- LocalEmulatorHandler :implements
   LocalDeviceHandler <|-- LocalRealDeviceHandler :implements
   LocalDeviceHandler <|-- LocalSimulatorDeviceHandler :implements
   DeviceServiceHandlerInterface <|-- BrowserStackHandler :implements
   <<proposed>> BrowserStackHandler
   DeviceServiceHandlerInterface <|-- OtherDeviceHandler :implements
   OtherDeviceHandler <|-- OtherVirtualDeviceHandler :implements
   OtherDeviceHandler <|-- OtherRealDeviceHandler :implements
   <<proposed>> BrowserStackHandler
   <<proposed>> OtherDeviceHandler
   <<possible>> LocalEmulatorHandler
   <<possible>> LocalSimulatorDeviceHandler
   <<possible>> LocalRealDeviceHandler
   DeviceServiceHandlerFactory ..> DeviceServiceHandlerInterface :creates
   <<Interface>> DeviceServiceHandlerInterface
  
   AMTH ..> DeviceServiceHandlerFactory :uses

   class DeviceServiceHandlerFactory{
       +create_device_service_handler(device_service_type)DeviceServiceHandlerInterface
   }
   class DeviceServiceHandlerInterface{
        +_platform
       +__init__(config_file:str)
       +set_desired_capabilities(config:dict)
       +intitialize_driver()webdriver
       +inject_qrcode(image)
       +biometrics_authenticate(bool)
       +supports_test_result()bool
       +set_test_result(passed:bool)
   }
   class DeviceServiceMap{
     +SauceLabs:SauceLabsHandler
     +LocalAndroidEmulator:LocalAndroidEmulatorHandler
     +LocalAndroidReal:LocalAndroidRealHandler
     +LocaliOSSimulator:LocaliOSSmulatorHandler
     +LocaliOSReal:LocaliOSRealHandler
   }
    class AMTH{
      +beforeFeature(device_service_type)
    }		
```

### Usage of the Handlers in Tests
Using the device handlers in the test code will be the same no matter which device handler is being used. The handler is assigned to the test run based on the `-d` option on the `./manage run` command of AMTH. This means the same test code can be used for the run command,
```
LEDGER_URL_CONFIG=http://test.bcovrin.vonx.io REGION=us-west-1 ./manage run -d SauceLabs -u <sl user name> -k <sl access key> -p Android -a app-release.aab -i "AATH;http://0.0.0.0:9020" -v "AATH;http://0.0.0.0:9030" -t @T002.1-Proof
```
can be the same as the test code used for this run command,
```
LEDGER_URL_CONFIG=http://test.bcovrin.vonx.io ./manage run -d LocalAndroid -p Android -a /<full local path>/AriesBifold-209.apk -i "AATH;http://0.0.0.0:9020" -v "AATH;http://0.0.0.0:9030" -t @bc_wallet -t @T002.1-Proof
```

The test harness creates an instance of the handler at the start of the test run, and adds it to the Behave `context` object that gets passed around to all the tests. So to call specific functions on the device handler, user the `context.device_service_handler` instance to do so. 

The two biggest differences between handlers are biometrics handling and QR code (image) injection. To call any of these functions at the point it is needed in the test code, it is called as follows,
```python
context.device_service_handler.biometrics_authenticate(True)
```
and
```python
context.device_service_handler.inject_qrcode(image)
```

## Setup
The setup required will be different depending on the device service being used. 

### Setup with Sauce Labs
The user will need a Sauce labs account. If testing includes QR Code scanning, this account will need to be the real device service as it is the only one in Sauce Labs that supports image injection. 

If running the test harness locally with AATH agents acting as issuer and/or verifier when doing test development the Sauce Connect Tunnel will be needed to allow communication with the local agents. 

```bash
docker pull saucelabs/sauce-connect
```
```bash
docker run --rm \
    -e SAUCE_USERNAME=<sl user name> \
    -e SAUCE_ACCESS_KEY=<sl access key> \
    --network="host" \
    -it saucelabs/sauce-connect \
    --user <sl user name> --api-key <sl access key>
    --direct-domains <aries-mediator-agent-test-endpoint>
```
If the wallet under test is using a Mediator agent, there will be a need to add the endpoint to the `--direct-domains` option so that the wallet won't go through the Sauce tunnel to connect to the mediator. That is, unless the mediator is running on your local machine or behind a corporate firewall. 

### Setup with an Local Android Emulator
- Install Android Studio for your platform
- Open Android Studio and open/create a new project
- Open Device Manager under Tools menu
- Create a device or launch an existing emulator
- Install Appium Server
- Start Appium Server
- In AMTH, update the local_android_config.json with the appropriate settings. For Example, here is a set of capabilities that work with the BC Wallet app.
```json
{
  "capabilities": {
    "appPackage": "ca.bc.gov.BCWallet",
    "appium:appActivity": "ca.bc.gov.BCWallet.MainActivity",
    "platformName": "Android",
    "app": "/Users/Shel/Projects/BC.gov/apps/bifold-bc/AriesBifold-209.apk",
    "deviceName": "Android Accelerated Oreo",
    "udid": "emulator-5554",
    "automationName": "UiAutomator2",
    "autoGrantPermissions": true
  }
}
```
- Make sure biometrics (fingerprint is setup in settings) on the emulator
- Set ANDROID_HOME environment variable to the android sdk. For example:
```bash
export ANDROID_HOME=/Users/Shel/Library/Developer/Xamarin/android-sdk-macosx
# system wide do something like this
echo 'export ANDROID_HOME=/Users/Shel/Library/Developer/Xamarin/android-sdk-macosx' >> ~/.zshenv
```
- Edit ${ANDROID_HOME}/emulator/resources/Toren1BD.posters, and add:
```
poster custom
size 1.2 1.2
position 0 -0.1 -1.8
rotation 0.1 0 0
default qrcode.png
```
- You must have the Android emulator PIN security setup in order to do biometrics, do not turn off the PIN, but when you start the emulator, unlock it with the pin before running tests. 
- You must (for now) set the `save_qr_code_on_creation` AMTH option in the `behave.ini` file to `True`

At this point, if a set of tests exist for the wallet under test, the ./manage run command will work with your local Android Emulator. For example, this command will successfully run tests for the BC Wallet, if AATH agents are running. 
```
LEDGER_URL_CONFIG=http://test.bcovrin.vonx.io ./manage run -d LocalAndroid -p Android -a /<full local path>/AriesBifold-209.apk -i "AATH;http://0.0.0.0:9020" -v "AATH;http://0.0.0.0:9030" -t @bc_wallet -t @T009-Proof
```


### Setup with a Real Andoid Device Connected Locally
TBD

### Setup with a Local iOS Simulator
TBD

### Setup with a Real iOS Device Connected Locally
TBD

### Debugging with VS Code
Most of the time for test development, the test developer will want to be running with a Local Device with the Python IDE of choice. The following is an example of getting AMTH running with a Local Device and using VS Code as the IDE. 

#### Setup AMTH locally
Setting up AMTH locally means running the test harness without the provisioning and handling of the `manage` script, and running the test harness outside of its containerized version. To setup locally, installation of the libraries and components that comprise the AMTH. 

If not already installed, install Python 3.7 on your local environment. 

Then `pip install` the following libraries.
```
behave
allure-behave
SauceClient
paver==1.3.4
selenium
psutil==5.7.2
Appium-Python-Client
qrcode[pil]~=6.1
webdriver-manager
python-decouple
aiohttp
```

#### Setup VS Code
Create a launch.json file for your instance of VS Code. See [here](https://code.visualstudio.com/docs/editor/debugging) for more details.

Open the launch.json file created for debugging and add the following section to it. 
```
        {
            "name": "Python: Behave current file",
            "type": "python",
            "request": "launch",
            "module": "behave",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/aries-mobile-tests",
            "env": {
                "SAUCE_USERNAME": <sauce username>,
                "SAUCE_ACCESS_KEY": <sauce access key>,
                "SL_REGION": "us-west-1",
                "DEVICE_CLOUD": "LocalAndroid"
            },
            "args": [
                "${file}",
                "--tags=@T002-Proof",
                "-k",
                "-D",
                "Issuer=AATH;http://0.0.0.0:9020",
                "-D",
                "Verifier=AATH;http://0.0.0.0:9030"
            ]
        },
```

This configuration sets up expected environment variables, launches behave directly and sends in expected behave arguments.

The key environment variable here is the `DEVICE_CLOUD`, setting it to `LocalAndroid` tells the test harness to use a local android emulator. the SAUCE* environment variables can be removed/ignored here, but they could be used here to do test debugging with Sauce Labs Devices instead of a local device. 

The `args` are behave arguments as the `manage` script would pass to behave. Setup the tags that point to the tests you want to run, and set the issuer and verifier to your preferred services. 

With this setup you will need to have the feature file of the test(s) you wish to run in view when you select debug. 

#### Working with a Local Device
The last step in getting the local device working with VS Code is to edit the AMTH config.json file, setting the capabilities to the appropriate settings. For example, this configuration works with the BC Wallet with a local running Android emulator.
```
{
  "capabilities": {
    "appPackage": "ca.bc.gov.BCWallet",
    "appium:appActivity": "ca.bc.gov.BCWallet.MainActivity",
    "platformName": "Android",
    "app": "/Users/Shel/Projects/BC.gov/apps/bifold-bc/AriesBifold-209.apk",
    "deviceName": "Android Accelerated Oreo",
    "udid": "emulator-5554",
    "automationName": "UiAutomator2",
    "autoGrantPermissions": true
  }
}
```
If using tests to scan a QR code, set the `autoGrantPermissions` to `true`, this will accept the devices prompt to allow camera access for the app.


### Creating a New Handler for a Device Service
To create a new handler for another cloud device service like BrowserStack, AWS, etc, or a new local device handler for iOS (which is currently not implemeted), follow the patterns laid out by the `local_android_handler.py` and `sauce_labs_handler.py` in `device_service_handler`. In short it requries the implementation of the `device_service_handler_interface` as documented in the class diagram above.

### CONFIG_FILE_OVERRIDE for bypassing default cababilities
TBD