# setup guide (for total beginners)

if you've never opened terminal before, this is really for you. setup takes about 20 minutes and you only do it once, and after that editing a reel is basically dragging the video in and answering a couple of questions.

you'll copy and paste a few commands along the way, but you don't need to understand them, i promise.

---

## step 1: get claude

1. you need a paid claude plan (pro or higher). claude code is included.
2. download the claude desktop app from [claude.com/download](https://claude.com/download) and sign in.
3. open the **code** tab. this is claude code, the version of claude that can work with files on your computer.

## step 2: install the video tools (one time, in terminal)

these are the free tools claude uses to cut video and clean audio.

1. open **terminal**: press `cmd + space`, type `terminal`, hit enter.
2. install homebrew (a free app installer for mac). paste this, hit enter, and type your mac password when it asks (you won't see the letters as you type, that's normal):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   when it finishes, it may show you two or three lines under **"next steps"**. copy and run those too.

3. install the video tools:

   ```bash
   brew install ffmpeg node
   ```

   this one takes a few minutes. go make a coffee.

## step 3: install the reel editor (in claude)

go back to the claude code tab and paste this:

```
install the reel editor from github.com/nicolapocock/claude-reel-editor and the hyperframes skills it needs (npx skills add heygen-com/hyperframes), then run its doctor check and tell me if anything is missing
```

claude does the rest, and if it asks permission to run a command, just say yes.

when the check says **all set**, you're done with setup.

## step 4: your first reel

1. film yourself talking to camera on your phone. under 2 minutes is easiest for your first one.
2. airdrop or copy the video to your mac.
3. in claude code, type **"edit this into a reel"** and drag the video file into the chat.
4. **first time only:** claude asks you about your brand, one question at a time (colours, fonts, caption style, sounds). the most useful thing you can give it is a reel you wish you'd made, so have a link ready. this part takes about 5 minutes.
5. claude sends you a link to your **reel review** page (it's private, on your claude.ai account). open it and:
   - press **play rough cut** to watch the edit with your changes, as you make them. use −5s / +5s or drag the bar to move around.
   - **cuts:** tap a word to cut it, or tap a crossed-out word to bring it back. grey dotted words are "um"s and ⏸ chips are pauses it removed; tap one to keep it.
   - **graphics:** keep, change (say what) or drop each one. the little picture shows roughly where it sits.
   - **captions:** tap a word to make it a highlight word, tap **edit** to fix spelling, **merge** to join two.
   - **sound & colour:** listen to your voice before and after, and switch off any sound effect you don't like.
   everything saves as you go, and **undo** is there if you change your mind.
6. press **build preview**, then type **"build preview"** in claude code. about 4 minutes later the draft shows up in the **preview** tab.
7. watch it. if something's off, pause there, describe it, and press **add note at current time**. tell claude when you're done and it fixes those spots.
8. when you're happy, type **"final"**. your 4K reel lands in **movies → reels**. airdrop it to your phone and post.

from the second reel on, it's just steps 1, 2, 3, then 5 to 8.

## want the capcut version too? (optional)

capcut gives you an editable version where every caption and sound effect is its own layer, so you can tweak anything after.

**check this first:** it doesn't work in the us (capcut's connector isn't available there yet) or india (the capcut app isn't available). everywhere else it usually works, and if you're in either place you can skip this and you'll still get the full finished reel.

1. make a free account at [capcut.com](https://www.capcut.com)
2. paste this into claude code:

   ```
   set up the optional capcut route for the reel editor, following references/capcut.md in the skill
   ```

   claude adds capcut's connector for you.

3. log in to capcut once. open terminal, type `claude` and hit enter, then type `/mcp`, pick `capcut_creation`, and sign in with your capcut account when the browser opens. after that, every reel comes with a capcut link as well.

## want to build your own?

if you'd like to understand how this works or build your own version, read [build it yourself](BUILD-IT-YOURSELF.md). it has the prompts i used, in order.

## if something goes wrong

| what you see | what to do |
|---|---|
| `command not found: brew` | close terminal and open it again. if it's still broken, redo step 2.2 and run the "next steps" lines it prints |
| `command not found: ffmpeg` or `node` | run `brew install ffmpeg node` again |
| the check says something is ❌ | paste the whole message into claude code and say "fix this" |
| capcut won't connect | if you're in the us or india, that's capcut's region block and there's nothing to fix. anywhere else, ask claude to log you in to capcut again |
| the review page won't load | open it from the link claude gave you, signed in to your claude.ai account |
| the rough cut won't play | press play rough cut once more (browsers sometimes block the first play). if it still won't, reload the page |
| the edit looks off-brand | tell claude what's wrong ("captions are too small", "never use that font"). it adds it to your brand rules so it doesn't happen again |
| your mac is slow or out of space | you need about 10 GB free. 4k needs 35+ GB, so stick to 1080p if your mac is older |

## changing your style later

your brand lives in two files in a folder called **reels** in your home folder. you never have to open them, you can tell claude what to change ("make my captions one word at a time", "use pink for highlight words") and it updates them.
