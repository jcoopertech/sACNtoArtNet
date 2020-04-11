from load_settings import load_settings, save_settings, delete_category
from flask import app, Flask, session, render_template, flash, redirect, url_for, request
from server.forms import LoginForm, ChangePasswordForm
from secrets import token_hex
import networkx as nx
from collections import OrderedDict
from time import sleep
from copy import deepcopy

app = Flask(__name__)


sacn_to_artnet = load_settings("sacn_to_artnet", "sACN")
artnet_to_sacn = load_settings("artnet_to_sacn", "Art-Net")


def check_loopback(input_dict, universe_type="sACN"):
    """Searches for loopbacks caused by multiple conversions from one to the other protocol"""
    """INPUT: The change that was made; the input universe universe_type"""
    """OUTPUT: True if a loop was found
               False if no loop was found"""
    # Add tags, to the universes to create a node map
    if load_settings("sacn_to_artnet", "sACN") is True and load_settings("artnet_to_sacn", "Art-Net") is True \
            or universe_type == "All":
        if universe_type == "sACN":
            artnet_dict = {'Art-Net: ' + str(k): set(map(lambda x: 'sACN: ' + str(x), v))
                           for k, v in load_settings("artnetdict", "Art-Net").items()}
            sacn_dict = {'sACN: ' + str(k): set(map(lambda x: 'Art-Net: ' + str(x), v))
                         for k, v in input_dict.items()}
        elif universe_type == "Art-Net":
            artnet_dict = {'Art-Net: ' + str(k): set(map(lambda x: 'sACN: ' + str(x), v))
                           for k, v in input_dict.items()}
            sacn_dict = {'sACN: ' + str(k): set(map(lambda x: 'Art-Net: ' + str(x), v))
                         for k, v in load_settings("sacndict", "sACN").items()}
        elif universe_type == "All":
            artnet_dict = {'Art-Net: ' + str(k): set(map(lambda x: 'sACN: ' + str(x), v))
                           for k, v in load_settings("artnetdict", "Art-Net").items()}
            sacn_dict = {'sACN: ' + str(k): set(map(lambda x: 'Art-Net: ' + str(x), v))
                             for k, v in load_settings("sacndict", "sACN").items()}

        # Create a dictionary containing both dicts
        loopback_dict = sacn_dict
        loopback_dict.update(artnet_dict)

        # Search the loopbacks
        loopbacks = nx.DiGraph(loopback_dict)
        loopbacks = list(nx.simple_cycles(loopbacks))
        if loopbacks:  # If there is a loopback, print an error
            message = str(loopbacks).replace("', '", " -> ")
            return True, f"Loop found: {message}. This would result in an infinite amount of packages."
        else:
            return False, None
    else:
        return False, None


@app.route("/")
@app.route("/home", methods=["POST", "GET"])
def home():
    """Renders the main page"""
    """INPUT: None"""
    """OUTPUT: Rendered Browser Template"""
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        # If the input_dict is out of order, it will be ordered.
        return render_template("dashboard.html", sacn_to_artnet=load_settings("sacn_to_artnet", "sACN"),
                               artnet_to_sacn=load_settings("artnet_to_sacn", "Art-Net"),
                               sacndict=OrderedDict(sorted(load_settings("sacndict", "sACN").items())),
                               artnetdict=OrderedDict(sorted(load_settings("artnetdict", "Art-Net").items())))


@app.route("/login", methods=["POST", "GET"])  # Login page
def login():
    form = LoginForm()
    if form.validate_on_submit:
        if form.username.data == load_settings("username", "Server") and form.password.data == \
                load_settings("password", "Server"):
            session['logged_in'] = True
            flash(f"Login for {form.username.data} was successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login failed.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")  # End session
def logout():
    session['logged_in'] = False
    flash("Logout successful!", "success")
    form = LoginForm()
    return render_template("login.html", form=form)


def validate_entry(artnet_universe, sacn_universe):
    try:
        artnet_universe = int(artnet_universe)
    except ValueError:  # Error if not a valid number
        return f"'{artnet_universe}' is not a valid number!", "danger"
    try:
        sacn_universe = int(sacn_universe)
    except ValueError:  # Error is sACN input is invalid
        return f"'{sacn_universe}' is not a valid universe number!", "danger"
    try:
        if not 0 <= artnet_universe <= 32768:
            raise ValueError(f"{artnet_universe}")
        if not 1 <= sacn_universe <= 63999:
            raise ValueError(f"{sacn_universe}")
    except ValueError as Error:
        return f"Universe {Error} out of range! Art-Net range: 0 to 32768, sACN range: 1 to 63999", "danger"
    else:
        pass


def add_sacn_entry(sacn_universe, artnet_universe, sacn_universe_old, artnet_universe_old):
    sacndict = load_settings("sacndict", "sACN")
    sacn_universe = int(sacn_universe)
    artnet_universe = int(artnet_universe)
    sacn_universe_old = int(sacn_universe_old)
    artnet_universe_old = int(artnet_universe_old)
    loopback_testdict = deepcopy(sacndict)
    if sacn_universe not in sacndict:

        # Test loopback
        loopback_testdict[sacn_universe] = [artnet_universe]
        loopback_testdict[sacn_universe_old].remove(artnet_universe_old)
        loopback, message = check_loopback(loopback_testdict, "sACN")
        if loopback is True:
            return message, "danger"

        # Add new sACN key if no loopback was found
        sacndict[sacn_universe] = [artnet_universe]
        sacndict[sacn_universe_old].remove(artnet_universe_old)
        save_settings("sACN", "sacndict", sacndict)
        return "Saved successfully!", "success"

    # Test if mapping already exists
    if artnet_universe in sacndict[sacn_universe]:  # If mapping already exists, show a warning
        return "This mapping already exists!", "danger"
    else:  # If mapping does not exist, add a new entry and remove the old one

        # Test loopback
        loopback_testdict[sacn_universe].append(artnet_universe)
        loopback_testdict[sacn_universe_old].remove(artnet_universe_old)
        loopback, message = check_loopback(loopback_testdict, "sACN")
        if loopback is True:
            return message, "danger"

        # Add new Art-Net key if no loopback was found
        sacndict[sacn_universe].append(artnet_universe)
        sacndict[sacn_universe_old].remove(artnet_universe_old)
        save_settings("sACN", "sacndict", sacndict)
        # Check if universe would result in a loopback error
        return "Saved successfully!", "success"


def add_artnet_entry(sacn_universe, artnet_universe, sacn_universe_old, artnet_universe_old):
    artnetdict = load_settings("artnetdict", "Art-Net")
    sacn_universe = int(sacn_universe)
    artnet_universe = int(artnet_universe)
    sacn_universe_old = int(sacn_universe_old)
    artnet_universe_old = int(artnet_universe_old)
    loopback_testdict = deepcopy(artnetdict)
    if artnet_universe not in artnetdict:

        # Test loopback
        loopback_testdict[artnet_universe] = [sacn_universe]
        loopback_testdict[artnet_universe_old].remove(sacn_universe_old)
        loopback, message = check_loopback(loopback_testdict, "Art-Net")
        if loopback is True:
            return message, "danger"

        # Add new Art-Net key if no loopback was found
        else:
            artnetdict[artnet_universe] = [sacn_universe]
            artnetdict[artnet_universe_old].remove(sacn_universe_old)
            save_settings("Art-Net", "artnetdict", artnetdict)
            return "Saved successfully!", "success"

    # Test if mapping already exists
    if sacn_universe in artnetdict[artnet_universe]:  # If mapping already exists, show a warning
        return "This mapping already exists!", "danger"
    else:  # If mapping does not exist, add a new entry and remove the old one

        # Test loopback
        loopback_testdict[artnet_universe].append(sacn_universe)
        loopback_testdict[artnet_universe_old].remove(sacn_universe_old)
        loopback, message = check_loopback(loopback_testdict, "Art-Net")
        if loopback is True:
            return message, "danger"

        # Add new sacn key if no loopback was found
        artnetdict[artnet_universe].append(sacn_universe)
        artnetdict[artnet_universe_old].remove(sacn_universe_old)
        save_settings("Art-Net", "artnetdict", artnetdict)
        # Check if universe would result in a loopback error
        return "Saved successfully!", "success"


def delete_entry(sacn_universe_old, artnet_universe_old, universe_type="sACN"):
    sacn_universe_old = int(sacn_universe_old)
    artnet_universe_old = int(artnet_universe_old)
    if universe_type == "sACN":
        sacndict = load_settings("sacndict", "sACN")
        try:
            sacndict[sacn_universe_old].remove(artnet_universe_old)
        except IndexError as ErrorMessage:
            return ErrorMessage, "danger"
        save_settings("sACN", "sacndict", sacndict)
        return "Universe successfully deleted!", "success"
    elif universe_type == "Art-Net":
        artnetdict = load_settings("artnetdict", "Art-Net")
        try:
            artnetdict[artnet_universe_old].remove(sacn_universe_old)
        except IndexError as ErrorMessage:
            return ErrorMessage, "danger"
        save_settings("Art-Net", "artnetdict", artnetdict)
        return "Universe successfully deleted!", "success"


@app.route("/change_sacn_entry", methods=["POST"])
# Depending on which button was pressed, a new Universe entry is added, removed or the entry will be reset.
def change_sacn_entry():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        # Receive the values entered by the user
        artnet_universe = request.form["artnet"]
        sacn_universe = request.form["sacn"]
        artnet_universe_old = request.form["artnet_old_value"]
        sacn_universe_old = request.form["sacn_old_value"]

        # Test if the entered values are valid
        message = validate_entry(artnet_universe, sacn_universe)
        if message:
            flash(message[0], message[1])
            return redirect(url_for("home"))

        # If the "add" button was pressed, change the universe.
        if "add" in request.form:
            message = add_sacn_entry(sacn_universe, artnet_universe, sacn_universe_old, artnet_universe_old)
            if message:
                flash(message[0], message[1])
                return redirect(url_for("home"))

        # If the "delete" button was pressed, delete the universe.
        elif "delete" in request.form:
            message = delete_entry(sacn_universe_old, artnet_universe_old, universe_type="sACN")
            if message:
                flash(message[0], message[1])
                return redirect(url_for("home"))
        # If the "reset" button was pressed, reload.
        elif "reset" in request.form:
            return redirect(url_for("home"))


@app.route("/change_artnet_entry", methods=["POST"])
# Depending on which button was pressed, a new Universe entry is added, removed or the entry will be resetted.
def change_artnet_entry():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:

        # Receive the values entered by the user
        artnet_universe = request.form["artnet"]
        sacn_universe = request.form["sacn"]
        artnet_universe_old = request.form["artnet_old_value"]
        sacn_universe_old = request.form["sacn_old_value"]

        # Test if the entered values are valid
        message = validate_entry(artnet_universe, sacn_universe)
        if message:
            flash(message[0], message[1])
            return redirect(url_for("home"))

        # If the "add" button was pressed, change the universe.
        if "add" in request.form:
            message = add_artnet_entry(sacn_universe, artnet_universe, sacn_universe_old, artnet_universe_old)
            if message:
                flash(message[0], message[1])
                return redirect(url_for("home"))

        # If the "delete" button was pressed, delete the universe.
        elif "delete" in request.form:
            message = delete_entry(sacn_universe_old, artnet_universe_old, universe_type="Art-Net")
            if message:
                flash(message[0], message[1])
                return redirect(url_for("home"))

        # If the "reset" button was pressed, reload.
        elif "reset" in request.form:
            return redirect(url_for("home"))


@app.route("/add_sacn_universe")
def add_sacn_universe():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        sacndict = load_settings("sacndict", "sACN")
        new_entry = sorted(sacndict.keys())[0]
        new_entry_key = new_entry
        while new_entry_key in sacndict[new_entry]:
            new_entry_key = new_entry_key + 1
        sacndict[new_entry].append(new_entry_key)
        save_settings("sACN", "sacndict", sacndict)
        flash(f"Universe {new_entry} to {new_entry} added!", "success")
        return redirect(url_for("home"))


@app.route("/add_artnet_universe")
def add_artnet_universe():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        artnetdict = load_settings("artnetdict", "Art-Net")
        new_entry = len(artnetdict) + 1
        artnetdict[new_entry] = [new_entry]
        save_settings("Art-Net", "artnetdict", artnetdict)
        flash(f"Universe {new_entry} to {new_entry} added!", "success")
        return redirect(url_for("home"))


@app.route("/activate_sacn_to_artnet")
def activate_sacn_to_artnet():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        loopback, message = check_loopback(0, "All")
        if loopback is True and load_settings("artnet_to_sacn", "Art-Net") is True:
            flash(message, "danger")
            return redirect(url_for("home"))
        else:
            sleep(0.5)  # Sleep until the slider animation on the frontend is finished
            save_settings("sACN", "sacn_to_artnet", True)
            return redirect(url_for("home"))


@app.route("/deactivate_sacn_to_artnet")
def deactivate_sacn_to_artnet():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        sleep(0.5)  # Sleep until the slider animation on the frontend is finished
        save_settings("sACN", "sacn_to_artnet", False)
        return redirect(url_for("home"))


@app.route("/activate_artnet_to_sacn")
def activate_artnet_to_sacn():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        loopback, message = check_loopback(0, "All")
        if loopback is True and load_settings("sacn_to_artnet", "sACN") is True:
            flash(message, "danger")
            return redirect(url_for("home"))
        else:
            sleep(0.5)  # Sleep until the slider animation on the frontend is finished
            save_settings("Art-Net", "artnet_to_sacn", True)
            return redirect(url_for("home"))


@app.route("/deactivate_artnet_to_sacn")
def deactivate_artnet_to_sacn():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        sleep(0.5)  # Sleep until the slider animation on the frontend is finished
        save_settings("Art-Net", "artnet_to_sacn", False)
        return redirect(url_for("home"))


@app.route("/settings")
def settings():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        form = ChangePasswordForm()
        return render_template("/settings.html", form=form, sacn_port=load_settings("sacn_port", "sACN"),
                               artnet_port=load_settings("artnet_port", "Art-Net"),
                               server_port=load_settings("server_port", "Server"),
                               server_ip=load_settings("ip", "Server"))


@app.route("/change_password", methods=["POST"])
def change_password():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        if "change" in request.form:

            try:
                if not request.form["username"]:
                    raise ValueError
                if not request.form["password"]:
                    raise ValueError
            except ValueError:
                flash("Username and Password can not be empty!", "danger")
                return redirect(url_for("settings"))

            try:
                username_input = str(request.form["username"])
                password_input = str(request.form["password"])
                if "%" in username_input:
                    if "%" in password_input:
                        raise ValueError
            except ValueError:
                flash("'%' not allowed. Please try again", "danger")
                return redirect(url_for("settings"))
            try:
                save_settings("Main", "username", username_input)
                save_settings("Main", "password", password_input)
            except ValueError:
                flash("Unknown symbol. Please try again", "danger")
                return redirect(url_for("settings"))
        flash("Password changed successfully!", "success")
        return redirect(url_for("settings"))


@app.route("/restore_factory_settings")
def restore_factory_settings():
    if not session.get('logged_in'):  # Show login screen if not logged in.
        form = LoginForm()
        return render_template("login.html", title="Login", form=form)
    else:
        delete_category("Art-Net")
        delete_category("sACN")
        delete_category("Main")
        flash("Factory settings restored!", "danger")
        return redirect(url_for("settings"))


def main():
    app.config["SECRET_KEY"] = token_hex(16)  # Create a random secret key
    app.run(debug=True, use_reloader=False, host=load_settings("ip", "Server"),
            port=load_settings("server_port", "Server"))


if __name__ == "__main__":
    main()
