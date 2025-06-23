# Keila Project – AI Personal Assistant 

## Technical Specification

Keila is a physical device based on a Raspberry Pi 3 B+, using Python, that functions as an intelligent virtual assistant. The system receives voice commands, converts them to text (STT), sends them to the OpenAI API (ChatGPT), receives the response in text, and converts it back to audio (TTS) for spoken output.  

All interactions are displayed on a touchscreen, which also serves as a local configuration interface. The system can be configured either locally via the embedded screen or remotely via a browser. Both are valid ways to interact with Keila’s API.  

The capacitive screen must display a Keila avatar with simple facial expressions. This screen is used to show the avatar and information when needed, as well as to provide access to settings as an alternative to the browser. There must be a physical button (or one accessible on the screen) that starts a predefined ACTION, such as VoicePrompt.  

All interaction with Keila must occur via API, allowing 100% control via the screen (menus) or via a web client provided by Keila itself, with full access to features. 

Keila must have a temperature sensor that allows measuring and informing the user of the temperature.  

## Structure and Operation  

Keila can have different ACTIONS, which are capabilities/features that can be added in the future. At the moment, the only ACTION is VoicePrompt, which covers the entire process of recording audio, sending it to GPT, and playing the response. In the future, other ACTIONS may be created, such as Play Music, among others.  

There is a main state that defines the application flow: INIT, CANCELING, READY, or RUNNING. When an ACTION is happening, the global state is RUNNING. There is an endpoint capable of canceling all actions in progress.  

This is implemented with a Thread Manager, which has methods such as canceling all actions and starting threads. Each ACTION runs on its own thread and can start new threads, but the main flow must always be ready to be interrupted by a user command.  

There is a continuous flow running on the main thread, aiming to keep Keila very responsive. This means that while it performs tasks such as searching for information on the internet, playing or recording audio, it must be able to interrupt what it is doing and immediately restart the audio listening process upon receiving a user command.  

This behavior involves continuous listening programming (non-stop), with silence recognition (perception that the user has stopped or finished speaking) and detection of basic commands such as “Hi Keila,” among others.  

---

## Technical Requirements  

All development must be done on a Windows machine, ensuring that all of Keila’s features, such as audio recording and playback, work properly. The system must be able to play audio both on the Raspberry Pi and on Windows, handling the differences between environments correctly. For this, libraries compatible with both must be used.  

There must be a configuration file called `keila_config.ini` in the folder where the program is run.  



## Features  

- Voice recognition  
- Integration with OpenAI (GPT-4/4o)  
- Voice response (TTS)  
- Embedded touchscreen interface  
- Admin panel via browser  
- Local web API for control and configuration  
- Indicator LEDs  
- Ambient temperature sensor  
- Automatic startup on power-on  
- Internal API to serve the screen or the Admin Panel via browser
- Actions system to allow new funcionality

## Hardware Used  

- Raspberry Pi 3 B+ 1Gb: Main computer  
- HDMI + USB Capacitive Screen (5~7"): Visual touch interface  
- 5V 3A (or 4~5A) power supply: System power  
- USB or I2S microphone: Audio capture  
- P2 or Bluetooth speaker: Audio output  
- Temperature sensor (DHT22 or BME280): Environment data  
- RGB LED (WS2812 or regular): Visual feedback  
- Powered USB hub: To connect microphone, touch, etc.  
- 16~32GB microSD card: Operating system and data  

## Software  

- Operating system: Raspberry Pi OS Lite (headless) or with interface  
- Main language: Python 3  
- Web/API framework: FastAPI  
