# ECED4900 Ultrasound Transducer Build Tracker

This is the project work for the ECED4900 Course to get the respositry.
The whole project file belongs to Shaonan Hu, Jiahao Chen, Yilun Peng and Jiawei Yang.

## Getting Started

### Setup Respository

The first step is to get the template onto your local machine.
You can start by making an empty local repository:
```
$ mkdir -p /path/to/your/local/repo
$ cd /path/to/your/local/repo
$ git init
```
Now you can configure a remote connection to the template repository and pull its history into yours.
```
$ git remote add upstream https://github.com/ApplyKCL/SNYProject.git
$ git pull upstream main
```
Your local repository should now be populated with the contents of the template, and you should see commits from yours truly when you run `git log`.

### Branches

This will be eaiser not mess to the whole work and keep one clean version in the resporitry.

You can create and checkout a branch named "Jiahao" like this:
```
$ git checkout -b Jiahao
```
### Getting Updates

As the project going, all the files in the project may need to be revised or add new things in the template. If so, there will be new commits on the upstream repo that you'll need to merge into yours.
If there are changes, you'll get a notification from Team chat tools, Teams, Wechat, etc.
You'll look something like this:

First, pull the changes form the upstream.
```
$ git checkout main
$ git pull upstream main
$ git log # print the log to review the changes
```
Enter `q` will allow you to exit from `git log`.
Remember, you can run `git status` to check the state of your repository, including what branch you're currently on.

Then, merge the changes into your working branch.
```
$ git checkout Jiahao # or whatever you called your working branch for the project
$ git merge main
```
### Uploading the work

After the any change you made in software part, please verify with software team member, Shaonan Hu or Jiahao Chen. Otherwise, please following the below steps:
```
$ git checkout main
$ git add --all
$ git commit -m "<commit_message>"
$ git status # To check all the files has been uploaded correctly
```

Using `git log` to check the push you made had been finished.

## Reference
- Git Command [cheat sheet](https://dzone.com/articles/top-20-git-commands-with-examples)

## Thank you for your reading.
 If you have any further question, welcome to talk to owners.
 Have a wonderful day!
