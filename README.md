# Bitkub-Bot-Trade
### BOT Auto Trading
BOT ตัวนี้ทำขึ้นจากความขี้เกียจในการเฝ้า Graph ทำให้เสียเวลาทำมาหากิน หลักการทำงานก็คือ เราได้สัญญาณซื้อ/ขายจาก TraindingView และโยน Json ไปให้ BOT ผ่าน ngrok ซึ่งคำสั่งซื้อหรือคำสั่งขายจะส่งไปยัง Bitkub ทันที


##### สิ่งที่ต้องมีให้พร้อมก่อนใช้งานหากต้องการให้ BOT รันที่เครื่องตัวเอง
1. OS (Window,Ubuntu,Macos) ที่จะต้องติดตั้ง Python3 ให้เรียบร้อย และติดตั้ง library (bitkub,flask)
2. ตัว Trigger สัญญาณซื้อ/ขาย ผมใช้ TradingView และ CDC Action Zone V3 2020
3. Ngrok.com เพื่อสร้าง Endpoint ชี้มายังเครื่องของคุณเอง (ngrok http -hostname=xxxxx.ngrok.io 8899)

##### กำหนดค่าเบื้องต้น
1. ที่ไฟล์ bitkub_v2.py คุณจะต้องเปลี่ยน API_KEY และ API_SECRET ที่คุณต้องสร้างมาจาก API ของ Bitkub
2. ที่ไฟล์ webtrade.py เปลี่ยนค่า buy_value=3000 เป็นจำนวนเงินที่คุณจะซื้อต่อครั้ง (3000 บาทต่อไม้)   
2. คำสั่งรันโปรแกรม python3 webtrade.py
3. สร้าง Alert ซื้อ บน TradingView (TimeFrame = 4 ชั่วโมง หรือ มากกว่า) โดยกำหนดสัญญาณซื้อ
   3.1 Condition = CDC Action Zone และเลือก Buy Alert
   3.2 กดปุ่ม Once Per Bar Close
   3.3 WEB Hook URL == https://xxxxx.ngrok.io/tradingview
   3.4 Alert Name = Buy - BTC
   3.5 Message = {"cmd": "buy","symbol": "{{ticker}}","price": {{close}}}
4. สร้าง Alert ขาย บน TradingView (TimeFrame = 4 ชั่วโมง หรือ มากกว่า) โดยกำหนดสัญญาณขาย
   4.1 Condition = CDC Action Zone และเลือก Sell Alert
   4.2 กดปุ่ม Once Per Bar Close
   4.3 WEB Hook URL == https://xxxx.ngrok.io/tradingview
   4.4 Alert Name = Sell - BTC
   4.5 Message = {"cmd": "buy","symbol": "{{ticker}}","price": {{close}}}

##### ข้อจำกัด
* ~~ทำงานเฉพาะเหรียญที่มีตัวย่อ 3 ตัวอักษร~~
* จะมีการซื้อ/ขายได้ 1 ไม้ต่อเหรียญ
* หากจะรัน 24 ชม. คุณจะต้องเปิดเครื่องทิ้งไว้ตลอด