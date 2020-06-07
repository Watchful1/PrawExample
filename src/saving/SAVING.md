There are a number of ways to save data between runs of your bot. The simplest by far is just not saving anything. If you can structure your bot to, for example, only operate on unread messages, and then mark a message as read when you're done processing it, there's no need to save which messages you've processed. Or by only operating on comments submitted after the bot has started running. This might mean you will miss some comments while the bot is turned off, but it saves a lot of work, so it might be worth it.

If you do need to save something, consider doing it on reddit rather than locally. Either by using reddit's save functionality, writing to a wiki page, or even hiding info in plain sight in a comment. I detail these [here](reddit_saving.py).

pickle

database/sqlite

sqlalchemy