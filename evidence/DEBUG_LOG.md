# Red-to-Green Debug Log

Preserve one genuine failure. Do not invent a retrospective story after the test is green.

| Field | Trio record |
|---|---|
| Command that failed | |
| Exact failing test | |
| Last useful line / observed fact | |
| Expected behavior from the contract | |
| Smallest hypothesis | |
| Smallest code change | |
| Focused rerun command | |
| Focused result | |
| Full regression result | |
| Commit or PR URL | |

## Explain-back

What evidence rules out at least one alternative cause?

1.蘋果生成判斷位於 [game.py (line 73)](D:/Lab/lab03-snake-trio/src/snake_trio/game.py:73) 的 choose_food()：
def choose_food(body: list[Cell]) -> Cell:
    for y in range(0, HEIGHT, CELL):
        for x in range(0, WIDTH, CELL):
            if (x, y) not in body:
                return (x, y)
它不是隨機生成，而是按照以下順序搜尋：
y 從 0 開始，也就是最上面一列。
x 從 0 開始，也就是最左邊。
遇到第一個沒有蛇身的格子便立即回傳。
目前蛇身在 (200, 200) 附近，所以第一個空格就是：
food = (0, 0)
因此蘋果總是出現在左上角。
呼叫生成判斷的地方有兩處：
開始新遊戲：[game.py (line 91)](D:/Lab/lab03-snake-trio/src/snake_trio/game.py:91)
吃到蘋果後重新生成：[game.py (line 105)](D:/Lab/lab03-snake-trio/src/snake_trio/game.py:105)
另外，蘋果的繪製位置是：
screen.blit(apple_sprite, (fx, fy - CELL // 2))
因此當食物格為 (0, 0) 時，圖片會從 y=-10 開始畫，向上的葉子會被視窗裁掉一半。這是顯示問題；碰撞格仍然正確位於 (0, 0)。
合理修正方向是讓 choose_food()：
排除最上面一列，讓蘋果葉不超出視窗；
排除牆壁占用的邊緣；
從剩餘且沒有蛇身的格子中隨機選擇。

=>蘋果要如何從for迴圈改成random

原本的程式其實不是「生成」食物，而是從左上角開始依序搜尋第一個空格。
原本寫法：
for y in range(0, HEIGHT, CELL):
    for x in range(0, WIDTH, CELL):
        if (x, y) not in body:
            return (x, y)
原本 for 迴圈如何運作
假設：
WIDTH = 640
HEIGHT = 480
CELL = 20
第一層：
for y in range(0, HEIGHT, CELL):
會產生：
0, 20, 40, 60, ..., 460
第二層：
for x in range(0, WIDTH, CELL):
會產生：
0, 20, 40, 60, ..., 620
搜尋順序會是：
(0, 0)
(20, 0)
(40, 0)
...
(620, 0)
(0, 20)
(20, 20)
...
當程式遇到第一個沒有蛇身的位置：
if (x, y) not in body:
    return (x, y)
函數就立即結束。因此，只要 (0, 0) 沒有蛇身，蘋果永遠會出現在 (0, 0)。
修改後的隨機版本
free_cells = [
    (x, y)
    for y in range(CELL, HEIGHT - CELL, CELL)
    for x in range(CELL, WIDTH - CELL, CELL)
    if (x, y) not in body
]

return RNG.choice(free_cells)
它可以拆解成比較容易理解的普通 for 迴圈：
free_cells = []

for y in range(CELL, HEIGHT - CELL, CELL):
    for x in range(CELL, WIDTH - CELL, CELL):
        if (x, y) not in body:
            free_cells.append((x, y))

return RNG.choice(free_cells)
差別是原本找到第一個空格就：
return (x, y)
現在則先把所有空格加入：
free_cells.append((x, y))
最後才從所有合法空格中隨機挑選：
return RNG.choice(free_cells)

2.蛇身的「生成位置」與「圖片方向」由不同部分控制。
初始蛇身位置
位於 [game.py (line 20)](D:/Lab/lab03-snake-trio/src/snake_trio/game.py:20)：
START_BODY = [
    (200, 200),  # 蛇頭
    (180, 200),  # 第一節身體
    (160, 200),  # 第二節身體
]

START_DIRECTION = (1, 0)
三節的 y 都是 200，x 則依序向左，所以初始蛇身水平排列：
body ← body ← head → 移動方向

