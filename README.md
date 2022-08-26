# PodBot
A bot for downloading podcasts from the [Israeli podcast website](https://podcastim.org.il/).

The bot is used for easy and orderly downloading from the site.

## setup
### webdrivers
The bot use selenium, so you need a web driver to run him.
The appropriate webdriver must be downloaded from [here](https://www.selenium.dev/downloads/).
You can also download the webdriver directly from here, but it may not be up to date.

The bot was tested on Firefox, but should also work on Chrome. Of course you need to download the appropriate driver for the browser you are using.

NOTE: The web driver have to be locaded in the main folder (with the script). And the script won't be able to run without it.

### Python packages
The bot also uses several Python packages.
To use it, you will need to install them first:

`pip install selenium`

and

`pip install requests`

in the command line.

You can also download selenium and requests from [PyPi](https://pypi.org/project/selenium/), there are also the webdrivers for the browsers.

And only then can you run the script.
