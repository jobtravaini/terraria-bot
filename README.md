# terraria-bot

This is a simple Terraria bot to control your TShock server from a Discord Channel. To use this feature, you will have to enable [REST Services from your TShock server](https://tshock.readme.io/v4.3.22/reference).

  - [TShock Server](https://github.com/Pryaxis/TShock/releases) is required.
  - **startup.bat** - This script should be used to start your TShock server on your windows machine
  - **startup.sh** - This script should be used to start your TShock server on your unix machine (_pending_)

### Tech

To run terraria-bot you need the following technologies

* [python](https://www.python.org/) - Python version 3.x is required
* **python libraries** - The file requirements.txt specifies all the required libraries and modules (_produced by pigar_)

### Installation

  - **TShock** should be installed and configured to expose REST Services on your localhost.
  - **startup script** should be located at your TShock root folder
  - You have to configure your [Discord Bot Application](https://github.com/SinisterRectus/Discordia/wiki/Setting-up-a-Discord-application)
  - Populate your token on the [Bot.py](https://github.com/jobtravaini/terraria-bot/blob/master/Bot.py) constant **TOKEN**

### Configuration

  - It is required to [create an Admin user on your TShock Server](https://tshock.readme.io/docs/getting-started)
  - It is required to configure your TShock Admin username and password (_**USERNAME** and **PASSWORD** constants_) on the [Server.py](https://github.com/jobtravaini/terraria-bot/blob/master/tshock/Server.py) file (_REST API requires admin access_)
  
### Running

  - Add your Bot to your Discord Channel. Suggestion: [oauth2 URL](https://discordapp.com/developers/docs/topics/oauth2)
  - Start your server using the **startup** script and run Bot.py file
