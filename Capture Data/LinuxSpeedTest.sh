#Install all the packages needed
sudo apt-get update
sudo apt-get install apt-transport-https
sudo apt-get update
sudo apt-get install dotnet-sdk-6.0
sudo apt-get install dotnet-runtime-6.0
sudo apt-get install aspnetcore-runtime-6.0
sudo apt-get install postfix

#Create the directory for the application to run in
sudo mkdir /home/dotnet
cd /home/dotnet

#Copy the code from this repo
sudo git clone https://github.com/zalimitless/SpeedTestCSharp.git
sudo mkdir /home/dotnet/SpeedTestCSharp/bin/Release/net6.0/Data

#Setup Cron Job
(crontab -l ; echo "* * * * * sudo dotnet /home/dotnet/SpeedTestCSharp/bin/Release/net6.0/DataCapture.dll /home/dotnet/SpeedTestCSharp/bin/Release/net6.0/Data") | sudo crontab -u root -