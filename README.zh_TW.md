<p align="center">
  <a href="#">
    <img src="https://github.com/onuratakan/gpt-computer-assistant/assets/41792982/176c8ddb-219e-444e-8782-1f8c37a92678" alt="Logo" width="250" >
  </a>

  <h3 align="center">GPT 電腦助手</h3>

  <p align="center">
    適用於 Windows、MacOS 和 Ubuntu 的 gpt-4o
    <br />
   <a href="https://github.com/onuratakan/gpt-computer-assistant/wiki"><strong>文件</strong></a>
   .
    <a href="https://github.com/onuratakan/gpt-computer-assistant/#Capabilities"><strong>探索功能 »</strong></a>
    <br />
    </p>
    <br>
    <p align="center">
     <a href="https://github.com/onuratakan/gpt-computer-assistant/wiki">
   <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="windows">
   </a>
   <a href="https://github.com/onuratakan/gpt-computer-assistant/wiki">
   <img src="https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white" alt="macos">
   </a>
    <a href="https://github.com/onuratakan/gpt-computer-assistant/wiki">
   <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="linux">
   </a>
  <br> 

  </p>
  <p align="center">
  <a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made_with_python">
  </a>
  .
  <img src="https://static.pepy.tech/personalized-badge/gpt-computer-assistant?period=total&units=international_system&left_color=grey&right_color=blue&left_text=PyPI%20Downloads" alt="pypi_downloads">
  </p>


  <p align="center">
   <a href="https://discord.gg/qApFmWMt8x"><img alt="Static Badge" src="https://img.shields.io/badge/Discord-Join?style=social&logo=discord" width=150></a>
   <a href="https://x.com/GPTCompAsst"><img alt="Static Badge" src="https://img.shields.io/badge/X-Join?style=social&logo=x" width=100></a>

  </p>

|[ENGLISH](README.md)|[簡體中文](README.zh_CN.md)|正體中文

# GPT 電腦助手
你好，這是一個將 ChatGPT MacOS 應用程式提供給 Windows 和 Linux 的替代工作。因此，這是一個全新且穩定的項目。您可以輕鬆安裝為 Python 庫，但我們將準備一個管道，以提供本機安裝腳本（.exe）。
由 <a href="https://github.com/Upsonic/Tiger"><strong>Upsonic Tiger 🐅</strong></a> 提供支持的功能集成中心。

## 安裝 && 運行
需要 >= Python 3.9
```console
pip3 install gpt-computer-assistant
```

```console
computerassistant
```



### 示範影片（1 分鐘）

https://github.com/onuratakan/gpt-computer-assistant/assets/41792982/26ae3624-e619-44d6-9b04-f39cf1ac1f8f



## 使用案例

<table>
  <tr>
    <td><img src="https://github.com/onuratakan/gpt-computer-assistant/assets/41792982/b4a4f11e-5588-4656-b5d7-b612a9a2855b" alt="Take Meeting Notes" width="500"/></td>
    <td><img src="https://github.com/onuratakan/gpt-computer-assistant/assets/41792982/49eeac70-b33a-4ec4-8125-64127621ed62" alt="Daily Assistant" width="500"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/onuratakan/gpt-computer-assistant/assets/41792982/10b69a18-033c-4d81-8ac9-f4e3c65b59c3" alt="Read Docs" width="500"/></td>
    <td><img src="https://github.com/onuratakan/gpt-computer-assistant/assets/41792982/0f483bae-ffaf-4311-8653-c0dc64fb5ebe" alt="Coding Assistant" width="500"/></td>   

  </tr>
</table>



## 路線圖

| 功能                             | 狀態         | 目標發布      |
|---------------------------------|--------------|--------------|
| 清除聊天記錄                     | 已完成       | 2024 年第二季度|
| 長音訊支持（拆分 20mb）          | 已完成       | 2024 年第二季度|
| 文本輸入                          | 已完成       | 2024 年第二季度|
| 僅文本模式（靜音）                | 已完成       | 2024 年第二季度|
| 添加配置文件（不同聊天）           | 已完成       | 2024 年第二季度|
| 更多關於助手狀態的回饋             | 已完成       | 2024 年第二季度|
| **新 UI**                        | 計劃中       | 2024 年第二季度|
| **我們的自訂代理基礎設施**        | 計劃中       | 2024 年第二季度|
| **本機應用程式，exe，dmg，appimage** | 計劃中       | 2024 年第二季度|
| **DeepFace 集成（臉部識別）**      | 計劃中       | 2024 年第二季度|
| **本地模式（使用 Ollama，語音和視覺模型）** | 計劃中       | 2024 年第二季度|


#### 代理基礎設施 | 即將推出

```python
from gpt-comptuer-assistant import crew, agent

coder = agent("你是一名高級 Python 開發者")

manager = agent("你是一名高級項目經理")

assistant = crew(
 [coder, manager]
)

assistant.gui()
```




## 功能
此時我們擁有許多基礎設施元素。我們只是希望提供 ChatGPT 應用中已經存在的所有功能。

| 功能                              | 描述                          |
|-----------------------------------|-------------------------------|
| **螢幕讀取**                      |            OK                 |
| **麥克風**                        |            OK                 |
| **系統音訊**                      |            OK                 |
| **記憶體**                          |            OK                 |
| **打開和關閉應用程式**              |            OK                 |
| **打開一個 URL**                  |            OK                 |
| **剪貼簿**                        |            OK                 |
| **搜尋引擎**                      |            OK                 |
| **編寫和運行 Python**            |            OK                 |
| **編寫和運行 SH**                |            OK                 |
| **使用你的 Telegram 帳戶**        |            OK                 |
| **知識管理**                      |            OK                 |







## 用法

![options](https://github.com/onuratakan/gpt-computer-assistant/assets/41792982/20972b1e-6d4f-4314-8470-f2fcf79b6e6d)



** 第一次單擊包含麥克風或系統音訊的選項後，需要再次單擊相同選項以停止。



## 貢獻者

<a href="https://github.com/onuratakan/gpt-computer-assistant/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=onuratakan/gpt-computer-assistant" />
</a>