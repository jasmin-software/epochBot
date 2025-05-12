# Discord Epoch Bot

A simple Discord bot that converts a datetime string into epoch seconds and formats a countdown.

[Bot invitation link](https://discord.com/oauth2/authorize?client_id=1371199566749237492&permissions=274877908992&integration_type=0&scope=bot+applications.commands)

## Usage
```slash
/epoch preMsg: "Countdown begins: " datetime: "2025-05-11 19:30:00" timezone: "America/Vancouver"  format: "R" postMsg: " Get ready!"
```
Note: format is optional, default value is Relative (in 420 days)
![Alt text](./image.png)