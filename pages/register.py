import os
import panel as pn
from .home import home_page

def register_page():

    pn.extension()

    db_input = pn.widgets.TextInput(name='Database', placeholder='Enter database name')
    host_input = pn.widgets.TextInput(name='Host', placeholder='Enter host name')
    port_input = pn.widgets.TextInput(name='Port', placeholder='Enter port number')
    user_input = pn.widgets.TextInput(name='Username', placeholder='Enter username')

    password_input = pn.widgets.PasswordInput(name='Password', placeholder='Enter password')

    login_button = pn.widgets.Button(name='Login', button_type='primary')

    def load_config():
        # Use os.path.join to create the full path for the config file
        config_file = os.path.join(os.getcwd(), "db_config.txt")
        
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                lines = f.readlines()

                db_value = lines[0].split(": ")[1].strip()
                host_value = lines[1].split(": ")[1].strip()
                port_value = lines[2].split(": ")[1].strip()
                user_value = lines[3].split(": ")[1].strip()
                password_value = lines[4].split(": ")[1].strip()

                db_input.value = db_value
                host_input.value = host_value
                port_input.value = port_value
                user_input.value = user_value
                password_input.value = password_value

    load_config()

    elements = [
        db_input,
        host_input,
        port_input,
        user_input,
        password_input,
        login_button
    ]

    layout = pn.Column(*elements)

    def save_to_file(event):
        config_file = os.path.join(os.getcwd(), "db_config.txt")
        
        db_value = db_input.value
        host_value = host_input.value
        port_value = port_input.value
        user_value = user_input.value
        password_value = password_input.value

        with open(config_file, "w") as f:
            f.write(f"Database: {db_value}\n")
            f.write(f"Host: {host_value}\n")
            f.write(f"Port: {port_value}\n")
            f.write(f"Username: {user_value}\n")
            f.write(f"Password: {password_value}\n")

        home_page(layout,db_value, host_value, port_value, user_value, password_value)

    login_button.on_click(save_to_file)
    
    pn.serve(layout, port = 3000)