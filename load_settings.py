from ast import literal_eval
from configparser import ConfigParser, NoSectionError, NoOptionError, DuplicateSectionError
from copy import deepcopy
from flask import flash, redirect, url_for
from socket import gethostname, gethostbyname


config = ConfigParser()
default = {"username": "admin", "password": "password", "universemin": 1, "universemax": 10,
           "sacndict": {1: [1], 2: [2]}, "artnetdict": {3: [3], 4: [4]}, "sacn_to_artnet": False,
           "artnet_to_sacn": False, "broadcast": False, "artnet_port": 6454, "sacn_port": 5568, "server_port": 4000,
           "ip": gethostbyname(gethostname()), "per_channel_priority": True, "merge_sacn": True, "merge_artnet": True,
           "artnet_priority": 100}


def load_settings(variable, category="Main"):
    """ Check if variable is a literal. If it is, it will be converted to a variable """
    try:
        output = literal_eval(open_settings(category, variable))
    except (ValueError, SyntaxError):
        output = open_settings(category, variable)
    return output


def open_settings(category, name):
    """ Try to access variable from the config file. If it does not exist or is not readable, take the default value """
    try:
        config.read_file(open("settings.dat", "r"))
        output = config.get(category, name)
    except (NoSectionError, NoOptionError):
        output = deepcopy(default[name])
    except OSError as Error:
        try:
            file = open("settings.dat", "w")
            file.close()
            config.read_file(open("settings.dat", "r"))
            output = config.get(category, name)
        except Exception as Error:
            print(Error, "Could not create settings file")
            output = deepcopy(default[name])
    return output


def save_settings(category, name, variable):
    """Store a new variable to the settings file or overwrite an existing one"""
    try:  # If section already exists, pass
        config.add_section(category)
    except DuplicateSectionError:
        pass

    config.set(category, name, f"{variable}")  # Set up configparser for saving.
    try:  # Show an error if it is not possible to save.
        file = open("settings.dat", "w")
        config.write(file)
        file.close()
    except(FileNotFoundError, OSError):
        flash("Can not open settings file. Maybe it is write-protected?", "danger")
        return redirect(url_for("home"))


def delete_category(category):
    try:
        file = open("settings.dat", "w")
        config.remove_section(category)
        file.close()
    except (NoOptionError, NoSectionError, OSError):
        pass
