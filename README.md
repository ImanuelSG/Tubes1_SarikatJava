# Tubes1_SarikatJava

![image](img/cover.jpg)

## Contents
- [General Information](#general-information)
- [Program Requirements](#program-requirements)
- [Setup](#setup)
- [The Bot's Logic](#the-bots-logic)
- [Project Structure](#project-structure)
- [Authors](#authors)

## General Information
Diamonds is a programming challenge that pits your bot against bots created by other players. Each player will have a bot whose goal is to collect as many diamonds as possible. There are several elements to this game. Those are: diamonds, red diamond button, teleporters, bots and bases, and inventory. To win the match, each player must implement specific strategies for their respective bots which will be contested in a 60 second round with three oponents.
<br>
<br>
Each bot will have an inventory of size 5 which can store the diamonds before it goes back to base. The bot's score will only increase if the diamonds stored in the inventory have been brought back to base. In this game, one player can tackle another, causing the other player to lose all of its diamonds in its inventory. The other bot will re-spawn at base.

## Program Requirements
### Game Engine Requirement
- Node.js (https://nodejs.org/en) 
- Docker desktop (https://www.docker.com/products/docker-desktop/) 
- Yarn (`npm install --global yarn`)
### Bot Requirement
- Python (https://www.python.org/downloads/)

## Setup
### Game Engine Setup
1. Download the source code (.zip) from [the latest release](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0)
2. Extract the zip file and open the terminal
3. Go to the project root directory
    ```
    $ cd tubes1-IF2110-game-engine-1.1.0
    ```
4. Install dependencies with yarn
    ```
    $ yarn
    ```
5. Set up default environment variable
    Windows:
    ```
    $ ./scripts/copy-env.bat
    ```
    Linux:
    ```
    $ chmod +x ./scripts/copy-env.sh
    $ ./scripts/copy-env.sh
    ```
6. Set up a local database by opening docker then run the following command
    ```
    $ docker compose up -d database
    ```
    Then, run the following script. For Windows:
    ```
    $ ./scripts/setup-db-prisma.bat
    ```
    For Linux:
    ```
    $ chmod +x ./scripts/setup-db-prisma.sh
    $ ./scripts/setup-db-prisma.sh
    ```
7. Build and run by the following commands
    ```
    $ npm run build
    ```
    ```
    $ npm run start
    ```
To access the frontend page of the website, visit http://localhost:8082/

### Bot Setup
1. Download the source code (.zip) from [the latest bot release](https://github.com/haziqam/tubes1-IF2211-bot-starter-pack/releases/tag/v1.0.1)
2. Extract the zip file and open the terminal
3. Go to the project root directory
    ```
    $ cd tubes1-IF2110-bot-starter-pack-1.0.1
    ```
4. Install dependencies with pip
    ```
    $ pip install -r requirements.txt
    ```
5. Run the bot
    To run a bot, you can use the following command in the src directory
    ```
    $ python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo
    ```
    Or, if you want to run multiple bots (up to four bots) at a time, you can run (and edit) the following script<br>
    For Windows:
    ```
    $ ./run-bots.bat
    ```
    For Linux:
    ```
    $ ./run-bots.sh
    ```
    You can change the logic used (in the example above, the logic is Random), email, name, and password.

## The Bot's Logic
In this repository, we experimented with four Greedy algorithm approaches in the game Etimo: Diamonds, namely Greedy by Distance, Greedy by Points, Greedy by Point Density, and Greedy by Area Density. After conducting analysis and simulations, we propose the Greedy by Point Density algorithm as the main greedy algorithm for this bot. At each step, this bot will choose the step advancing to the diamond with the largest density (point / distance) value, taking into acount teleporters which might reduce distance (and therefore increase the density).

## Project Structure
```
.
├── README.md
├── doc
│   └── SarikatJava.pdf
└── src
    ├── README.md
    ├── __pycache__
    │   └── decode.cpython-311.pyc
    ├── decode.py
    ├── game
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── api.cpython-311.pyc
    │   │   ├── board_handler.cpython-311.pyc
    │   │   ├── bot_handler.cpython-311.pyc
    │   │   ├── models.cpython-311.pyc
    │   │   └── util.cpython-311.pyc
    │   ├── api.py
    │   ├── board_handler.py
    │   ├── bot_handler.py
    │   ├── logic
    │   │   ├── Others
    │   │   │   ├── SquareDensity.py
    │   │   │   ├── __pycache__
    │   │   │   │   ├── SquareDensity.cpython-311.pyc
    │   │   │   │   ├── points.cpython-311.pyc
    │   │   │   │   └── teleportGreed.cpython-311.pyc
    │   │   │   ├── points.py
    │   │   │   └── teleportGreed.py
    │   │   ├── SarikatJava.py
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── DensityBot.cpython-311.pyc
    │   │   │   ├── PureDensity.cpython-311.pyc
    │   │   │   ├── SarikatJava.cpython-311.pyc
    │   │   │   ├── ShortestDistance.cpython-311.pyc
    │   │   │   ├── SquareDensity.cpython-311.pyc
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   ├── base.cpython-311.pyc
    │   │   │   ├── points.cpython-311.pyc
    │   │   │   ├── random.cpython-311.pyc
    │   │   │   └── teleportGreed.cpython-311.pyc
    │   │   ├── base.py
    │   │   └── random.py
    │   ├── models.py
    │   └── util.py
    ├── main.py
    ├── requirements.txt
    ├── run-bots.bat
    ├── run-bots.sh
    └── temp.txt
```
## Authors
| Nama                  | NIM      |
| --------------------- | -------- |
| Imanuel Sebastian Girsang  | 13522058 |
| Venantius Sean Ardi Nugroho | 13522078 |
| Julian Chandra Sutadi | 13522080 |