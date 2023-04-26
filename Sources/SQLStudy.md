# Study 

## Download MySQL

1. Downloads MySQL Community Version from the website, the link is attached below as the red circle shows.

> https://www.mysql.com/downloads/

![image-20220926182803168](C:\Users\shaon\AppData\Roaming\Typora\typora-user-images\image-20220926182803168.png)

2. After the download, all the way to this page.

   ![image-20220926183052228](C:\Users\shaon\AppData\Roaming\Typora\typora-user-images\image-20220926183052228.png)

   Remember the port number

   

3. Set up the password as u want

   ![image-20220926183241372](C:\Users\shaon\AppData\Roaming\Typora\typora-user-images\image-20220926183241372.png)

4. Remember the Service Name at this page

   ![image-20220926183315568](C:\Users\shaon\AppData\Roaming\Typora\typora-user-images\image-20220926183315568.png)

5. Execute or next to the end

## Start and Stop

1. After the install, we should know how to start and stop.

   1. Windows Key+R to open the cmd line and enter __services.msc__

      The following should be opened.

      ![image-20220926184106896](C:\Users\shaon\AppData\Roaming\Typora\typora-user-images\image-20220926184106896.png) Scroll down to find the MySQL80, then u can right click and decide to stop or start.

   2. Using cmd command to open and stop

      __net start mysql80__

      __net stop mysql80__

      1. Open command prompt as admin

      2. Try the upper code at command prompt and the screen should shown as following

         ![image-20220926184809127](C:\Users\shaon\AppData\Roaming\Typora\typora-user-images\image-20220926184809127.png)

         This indicate that ur successfully stop and start.

   ## Client Link