from process import analyze # business logic
from app import App # App window
from interface import interface # UI

options = {
    "width": 400,
    "height": 360,
    "icon": "assets/accenture_logo.png",
    "title": "BSC Intake Staffing Optimization"
}

functions = {
    "analyze": analyze
}

app = App(options, functions, interface)
app.start()