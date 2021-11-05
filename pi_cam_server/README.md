# Button + PiCamera + Google Vision ML + PiZero

TODO: wiring diagram

## To run this code:

###### 1. Update system packages:

```
$ sudo apt update
$ sudo apt upgrade
```

###### 2. Install dependencies:

```
$ pip3 install --upgrade google-cloud-vision
$ pip3 install --upgrade pillow
```

###### 3. Download Google Cloud Auth file:

Get the Google Cloud authentication JSON file from the [class Google Drive folder](https://drive.google.com/drive/folders/1q5ubmlic-o_oINPMw7kb9pr6ub2ZcMOs). This should be placed in the root `/home/pi` folder on the Pi.

###### 4. Make a folder for the photos/JSON to be served from:

```
$ mkdir /home/pi/SHARE
```

###### 5. Run program:

In one terminal window, run the main program code.

```
$ python3 btn-cam-ml.py
```

In another terminal window, navigate to the `/home/pi/SHARE` folder and start the `SimpleHTTPServer`.

```
$ cd /home/pi/SHARE
$ python -m SimpleHTTPServer
```

With default options, the server created by `SimpleHTTPServer` should be accessible by visiting the URL `http://<yourdevicehostname>.local:8000` from a device on the same local network.
