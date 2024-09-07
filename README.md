#### Reference:
+ [qsed](https://github.com/JiaRu2016/qsed)
+ [StockQuant](https://github.com/Gary-Hertel/StockQuant)
+ [easyquotation](https://github.com/shidenggui/easyquotation)


<!--
    事件驱动引擎使用了多个线程来实现功能:
    
    + main
      + EventEngine.__run() # 从 queue 中 get 事件，并处理
        + EventEngine.__process() # 处理 get 到的事件

      + BaseDataEngine.push_data() # 向 queue 插入 data

      + ClockEngine
-->
