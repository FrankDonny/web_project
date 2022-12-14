from flask import Flask, render_template, request

app = Flask(__name__)
app.url_map.strict_slashes = False
from app_pack import routes
