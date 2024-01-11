# TankMan
## 遊戲說明
<img src="https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/49dc8cb825ddd8dea61936fb6d339c846fe68d6c/asset/image/TankMan.svg" alt="logo" width="100"/> 


[![TankMan](https://img.shields.io/github/v/tag/Jesse-Jumbo/TankMan)](https://github.com/Jesse-Jumbo/TankMan/tree/0.7.1.1)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![MLGame](https://img.shields.io/badge/MLGame-10.2.5a0-<COLOR>.svg)](https://pypi.org/project/mlgame/10.2.5a0/)
[![pygame](https://img.shields.io/badge/pygame-2.0.1-<COLOR>.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)


坦克人(Tank Man)，一款經典的雙人對戰遊戲，時間內率先擊殺對手獲勝，否則以分數高者獲勝，除了擊中對手外，破壞遊戲物件，以獲得更高積分。 

！注意: 場上資源恢復皆須時間，先到者得，你需要這些補充品以提供前進和射擊的燃油和子彈。

![game.gif](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/game.gif)
---
## Requirements
- Python==3.9
- mlgame==10.2.5a0
- pytmx=3.31
---
## 更新說明
- 0.6.0 版本之後，遊戲為 2～6 人 團隊對抗遊戲
- 0.7.0 版本之後，坦克和砲管的方向可以分開控制
- 0.7.1 版本之後，物件尺寸從原來的 50ｘ50 縮小為 25ｘ25，且補給站可被破壞
---
## 遊戲簡介:
2～6 位玩家進行團隊對抗賽，GreenTeam 為綠色坦克車，BlueTeam 為藍色坦克車，透過回傳遊戲指令，操控玩家與射擊砲彈，場上會有各類補給站，經過以補給該資源。

---
## 畫面說明（2.x版本）:
<img src="https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/view_ex.png" alt="view_ex.png" width="1000" height="600"/> 

---
# 遊戲細節：
## 啟動方式:
- 在命令行輸入命令執行。
---
## 遊戲參數設定
- 在以下命令中，`.`代表執行的遊戲專案路徑，若`.`後不輸入參數，則默認使用預設值，即`game_config.json`內參數值。
```bash
# MLGame.py
# Copy and Paste to play battle game with manual
python -m mlgame -f 120 -i ml/ml_play_manual.py -i ml/ml_play_manual.py . --green_team_num 1 --blue_team_num 1 --is_manual "1" --frame_limit 1000

# Copy and Paste to play battle game with AI
python -m mlgame -f 120 -i ml/ml_play.py -i ml/ml_play.py . --green_team_num 1 --blue_team_num 1 --frame_limit 1000
```
- `green_team_num`：選擇數字 1～3，以決定 綠隊 人數。
- `blue_team_num`：選擇數字 1～3，以決定 藍隊 人數。
- `is_manual`:  輸入 "1" 啟用手動模式，以讓遊戲適合手動遊玩。
- `frame_limit`:  輸入數字 30～3000，以決定遊戲的總幀數。
- `sound`:  輸入`on`或`off`，控制是否播放遊戲音效。
- 如果在`mlgame`後加上`-1`，代表只執行一次遊戲。
---
## 遊戲操作：

### 使用鍵盤
- 角色移動：方向鍵控制 1P，WASD 鍵控制 2P 的移動和轉彎。
- 角色射擊：1P 按下`M`鍵進行射擊，2P 按下`F`鍵進行射擊。
- 砲管旋轉：1P 按下`Z`、`X`鍵左右旋轉，2P 按下`Q`、`E`鍵左右旋轉。
- 遊戲畫面: 透過`I、K、J、L`來上下左右移動畫面；透過`O、U`來放大縮小畫面。
- 隱藏遊戲資訊：按下`H`鍵，可隱藏畫面中的遊戲資訊。
- 遊戲暫停：按下`P`鍵，可暫停遊戲（mlgame 10.2 後版本才有效）。
- 遊戲暫停：遊戲 AI 回傳`PAUSED`指令，可暫停遊戲。


### ＡＩ控制
- 藉由遊戲資訊，在`ml`資料夾，撰寫控制遊戲角色的`.py`檔。
- 可參考`ml_play.py`自動範例程式，撰寫自動遊玩的程式。
- 可參考`ml_play_manual.py`手動範例程式，撰寫手動遊玩的程式。
---
# 遊戲玩法
1. 團隊對抗戰 → 時間內殲滅敵對，或高分隊伍獲勝。
## 過關條件
1. 團隊對抗戰
    1. 將敵隊全數擊敗。
    2. 高過敵隊積分：
        - 對方失去的生命 * `20`分。
        - 每擊中一次牆壁 * `1`分。
        - 擊破牆壁 * `5`分。
---
## 失敗條件

1. 團隊對抗戰
    1. 生命歸零。
    2. 時間結束，分數較敵隊低。
---
## 物件設定：
### **`Tank`**

---
1. 前進、後退速度（8 px）
2. 車身轉彎角度（45 度） 
3. 砲管旋轉角度（45 度） 
4. 生命機會（3 次） 
5. 燃油（100） 
6. 彈匣（10）
---
### **`Walls`**
1. 生命次數（3）
2. 透明設定（依照生命次數決定）
---
### **`補給站`**
1. 燃油站
    - 玩家經過補充 30 點燃油，超過 100，則無效。
    - 與玩家或子彈碰撞後消失，30 幀後隨機位置顯示。

2. 彈藥站
    - 玩家經過補充 5 顆彈藥，超過 10，則無效。
    - 與玩家或子彈碰撞後消失，30 幀後隨機位置顯示。

---
# 地圖說明
- 寬 1000 pixel；高 600 pixel
- 每格 25 * 25 pixel，可放置一個物件

---
# image sours
- [Green Tank／Blue Tank](https://linevoom.line.me/user/_dV001P0rSN_bh8zGE0q4jmdr4Fn5d-j73cLrjTc?utm_medium=windows&utm_source=desktop&utm_campaign=Profile)
- [Bullet](https://linevoom.line.me/user/_dV001P0rSN_bh8zGE0q4jmdr4Fn5d-j73cLrjTc?utm_medium=windows&utm_source=desktop&utm_campaign=Profile)
- [Hourglass](https://opengameart.org/content/animated-hourglass)
- [Other Object](https://opengameart.org/content/simple-shooter-icons)

# sound sours
- [BGM](https://opengameart.org/content/commando-team-action-loop-cut)
- [SHOOT](https://opengameart.org/content/random-low-quality-sfx)
