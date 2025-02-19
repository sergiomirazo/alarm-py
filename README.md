# alarm-py

**Project:** alarm-py  
**Version:** 1.1.0  
**Date:** OCT/12/2023  
**Author:** Sergio Mirazo  

---

## Description:

`alarm-py` is a simple alarm application developed in Python that alerts you when it's time to go to work or attend a scheduled activity. This application allows the user to specify the days of the week when the alarm should be activated, the time, and the subject of the alarm. Additionally, it saves the configurations to a file for later use.

### Features:

- **User Registration and Login:** Users can register with a username, password, and choose an avatar from a selection of images.
- **Attractive GUI:** Utilizes Tkinter for a user-friendly and colorful interface with a modern design.
- **Alarm Creation:** Users can create alarms with a specified subject, time, and days of the week.
- **Alarm Configuration:** Allows selection between 12-hour format (AM/PM) or 24-hour format, and enables day selection for the alarm activation.
- **Multiple Alerts:** Alarms are audible and display a message on the screen when triggered.
- **Visual Enhancements:** Buttons feature rounded edges, thematic emojis, and effective contrast against a dark background.
- **Responsive Design:** Windows and interface elements adapt to various screen configurations.

### Requirements:

- Python 3.x
- Tkinter
- Pillow (for image handling)

### Installation:

1. Clone this repository or download the code.
2. Ensure you have Python 3.x installed.
3. Install Pillow if you haven't already:
```
   pip install Pillow
```
4. Run the `main.py` file to launch the application:
 ```
   python main.py
```

### Usage:

Start the application and navigate to the registration screen to create a new account.
Once registered, log in with your credentials.
Create alarms by specifying the time, days, and desired subject.
Alarms will trigger according to the established settings, alerting the user with a sound and a message.