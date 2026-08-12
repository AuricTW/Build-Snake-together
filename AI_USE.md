# AI Use Record - L1

L1 permits explanations, hints, counterexamples, test ideas, and traceback help. It does not permit AI to write or replace the four final function bodies.

| When | Person asking | Question or prompt | Hint received | Human decision and verification |
|---|---|---|---|---|
| 2026-08-12（時間未記錄） | 李韋宏 | 目前蘋果都會出現在最上方邊緣，請協助找出蘋果位置的生成判斷。 | AI 指出蘋果位置由 `game.py` 的 `choose_food()` 決定。原本的雙層 `for` 迴圈從 `(0, 0)` 開始逐格搜尋，找到第一個不在蛇身上的格子便立即回傳，因此蘋果通常固定出現在左上角。AI 也指出蘋果圖片向上偏移半格，當食物位於最上列時圖片會被視窗裁切，並建議排除牆壁邊緣及從合法空格中隨機選擇。 | 團隊閱讀 `choose_food()`、`new_game()`、吃到食物後重新生成的位置，以及蘋果的繪製程式，確認「固定搜尋第一個空格」與「圖片在頂端被裁切」是兩個不同問題。團隊決定讓食物避開邊緣，並改為從未被蛇身占用的合法格子中隨機選取。 |
| 2026-08-12 16:12 | 李韋宏 | 請講解蘋果要如何從 `for` 迴圈改成 `random`。 | AI 先解釋原本 `range(0, HEIGHT, CELL)` 與 `range(0, WIDTH, CELL)` 的搜尋順序，以及 `return` 會在找到第一個空格時結束函式。接著說明應先用迴圈把所有合法且未被蛇身占用的格子加入 `free_cells`，最後再使用 `RNG.choice(free_cells)` 隨機選取一格。 | 團隊決定保留容易理解的普通雙層 `for` 迴圈，不直接使用較精簡的串列生成式。實作會從 `CELL` 搜尋到 `HEIGHT - CELL`／`WIDTH - CELL`，排除牆壁邊緣，再用 `RNG.choice()` 選取食物。人工檢查目前 `choose_food()` 符合這項決定。 |
| 2026-08-12 16:24 | 李韋宏 | 蛇身生成位置和方向都固定在同一邊，請協助找出控制這部分的程式碼。 | AI 指出原本的初始蛇身由 `START_BODY` 控制，三節座標固定為 `(200, 200)`、`(180, 200)`、`(160, 200)`；移動方向則由 `START_DIRECTION = (1, 0)` 控制。因此蛇身固定水平排列，蛇頭在右側並向右移動。AI 也說明蛇身生成位置與圖片顯示方向是由不同部分控制。 | 團隊確認問題來自固定的起始座標與方向，而不是食物生成或碰撞判斷。這次 AI 只協助定位與解釋；起始位置和方向要如何改動，仍由團隊閱讀程式後自行決定與驗證。 |





If no AI was used, write: `No AI used.`
