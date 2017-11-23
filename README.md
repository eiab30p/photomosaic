# Photomosaic
# By Eddy Verde and David M


### **Description :** <br>
>    Below are going is the README.md file describing plug-ins, installs,
     environment variables, and any other process that is taken during the
     duration of this application.

>   We are creating a photomasic application using python and openCV. We will search through a database creating
    gathering images. This is only if the images are new. Once the photos are done. We will randomly select
    images in the database to create a photomosaic.

### **GIT Commands** <br>
>   Below are going to be a list of git commands regarding the code.

### REMEMBER TO PULL AND PUSH OFTEN!!!!!!

Git Commands                                                 | Description
-------------------------------------------------------------|--------------------------------------------------------------
git clone < http url>                                        | Use this command to clone the repository that you want.
git pull                                                     | Gets the latest code from the branch you are in. Conducts an auto merge from prior code to your code if there is an merge conflict the terminal will notify you and which file have a merge conflict. When a conflict arises contact person who last push to work through the merge
git push(optional: ": < tag >")                              | Pushes the latest the the branch you are in. The tag is great to create versions for each push
git merge < branch name>                                     | Great for combining branches. You will use this when you want to combine the master branch with your current branch
git stash                                                    | Stores your current changes in a queue (FIFO) while you do a pull or other change.
git stash pop                                                | Applies the changes you have just stored
git checkout < branch name >                                 | This will direct you to the branch you want to be in.
git branch < branch name >                                   | Will create a NEW branch
git branch --list                                            | Will list out all the branches
git push -u origin < branch name >                           | Will push a local branch to the repository
git status                                                   | list all files you have changes, added, deleted
git add                                                      | add a change to a commit best to do one at a time if you want to do multiple commits
git commit -a                                                | add all modifications to a single commit. Appears new terminal in vim. to add a message press "i" then type message. When done click the escape key and then enter ":wq" to leave the vim
git commit -m "< message >"                                  | If you have already added all modified changes to a commit you can just add a message prior to push
git push origin <branch name >                               | To show the branch in a repo


#### Examples :

* Most common flow of commands to add need changes. Both options are the same
    1. git add < files > >>> git commit -m " new code" >>> git pull >>> git push
    2. git commit -a >>> vim view >>> git pull >>> git push

* Going to a branch
    1. git checkout Eddy

* Getting the latest code into the Eddy branch after committing changes
    1. git checkout master >>> git pull >>> git checkout Eddy >>> git merge master

* Updating master code after committing changes in different branch
    1. git checkout master >>> git pull >>> git checkout testing >>> git pull >>> git checkout master >>> git merge testing

* Pulling changes prior to committing the change
    1. git stash >>> git pull >>> git stash pop

* Creating and pushing new branch into repository
    1. git branch new-ui >>> git commit -a >>> vim >>> git push -u origin new-ui


INSTALL
pip install beautifulsoup4

Used for images
https://www.thoughtco.com/images-of-us-presidents-4123096
I got all the photos from here and then a typed a little code toresize all photos to 500 by 500.
Once that is completed I got the json filr using the below link since I had issues with the dlob file
for windows.

used for points
https://www.faceplusplus.com/landmarks/
Need to convert Json into normal list

After I got the points I did the triangle thing. using the below site to understand the
algorithm used.

After this I worked on the translation part where I warped and scaled, moved the image to fit the points.





