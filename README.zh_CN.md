<p align="center">
  <a href="#">
    <img src="https://github.com/user-attachments/assets/df1a3ec1-8c03-43c8-9432-c71358c35b9e" >
  </a>
  <br>

<p align="center">

  <a href="https://docs.gca.dev">
    <img src="https://github.com/user-attachments/assets/c60562bf-540e-47d9-b578-994285071128" width="250">
  </a>

</p>

  <p align="center">
    <a href="https://www.producthunt.com/posts/gpt-computer-assistant?embed=true&utm_source=badge-top-post-badge&utm_medium=badge&utm_souce=badge-gpt&#0045;computer&#0045;assistant" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/top-post-badge.svg?post_id=465468&theme=dark&period=daily" alt="GPT&#0032;Computer&#0032;Assistant - Create&#0032;intelligence&#0032;for&#0032;your&#0032;products | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>
    .
    <a href="https://discord.gg/qApFmWMt8x"><img alt="Static Badge" src="https://img.shields.io/badge/Discord-Join?style=social&logo=discord" width=150></a>
    .
    <a href="https://x.com/GPTCompAsst"><img alt="Static Badge" src="https://img.shields.io/badge/X_App-Join?style=social&logo=x" width=150></a>
  </p>


  <p align="center">
    <br />
    Intelligence development framework
    <br />
    </p>
    <br>

  <p align="center">
  <a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made_with_python">
  </a>
  .
  <img src="https://static.pepy.tech/personalized-badge/gpt-computer-assistant?period=total&units=international_system&left_color=grey&right_color=blue&left_text=PyPI%20Downloads" alt="pypi_downloads">
  </p>


|[ENGLISH](README.md)|简体中文|[正體中文](README.zh_TW.md)|[TÜRKÇE](README.TR.md)

# GPT 计算机助手
你好，这是一个将 ChatGPT MacOS 应用程序提供给 Windows 和 Linux 的替代工作。因此，这是一个全新且稳定的项目。此时，您可以轻松地将其作为 Python 库安装，但我们将准备一个流水线来提供本机安装脚本 (.exe)。

由 <a href="https://github.com/Upsonic/Tiger"><strong>Upsonic Tiger 🐅</strong></a> 提供支持的功能集成中心。

## 1.安装 && 运行
**需要 Python 3.10 或者 3.11**
```console
pip install 'gpt-computer-assistant[base]'
pip install 'gpt-computer-assistant[api]'
```
要想运行 gpt-computer-assistant, 简单输入
```console
computerassistant --api
```

<p align="center">

  <a href="#">
    <img src="https://github.com/user-attachments/assets/890b4e0a-4484-4870-a158-2d365b0d969e" >
  </a>

</p>




<p align="center">
<br>
  <br>
  <br>
  <br>
  <br>
</p>

## 2. 大语言模型 设置

```python
from gpt_computer_assistant.remote import remote

remote.save_models("gpt-4o")
remote.save_openai_api_key("sk-**")
```

<p align="start">

  <a href="https://docs.upsonic.co/gca/dev_guides/llm_settings">
    <img src="https://github.com/user-attachments/assets/a75c8ddf-f9df-436b-9dc8-c5220211e15e" width="150">
  </a>

</p>



<p align="center">
<br>
  <br>
  <br>
</p>

## 3. 角色特征 API


```python
# 助手的名称:
remote.change_name("X Intelligence")

# 助手的开发人员角色:
remote.change_developer("X Company")
```

<p align="start">

  <a href="https://docs.upsonic.co/gca/dev_guides/characteristic">
    <img src="https://github.com/user-attachments/assets/d7e02ac6-e40c-4b35-8e65-4621bf3fb9a1" width="150">
  </a>

</p>



<p align="center">
<br>
  <br>
  <br>
</p>

## 4. 连接你自己的函数API


```python
# 安装一个库:
remote.install_library("numpy")



# 以Python函数的形式添加功能:
@remote.custom_tool
def my_server_status() -> bool:
  """
  Check the server status.
  """
  return True
```



<p align="center">
<br>
  <br>
  <br>
</p>



## 5. 与 用户 API 交互


### remote.input
与助手交谈，了解用户和计算机。使用此 api，您可以创建一个咨询流程。

```markdown
`Hi, look to user window and return which app using now`

`Ask user to is user need any kind of supoprt`

`Extract the user redis config file.`
```

有了这些问题，您就可以根据自己的需要找到一条捷径。

**您可以从用户电脑收集信息或直接从用户或用户电脑获取信息.**

```python
output = remote.input("Extract the user redis config file.", screen=False)
print(output)
```


<p align="start">

  <a href="https://docs.upsonic.co/gca/dev_guides/interact">
    <img src="https://github.com/user-attachments/assets/81614347-ab85-4965-9b77-225d0f2961e9" width="150">
  </a>
  .
  <a href="https://docs.upsonic.co/gca/dev_guides/interact">
    <img src="https://github.com/user-attachments/assets/ecaa7590-f4c5-4eda-9482-462cef54aeff" width="150">
  </a>
  .
  <a href="https://docs.upsonic.co/gca/dev_guides/interact">
    <img src="https://github.com/user-attachments/assets/0f35df10-b32e-4fa1-936e-b336be46b1bd" width="150">
  </a>

</p>



<p align="start">

  <a href="https://docs.upsonic.co/gca/dev_guides/interact">
    <img src="https://github.com/user-attachments/assets/a893c50c-3ede-4b42-90ee-92e2fea82120" width="150">
  </a>

</p>


<p align="center">
<br>
  <br>
  <br>
</p>


## 使用
![options](https://github.com/onuratakan/gpt-computer-assistant/assets/41792982/37d34745-ae4b-4b37-9bfa-aec070c97897)





## 使用案例

<img alt="Screenshot 2024-08-13 at 18 33 52" src="https://github.com/user-attachments/assets/8f994160-893a-4f56-bbf0-4a7aa87af650">






## 路线图

| 功能                             | 状态         | 目标发布      |
|---------------------------------|--------------|--------------|
| 清除聊天记录                     | 已完成       | 2024 年第二季度|
| 长音频支持（拆分 20mb）          | 已完成       | 2024 年第二季度|
| 文本输入                          | 已完成       | 2024 年第二季度|
| 仅文本模式（静音）                | 已完成       | 2024 年第二季度|
| 添加配置文件（不同聊天）           | 已完成       | 2024 年第二季度|
| 更多关于助手状态的反馈             | 已完成     | 2024 年第二季度|
| 本地模型的视觉和文本 (使用ollama和视觉模型)  | 已完成  |2024年第二季度        |
| **我们可以自定义的 Agent 基础架构**              | 已完成      | 2024 年第二季度      |
| 支持 Groq 模型  | 已完成  | 2024 年第二季度      |
| **添加自定义工具**  | 已完成  | 2024 年第二季度       |
| 界面可点击 (文本和图标)              | 已完成      | 2024 年第二季度       |
| 新的 UI  界面            | 已完成      | 2024 年第二季度       |
| 系统原生应用程序, exe, dmg              | 已完成     | 2024 年第三季度         |
| **在长篇响应中协同不同声音模型**              | 已完成     | 2024 年第二季度       |
| **当你完成通话时，自动停止录音**              | 已完成     | 2024 年第二季度       |
| **唤醒词**              | 已完成     | 2024 年第二季度      |
| **持续性对话**              | 已完成   | 2024 年第二季度   |
| **Adding more capability on device**              | 已完成     | 2024 年第二季度       |
| **本地 TTS 模型**              | 已完成    | 2024 年第三季度        |
| **本地 STT 模型**              | 已完成    | 2024 年第三季度        |
| 托盘菜单              |已完成     | 2024 年第三季度        |
| **全局快捷键**              | 即将到来     | 2024 年第三季度    |
| DeepFace 集成 (面部识别)                    | 计划中  | 2024 年第三季度         |







## 功能
此时我们拥有许多基础设施元素。我们只是希望提供 ChatGPT 应用中已经存在的所有功能。

| 功能                              | 描述                          |
|-----------------------------------|-------------------------------|
| **本地视觉LLM模型 (Ollama)**                    |            OK                    |
| 本地 文本转语音                    |            OK                    |
| 本地 语音转文本                    |            OK                    |
| **屏幕阅读**                    |            OK                    |
| **点击屏幕上的文本或图标**                    |            OK                    |
| **移动到屏幕上的文本或图标**                    |            OK                    |
| **输入内容**                    |            OK                    |
| **按下任意键**                    |            OK                    |
| **鼠标滚动**                    |            OK                    |
| **麦克风**                     |            OK                    |
| **系统音效**                  |            OK                    |
| **记忆**                         |            OK                    |
| **打开和关闭App**             |            OK                    |
| **打开URL链接**                     |            OK                    |
| **剪贴板**                       |            OK                    |
| **搜索引擎**                 |            OK                    |
| **输入并运行 Python**     |            OK                    |
| **输入并运行 SH**    |            OK                    |
| **使用你的Telegram 账户**    |            OK                    |
| **知识管理**           |            OK                    |
| **[添加更多工具](https://github.com/onuratakan/gpt-computer-assistant/blob/master/gpt_computer_assistant/standard_tools.py)**           |            ?                    |










### 预设定 Agents
如果你启用它，你的助手将和下面这些团队一起工作:

| Team Name                         | Status                      |
|------------------------------------|----------------------------------|
| **search_on_internet_and_report_team**                    |            OK                    |
| **generate_code_with_aim_team_**                    |            OK                    |
| **[添加一个你自己的](https://github.com/onuratakan/gpt-computer-assistant/blob/master/gpt_computer_assistant/teams.py)**                    |            ?                    |



  <a href="#">
    <img src="https://github.com/onuratakan/gpt-computer-assistant/assets/41792982/ba590bf8-6059-4cb6-8c4e-6d105ce4edd2" alt="Logo"  >
  </a>


## 贡献者

<a href="https://github.com/onuratakan/gpt-computer-assistant/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=onuratakan/gpt-computer-assistant" />
</a>
