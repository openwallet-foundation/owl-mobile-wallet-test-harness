# Working with the MWTH Dev Container<!-- omit in toc -->

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## Contents<!-- omit in toc -->
- [Summary](#summary)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running Tests](#running-tests)
  - [Write your tests](#write-your-tests)
  - [Run your tests](#run-your-tests)
  - [Using Appium Inspector](#using-appium-inspector)
  - [Connected Real Android Devices](#connected-real-android-devices)
  - [Cloud Based Device Services](#cloud-based-device-services)
  - [Biometrics Handling & QR Code Scanning](#biometrics-handling--qr-code-scanning)
  - [Using AATH Agents as Issuers and Verifiers](#using-aath-agents-as-issuers-and-verifiers)

## Summary

The Mobile Wallet Test Harness(aka Aries Mobile Test Harness) provides a [Dev Container](https://code.visualstudio.com/docs/devcontainers/tutorial) to streamline the process of writing and debugging mobile wallet tests. This setup allows developers to write test code for wallet apps without having to install all libraries and configure their local machine for mobile wallet testing. This document outlines the steps to set up and run the Dev Container with Appium server and a local Android device or a Device Cloud Service.

## Prerequisites

- Docker installed on your local machine
- Visual Studio Code with the [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed
- Android Studio or the Android SDK Platform-Tools installed on your local machine 
- A local Android emulator downloaded and installed,a connected Android device, or a subscription to one of the supported Device Cloud Services. 

## Setup

**Clone the repository**: Clone the [Mobile Wallet Test Harness repository](https://github.com/openwallet-foundation/mobile-wallet-test-harness) to your local machine.

**Open the project in VS Code**: Open the cloned repository in Visual Studio Code.

**Add the app apk to the mount location:** The `devcontainer.json` file in  `aries-movile-test-harness/.devcontainer/` defines where to get the app to install into the emulator. It is located in this `mounts` section:
```
	"mounts": [
		{ "source": "/Users/Shel/Projects/BC.gov/apps/bc-wallet", "target": "/bc-wallet/app", "type": "bind" },
		{ ...
	],
```
Change the `source` in the mount to the location of the apps apk file.  Change the `target` if you so desire, but remember it to reference later. 

**Update the apk filename in the android config:** Open and copy the contents of the `local_android_config.json` file and replace the contents of `config.json` with it. 
Update the `app` section with the name of your app apk file. If you changed the `mount` `target` location for the app above. then change it here as well to the correct app target location.
```
{
  "capabilities": {
    ...
    "app": "/bc-wallet/app/app-release1735.apk",
    ...
  }
}
```

**Start the Dev Container**: In VS Code, use the Command Palette (`F1`) to run the `Remote-Containers: Reopen in Container` command. This will start the Dev Container. 
This will take a few minutes on the first opening, since it will be building the container with all test harness dependencies. 

**Start the Android device**: Connect your local Android device to your local machine via USB, or start the Android emulator. Here is an example of what that may look like in a terminal. In the location of your <android-sdk-location>/emulator
```
./emulator -avd <emulator name> -no-snapshot-load &
```
Check to make sure adb server is running and that it sees the running emulator.
```
platform-tools> adb devices
```
You should see something like the following:
```
List of devices attached
emulator-5554	device
```
You could also do all of this in Android Studio in the Device Manager.

**Start Appium Server**: In VS Code, use the Command Palette (`F1`) to run the `Tasks: Run Tasks` command, and select `Start Appium Server` This will start Appium Server inside the Dev Container.

You are now ready to start writing, running, and debugging wallet tests.

## Running Tests

### Write your tests
Write your mobile wallet tests as you would as if you had setup the test harness locally as described in [Implementing Tests for Your Wallet](README.md#implementing-tests-for-your-wallet)

### Run your tests 
The following examples will reference the BC Wallet app. Just replace those specifics with your own. 

**Review/Update the config.json:** Make sure the config.json has the correct app location and app name in the dev container. Also make sure the udid is set to the emulator name you are running.
```
{
  "capabilities": {
    "platformName": "Android",
    "app": "/bc-wallet/app/app-release1735.apk",
    "autoGrantPermissions": true,
    "automationName": "UiAutomator2",
    "udid": "emulator-5554",
    "remoteAdbHost": "host.docker.internal",
    "newCommandTimeout": 480
  }
}
```

**Update the launch.json:** The test harness comes with a handful of predefined launch configurations, mostly that work with BC Wallet. Take one that best matches the Device Service and issuer and verifier agents you are using. The one below uses a local Android device and issuer and verifier from Aries Agent Test Harness Agents. 
The other configuration you will be concerned with is the `--tags` setting. Update this to the tag(s) that represents the test(s) you want to run. 
```
        {
            "name": "Python: Behave current file LocalAndroid",
            "type": "debugpy",
            "request": "launch",
            "module": "behave",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/aries-mobile-tests",
            "env": {
                "DEVICE_CLOUD": "LocalAndroid"
            },
            "args": [
                "${file}",
                "--tags=@T002-Proof",
                "-k",
                "-D",
                "Issuer=AATH;http://host.docker.internal:9020",
                "-D",
                "Verifier=AATH;http://host.docker.internal:9030"
            ]
        },
```

Make sure your launch configuration is selected in  the Run and Debug Section in VS Code. 


**Open the feature file:** In order to run with the debugger with the behave module you must have the feature file with the test definition you referenced with the `--tag` option above, opened and active in VS code and  with the test you want to run

**Run:** At this point you can run the debugger let the test play through or put breakpoints where ever you want to diagnose issues. 

You should at this point see the app load on the device and the test control the app. 

### Using Appium Inspector
When writing and running/debugging tests you will want to use a tool to get the possible element locators in the app. The easiest way to do this with the dev container is to use appium inspector in the browser on your local machine. 
Go to https://inspector.appiumpro.com/ and select the Appium Server section. Enter `localhost` as Remote Host, `4723` as the Remote Port, and `/wd/hub` as Remote Path. Select Attach to Session... and you should see the session ID of the Appium Server session you have running in the Dev Container. Selecting Attach to Session at the bottom of the page and you should see a view of the device, be able to control it, and inspect the page contents. 

### Connected Real Android Devices
If you desire to use a real device, the same launch.json configuration as shown above for LocalAndroid can be used. You will just have to get adb connected to that device either through USB or wirelessly.

### Cloud Based Device Services
The Dev Container can also work with Test Harness supported Device Cloud Services like Sauce Labs or LambdaTest. You would need to configure the config.json to look like the other example configs that exist like `sl_ios_config.json` for Sauce Labs iOS devices.

### Biometrics Handling & QR Code Scanning
To get your Android Emulator to work with biometrics handeling and scanning of QR Codes generated by issuers and verifiers in the Test Harness please follow the instructions [here](MOBILE_DEVICE_SERVICES.md#setup-with-an-local-android-emulator).

### Using AATH Agents as Issuers and Verifiers
You can use many different issuers and verfiers with your tests and when developing in the dev container, including [creating your own agent interfaces](AGENT_ABSTRACTION.md#implementing-agent-interfaces-for-your-agents). However, the most common is to use issuers and verifiers that are created from the AATH test agents. In the context of the dev container, you will need to run these agents outside of the dev container as you regularly would as documented [here](AGENT_ABSTRACTION.md#usage-at-runtime). It seem that when using the AATH agents you will have to use the NGROK tunnel option on the agents for the local android emulator/device and the agents to communicate. 

It has also been observed that sometimes VSCode may hold on to forwarded ports from runs of other dev containers (for example if you are running AATH agent in a dev container). If you are running AMTH in a Dev Container, you are also using AATH agents as issuers or verifiers, and you are having trouble with calls to the agent hanging, check the ports tab in VSCode in the running dev container. If you see ports like 9020 or 9030, just delete the port forwarding in that tab and rerun the tests. 


