# PremiumBot - List premium members within your chats
### Authored by Shinanygans (shinanygans@proton.me)


## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.10 or higher**: If you don't have Python installed, you can download it from the [official Python website](https://www.python.org/downloads/).

## Installation

Follow these steps to set up your project:

1. Clone this repository to your local machine:

    ```shell
    git clone https://github.com/shnygns/premiumbot.git
    ```

2. Navigate to the project directory:

    ```shell
    cd premiumbot
    ```

3. If you prefer using Pipenv:

    - Install Pipenv (if not already installed):

        ```shell
        pip3 install pipenv
        ```

    - Create a virtual environment and install dependencies:

        ```shell
        pipenv install 
        ```
        ...or, so specify the python version overtly:

        ```shell
        pipenv install --python 3.10
        ```


    - Activate the virtual environment:

        ```shell
        pipenv shell
        ```

4. If you prefer using venv and requirements.txt:

    - Create a virtual environment:

        ```shell
        python3 -m venv venv
        ```

    - Activate the virtual environment:

        - On Windows:

            ```shell
            .\venv\Scripts\activate
            ```

        - On macOS and Linux:

            ```shell
            source venv/bin/activate
            ```

    - Install dependencies:

        ```shell
        pip install -r requirements.txt
        ```

5. Make a copy of the template file `sample-config.py` and rename it to `config.py`:

    ```shell
    cp sample-config.py config.py
    ```

6. Open `config.py` and configure the bot token and any other necessary settings.


7. IMPORTANT - Configure named admins in config.py:
If other people find your PremiumBot through a Telegram search and run it in their rooms, THEIR DATA WILL BE STORED IN YOUR DATABASE! This is no bueno. 

To stop this from happening, put your Telegram user_id in the AUTHORIZED_ADMINS list in config.py. If there are user_ids in this list, then only these user_ids will be able to issue bot commands, and the bot will only vacuum up information from chats in which at least one user_id on this list is an admin. Problem solved.

AUTHORIZED_ADMINS = [XXXXXXXXXX, XXXXXXXXXX]


8. Run the script from your virtual environment shell:

    ```shell
    python premiumbot.py
    ```

## Getting a Bot Token

To run your Telegram bot, you'll need a Bot Token from the Telegram BotFather. Follow these steps to obtain one:

1. Open the Telegram app and search for the "BotFather" bot.

2. Start a chat with BotFather and use the `/newbot` command to create a new bot.

3. Follow the instructions to choose a name and username for your bot.

4. Once your bot is created, BotFather will provide you with a Bot Token. Copy this token.

5. In the `config.py` file, set the `BOT_TOKEN` variable to your Bot Token.


## Getting a Telegram user API ID and HASH

Premiumbot uses expanded functionality from telegram's MTProto API to deliver a list of participants in your chat. These are available at my.telegram.org after filling out a short form.


In config.py:

API_ID = XXXXXXXXXX      # Integer (i.e. no quotes)
API_HASH = "XXXXXXXXXX"  # String (i.e. with quotes)


## Usage


COMMANDS
/premium - Deliver a CSV of premium users to a private chat with the bot.

IMPORTANT:
In order for the bot to deliver your list, you MUST FIRST /START a private chat with the bot! Bot's cannot initiate private chats on their own.



## Configuration and Features

Do NOT forget to make a copy of sample-config.py and call it config.py. The program will error out if you don't.  The config file is where you store your bot token from Bot Father. But you can also configure other special features!


### Authorized Admins

AUTHORIZED_ADMINS = [XXXXXXXXXX, XXXXXXXXXX]

Only those users listed will be able to command the bot.




## Support
This script is provided AS-IS without warranties of any kind. I am exceptionally lazy, and fixes/improvements will proceed in direct proportion to how much I like you.

"Son...you're on your own." --Blazing Saddles



