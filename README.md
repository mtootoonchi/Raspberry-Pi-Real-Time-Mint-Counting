# Raspberry-Pi-Real-Time-Mint-Counting

This is a Real-Time Mint Counting program tested using the Raspberry Pi 3 B+ using Raspberry Pi OS Lite (64-bit), it may work on other devices, however. This program uses a Raspberry Pi Camera Module V2 connected to the Raspberry Pi with a CSI camera port to take video for detecting how much mints there are but also to stream that video on a local network to an internet browser along with other information all Real-Time streamed.

Video: WIP

To use this project, I recommend you use the hardware and OS that I used as this tutorial will assume this setup however, if you know what you are doing feel free to try other configs. With your Raspberry Pi make sure you can access it with a mouse and keyboard and view it with a monitor. I recommend you eventually set up SSH. After you boot up your Raspberry for the first time you need to do first time set up just follow the instructions on screen. I used ‘user’ as my username you may do the same. Afterwards you get the option of expanding the file system, setting up SSH, time zone, and internet. I recommend you do these things. In the new non-Legacy edition on the Raspberry Pi OS which I am using with the Raspberry Pi OS Lite (64-bit) you do not need to enable the camera since it is enabled by default in the new non-Legacy edition and you do not need legacy camera support. Here is the command to change these settings:

```shell
sudo raspi-config
```

After you finish editing those settings, I recommend you run this command twice to ensure you have up to date packages:

```shell
sudo apt update && sudo apt upgrade
```

You also will need to figure out your local IP connected to your router for both SSH and connecting to your Raspberry with your internet browser later. There are multiple ways to do this, but I recommend running this command:

```shell
ifconfig
```

After that you will see a bunch of text appear. What you are looking for is the word ‘inet’ and the number ’192.168.1.X’. The ‘X’ should be replaced with a number and that’s the number you are looking for since it is different for everyone. Remember this full number as you will need it for SSH and connecting to your Raspberry with your internet browser later.

Afterwards you need to install the necessary packages to run the project:

```shell
sudo apt install python3-flask
sudo apt install python3-opencv
sudo apt install opencv-data
sudo apt install git
```

Then you need to download the project onto your Raspberry Pi:

```shell
git clone https://github.com/mtootoonchi/Raspberry-Pi-Real-Time-Mint-Counting.git
```

You can check out your new project by doing:

```shell
cd Raspberry-Pi-Real-Time-Mint-Counting/
ls -all
```

Finally, while in the directory of Raspberry-Pi-Real-Time-Mint-Counting, lets run the project by doing:

```shell
sudo python main.py
```

It may take a minute, but you should see some text basically saying that Flask is running now. What you are waiting for is when you see ‘Debugger PIN:’ then it is ready.

Lastly, on any device connected to the same router as your Raspberry Pi (this includes devices such as a phone or a desktop) go on any internet browser and type this for the URL:

```shell
http://192.168.1.X:8000/
```

Remember the ‘X’ should be replaced with that number you found earlier for the local IP. Now you should see both the video feed and how many mints are currently on the screen! If you don’t see the video feed or/and you get some sort of error saying that the camera isn’t detected, make certain that you are not using legacy camera support and the CSI camera port on the camera and Raspberry Pi is firmly connected to each other as this can create issues, you may also want to try a different CSI camera port on the Raspberry Pi.

