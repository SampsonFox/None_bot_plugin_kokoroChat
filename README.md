## ChatGPT_API_chat_plugin_kokoro

### Introduction

This plugin is a chat application that utilizes the ChatGPT API and is based on the NoneBot platform. Its functionalities go beyond daily chat, as it allows users to create and use presets as well as view their chat logs history.

***

### Commonds

if you want to chat with kokoro, just sent kokoro a message in **private chat** or in **group chat**. In addition, you will need to **mention kokoro** (@), if you want to talk to kokoro in group chat.

All chat will start with a default preset, if you want to start without a preset, you will need to use **pure mode**.

Only input what inside the `f''`

```python
f'结束对话' # finish current session and return the ID of the closed session.
```

```python
f'查看对话 {sessionID}' # check the chat log based on the session ID.
```

```python
f'对话列表' # search and the least 20 chat logs related to the sender
```

```python
f'继承对话 {sessionID}' # 1.copy a session from anyone's history chat log。
                       # 2.continue chating under the copied session.
```

```python
f'纯净模式' # pure mode, start without a preset, you can use this to create a new preset.
```

```python
f'预设列表' # search all presets. This plugin will provide one default catgirl perset.
```

```python
f'生成预设 {sessionID} {presetName}' # Turn the selected session to a preset
```

```python
f'使用预设 {presetName}' # Load a preset
```

```python
f'gpt帮助' # get help in chat app
```
