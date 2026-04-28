


to run this file copy example.env to create your .env file


# commands to push, pull, update code on github
| command | description | Notes|
|--|--|--|
| ``` git init ``` | Initialize| before committing the folder to git for the first time|
|``` git add . ```| add files| Add all files to staging|
|``` git add -u ```| add files, update| updates to delte files in github whihc are locally deleted|
| ``` git commit -m "Initial commit" ```| commit changes |Create a repo in git before this step|
|``` git commit -am "My update message" ``` |for future commits: eg:| -a (All): Tells Git to automatically "stage" any changes to files it already knows about.| 
|``` git remote add origin https://github.com/USERNAME/REPOSITORY.git ```|Add the remote repository |(replace USERNAME and REPOSITORY)|
|``` git push -u origin main ``` |Push to GitHub | -u stands for upstream. You only use this the very first time you push a new branch to GitHub.|
|rm -rf .git| Clean out the copied Git history||
| ``` git push ```|future Push to GitHub| |
| ``` git checkout -b add-dependencies```|To create a branch: ||



- virtual environment

- Create a virtual environment: Open your terminal, navigate to your project directory and run ``` python3 -m venv .venv ```

- Activate the environment:  ``` source risk_env/bin/activate ```



- Install packages with a requirements.txt file - preferable  ``` pip install -r requirements.txt ```