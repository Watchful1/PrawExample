This repository is partly a collection of useful bits of code and design techniques for my own reference, and partly an explanation of how I arrived at these techniques. This is not intended as a tutorial, but a collection of best practices.

I've been writing reddit bots since 2016 and I've learned a lot since my initial attempts, especially as they have gotten larger and more complicated. Some examples include [RemindMeBot](https://github.com/Watchful1/RemindMeBot) and [UpdateMeBot](https://github.com/Watchful1/UpdateMeBot).

---

##Logging

The single most important thing you can do when starting a new bot is to set up and include logging for every important action the bot does. This way, when something breaks and you only notice hours or days later, you can easily go back and figure out exactly what went wrong. Read how I set up logging [here](src/logging_setup.py).

---

##Configuration

To run your bot, you need the credentials of the reddit account somewhere, but you don't want them to show up online if we upload our code somewhere, so we will use a config file. You can also put other stuff in the config file, like the subreddit your bot is going to run in, but I tend to put that directly in the code. I don't want to forget that I have something configured one way on my computer and a different way on my server. Like with logging, python has its own configuration setup, which is the one PRAW uses. Rather than setup a config file for each project, I just reuse PRAW's. More details [here](src/config_setup.py)

---

##Saving data between runs

It's important to save data information about what your bot has already done and what it's working on so that if it crashes, or you have to stop it, it doesn't lose its place. There are a bunch of different ways to do this, of varying complexity. This is an area where its easy to make things a bunch more complicated than they need to be, so it's a good idea to think carefully about how to do this. I break down the various ways I use [here](src/saving/SAVING.md).
