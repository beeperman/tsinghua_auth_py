# tsinghua_auth_py
A simple python3 headless browser script that helps you automatically login the new tsinghua auth. (Wired)

Python package needed

- selenium

System package needed

- PhantomJS

Edit `login.py` and add your own credentials before running the bash script `autologin` to log in.

```bash
# change username and password in the python script
vim login.py
# make the autologin bash script runnable and run it
chmod +x autologin
./autologin
```
