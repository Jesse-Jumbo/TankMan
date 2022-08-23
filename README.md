# TankMan
## 遊戲說明
<img src="https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/49dc8cb825ddd8dea61936fb6d339c846fe68d6c/asset/image/TankMan.svg" alt="logo" width="100"/> 


[![TankMan](https://img.shields.io/github/v/tag/Jesse-Jumbo/TankMan)](https://github.com/Jesse-Jumbo/TankMan/tree/0.1.9)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![MLGame](https://img.shields.io/badge/MLGame-10.0.0-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![pygame](https://img.shields.io/badge/pygame-2.0.1-<COLOR>.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)


坦克人(Tank Man)，一款經典的雙人對戰遊戲，時間內率先擊殺對手獲勝，否則以分數高者獲勝，除了擊中對手外，破壞遊戲物件，以獲得更高積分。 

！注意: 場上資源恢復皆須時間，先到者得，你需要這些補充品以提供前進和射擊的燃油和子彈。

![game.gif](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/game.gif)
---
## Requirements
- Python==3.9
- pygame==2.0.1
- pytmx=3.31
---
## 即將更新內容

- 
---
## 遊戲簡介:
雙人對戰遊戲，1P玩家透過方向鍵操控綠色坦克車，2P玩家透過WASD操控藍色坦克車，按下空白鍵與F鍵可射擊砲彈，場上會有各類補給站，經過以補給該資源。

---
## 畫面說明:
<img src="https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/view_ex.png" alt="view_ex.png" width="1000" height="600"/> 

---
# 遊戲細節：
## 啟動方式:
- 直接啟動`main.py`即可執行。
- 在命令行輸入命令執行。
---
## 遊戲參數設定
```python
# main.py
game = TankMan.TankMan(map_no=1, frame_limit=300, sound="off")
```
- `TankMan`後不輸入參數，則默認使用預設值，即範例參數值。
```bash
# MLGame.py
# Copy and Paste to play the game with manual
python MLGame.py -i ml_play_manual.py -f 120 TankMan --map_no 1 --sound on --frame_limit 30

# Copy and Paste to play the game with AI
python MLGame.py -i ml_play_template_1P.py -i ml_play_template_2P.py -f 120 TankMan --sound on --frame_limit 30 --map_no 1
```
- `map_no`:  輸入地圖編號，以選擇遊戲的地圖。
- `frame_limit`:  輸入遊戲總frame數，以決定遊戲的幀數。
- `sound`:  輸入`on`或`off`，控制是否播放遊戲音效。
- 如果在`MLgame.py`後加上`-1`，代表只執行一次遊戲。
---
## 遊戲操作：

### 使用鍵盤
- 角色移動：方向鍵控制 1P（綠），WASD鍵控制 2P（藍）移動和轉彎。
- 遊戲畫面: 透過 I、K、J、L 來上下左右移動畫面；透過 O、U 來放大縮小畫面。


### ＡＩ控制
- 藉由遊戲資訊，在`ml_template_1P.py`，撰寫控制1P（綠），和在ml_template_2P.py，撰寫控制2P（藍）的AI Mode。
- 藉由遊戲資訊，在`ml_play_manual.py`，撰寫執行坦克車行動的AI Mode。
---
# 遊戲玩法
1. 雙人對戰 → 時間內擊敗對方，或分數高者獲勝。
## 過關條件
1. 雙人對戰
    1. 將對方擊敗。
    2. 加總所有積分：
        - 對方失去的生命值。
        - 每擊中一次牆壁 * 1 分。
        - 擊破牆壁 * 5 分。
---
## 失敗條件

1. 雙人對戰
    1. 生命歸零。
    2. 時間結束，分數較對方低。
---
## 物件設定：
### Tank

---
1. 前進、後退速度（8 px）
2. 轉彎角度（45度）
3. 生命機會（3次）
4. 護盾值（100）
5. 燃油（100）
6. 彈匣（10）
---
### Walls
1. 生命次數（5）
2. 顏色設定（依照生命次數決定）
---
### 補給站
1. 燃油站
    - 玩家經過可補充燃油，每秒回一點燃油，上限100。

2. 彈藥站
    - 玩家經過可補充彈藥，每五秒補充一顆子彈，上限10。

---
# 地圖說明
- 寬1320 pixel；高660 pixel
- 每格60 * 60 pixel，可放置一個物件

---
## 地圖製作

coming soon
---
# image sours
[hourglass](https://opengameart.org/content/animated-hourglass)
[object](https://opengameart.org/content/simple-shooter-icons)
[bullet](https://opengameart.org/content/simple-2d-tank)

# sound sours
[BGM](https://opengameart.org/content/commando-team-action-loop-cut)
[SHOOT](https://opengameart.org/content/random-low-quality-sfx)
