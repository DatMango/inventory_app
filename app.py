from pages.register import register_page
import panel as pn
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.append(script_dir)

pn.extension()
register_page()