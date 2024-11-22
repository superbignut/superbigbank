#### Reference:
+ [qsed](https://github.com/JiaRu2016/qsed)
+ [StockQuant](https://github.com/Gary-Hertel/StockQuant)
+ [easyquotation](https://github.com/shidenggui/easyquotation)
+ [timor](https://timor.tech/api/holiday/)
+ [THSTrader](https://github.com/nladuo/THSTrader)
---
#### bigexample is a simplest event driven code.
#### superbigbank is a slightly simpler event driven code.

---
##### Main logic：
+ superbigdata: Get stock data from web.
+ superbigsttg: Implementation of strategies.
+ superbigcore: Integrate the event_engine, data_engine and strategy into a unified main_engine.
+ superbigbull: Trade api, (temporary fake_trader only).
---
##### Pipeline:
    python pipeline.py
---
##### Conclude:
This repository is a complete event driven quantification framework, and the core code has been completed, including:

+ Use Collection.Queue as the core event queue.
+ Definition, retrieval, and insertion of time events and data events.
+ MainEngine pop events and processes them.
+ Using streamlit for simple data visualization
+ Simulate trading using uiautomaton2.
---
Drawback:

However, this is only a toy-level quant platform and can hardly be used in real，here are some problems:

+ Data has not been cleaned and checked, which poses a risk in use without double check.
+ Insertion of data events is simple which can't meet the requirements of general strategies.
+ Is event driven method really suitable for quant framework?
+ There are many foreseeable bugs in simulated trading.