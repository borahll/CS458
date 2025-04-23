1- To run the flutter application only:
Install flutter
Navigate to project2 folder
Run "flutter pub get" (to install dependencies)

Start an emulator (Android Studio, Swift) 
Then run flutter with "flutter run" command
In one terminal

2- For appium:
Install appium and its drivers, drivers (appium flutter driver) can be installed from: https://github.com/appium/appium-flutter-driver
Command: appium driver install --source=npm appium-flutter-driver 

After all these navigate to project2/automation_tests folder
Do yarn install (to install yarn: npm install --global yarn, check version with yarn -v it should be 4.6.0)
After those either run "yarn appium" or directly "appium" to start the appium server
In a second terminal

3- For testing:
Navigate to project2/automation_tests/tests folder
Directly run test.py with "python test.py"
See the results there (also logs are available in the second terminal where appium server runs)
