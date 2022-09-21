# 地圖製作教學

此文將會介紹如何使用`Tiled`這個軟體製作一個地圖，並放進[PAIA坦克大作戰](https://github.com/Jesse-Jumbo/TankMan) 中，讓我們的坦克車可以跑在自己客製化的地圖。

建立好的地圖除了可以直接放入[PAIA坦克大作戰](https://github.com/Jesse-Jumbo/TankMan) ，在個人環境中做使用之外，也可以分享給其他人，讓所有人使用。

---
# 檔案更新

- [圖塊集](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/TankManObj.png)
---

# 軟體安裝
    ⚙ 製作地圖需要安裝Tiled這個軟體，請大家到 [官網](https://www.mapeditor.org) 中下載適合自己電腦作業系統的版本：

## 安裝流程：

1. 進入到[官網](https://www.mapeditor.org)後點擊「Donload on itch.io」跳轉到下載頁面。
    ![](https://i.imgur.com/dCbcYXs.png)

    
    
2. 點擊「Download Now」後將會顯示捐款浮動視窗。
    ![](https://i.imgur.com/FAk59CN.png)

    
3. 點選最上方「No thanks, just take me to the downloads」的選項後，即可看到不同作業系統適用的安裝檔。
    ![](https://i.imgur.com/VUjvlKz.png)

    
4. 選擇與自己電腦相容的安裝檔即可下載並安裝。
    ![](https://i.imgur.com/OpnUnXD.png)

    

---

# 新增地圖專案
    ⚙ 這部分主要說明如何建立一個地圖檔案並儲存。



1. 開啟Tiled，建立新地圖
第一次開啟Tiled的時候，可以在左上角看到以下截圖畫面。其中紅框內是比較常用到的功能。
選擇「New Map」，進入到軟體中。
    ![](https://i.imgur.com/hvcCuC0.png)

    

---

1. 設定地圖大小
    
    選擇建立新地圖後會跳出地圖屬性設定視窗，其中「地圖大小」的設定將會直接影響迷宮大小。
    
    將「圖塊大小」的高與寬都調整回50px，並設定好地圖大小之後就可以按下「Save As」
    ![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/mapping/define_map_format.jpg)



---

1. 儲存檔案
    
    存檔時需要注意存檔類型，預設為`.tmx`，也是Tiled可以直接打開編輯的檔案格式；而坦克車使用的也是TMX檔。
    
    ![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/mapping/save_file.jpg)
    

---

1. 新增圖塊集
    
    存好檔案之後就會進入到編輯頁面。
    
    - 點選圖塊區域中間的「New Tileset」
        
      ![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/mapping/new_tilsests.png)

        
- 再點擊「Browser」並打開[圖片檔](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/TankManObj.png) 。
    ![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/TankManObj.png)


- 將圖片寬度與高度調整為50px，邊距與間距分別為0px與0px。
    ![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/mapping/tilsest_format.png)


- 成功新增圖庫集之後就可以開始編輯地圖了
    ![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/mapping/object_image.png)


---

# 編輯地圖


    ⚙ Tiled的基本編輯方式相當簡單，只需要使用滑鼠選取圖塊集的方塊，再移動到編輯區點擊方格即可。
    也可以持續按著滑鼠左鍵拖曳繪製
![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/mapping/map.png)

---
## 積木種類

圖塊集的每個格子都會有相對應的編號，其順序從1開始，由左至右、由上至下。

目前坦克車使用到的編號為1~5，對應到的圖塊如圖所示，這5種圖塊的功能分別為：

1. 綠色坦克，玩家1P的起始位置，面向西方。
2. 藍色坦克，玩家2P的起始位置，面向東方。
3. 磚牆，遊戲中的牆壁，被擊中3次會消失。
4. 子彈圖示，子彈補給站的起始位置，每次經過可獲得5顆子彈。
5. WiFi圖示，油料補給站的起始位置，每次經過可獲得30點油料。

![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/mapping/image_no.png)


---

## 地圖圖塊與遊戲物件的關係

- 地圖圖塊的大小 = 遊戲物件的大小。

---

## 常用工具與功能列

- 橡皮擦
    
    在上方工具列可以找到，使用方式與圖塊集相同。
    
    ![](https://i.imgur.com/8O9nkvX.png)

    
- 調整地圖大小
    
    在上方的選單選擇「地圖」→「調整地圖大小」
    
    可以調整當前地圖的長寬，並移動原先的地圖物件，在視窗中間將會出現預覽圖。
    ![](https://i.imgur.com/A1vp255.png)


---

# FAQ 與 注意事項

## 地圖存放路徑
```python
Game/asset/maps/
```
![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/mapping/image_path.png)

## 地圖檔名命名規則

- 檔名最後的數字（`x`）就是地圖的編號。
    - 地圖格式：map_0`x`.tmx
    
---

## 如何更換新版圖塊集
當更新了新版圖塊集。過去有使用過舊版的使用者有可能遇到編號不相容的問題，在此提供解決方法。

1. 避免在同一個檔案下使用兩個圖塊集
2. 刪除舊版圖塊集

![](https://raw.githubusercontent.com/Jesse-Jumbo/TankMan/main/asset/image/mapping/del_image.png)

當軟體中存在一個以上的圖塊集時編號將會存在衝突，導致載入遊戲時無法順利產生物件，因此建議使用者在同一個地圖檔案內不要使用兩個圖塊集。例如：在曾經以舊版編輯過的地圖裡直接使用新版圖塊集，可以選擇重新開新的地圖檔案套用新版的圖塊集。如果還是擔心會有混用的問題，在圖塊集的下方有垃圾桶的Icon，可以直接刪除舊的圖塊集。

---