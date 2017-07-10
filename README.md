# SeverNettle
A Twitter bot designed to help OnePlus 5 users by putting @OnePlus tweets upside down

## What is this? 

After seeing the OnePlus 5 upside down screens fiasco, I decided to make this bot. It will reply to every tweet by OnePlus with an upside down version of their tweet. 

## Requirements

- Python3, the newest the best 
- Twython 
- FFMPEG
- Imagemagick

This script was designed to be used on Linux, so you'll probably need that too. 

## Installation and Setup 

- Clone this repository 
- Be sure to install the requirements : install Twython with pip (`pip install twython`) and the other requirements with your distro's package manager. 
- Follow the instructions in the `config.py.example` file
- Mark `bot.py` as executable : `chmod +x bot.py`

## How to use

This script can be run by simply typing `python3 bot.py`. However, as this script checks for tweets only when it's ran, I recommend using crontab to run it at specific times. If needed, here's a tutorial on how to use the `cron` command : https://www.howtogeek.com/101288/how-to-schedule-tasks-on-linux-an-introduction-to-crontab-files/

## Credits :

- [Ryan McGrath for Twython](https://github.com/ryanmcgrath/twython) 
- The ffmpeg and imagemagick team for their respective programs

## License

This project is available under the terms of the WTFPL. You can find a copy of the license in the LICENSE file. 

