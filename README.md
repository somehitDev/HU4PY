<div align="center">
<img src="https://github.com/oyajiDev/hufpy/blob/master/resources/splash_transparent.png?raw=true" width="300" />
</div>
<hr>

<div align="center">
    <a href="https://github.com/oyajiDev/hufpy/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/oyajiDev/hufpy.svg" alt="MIT License" />
    </a>
    <a href="https://pypi.org/project/hufpy/">
        <img src="https://img.shields.io/pypi/v/hufpy.svg" alt="pypi" />
    </a>
</div>

<br/><br/>

## 🌐 install
### - using pip
```zsh
python -m pip install hufpy
```

### - using git(dev)
```zsh
python -m pip install git+https://github.com/oyajiDev/hufpy.git
```

<br/><br/>

## 🛠 usage
### - basic
```python
from hufpy import Application
from hufpy.widgets.layouts import Frame

Application.init()
Application.Run(Frame)
```

### - view class
- view class can be defined by inheriting from <a href="https://github.com/oyajiDev/hufpy/blob/master/hufpy/widgets/layouts.py">"Layout" classes</a>
```python
from hufpy.widgets.layouts import Frame
from hufpy.widgets import Label

class MyLayout(Frame):
    def __init__(self):
        super().__init__()

        self.label1 = Label(self)
        self.label1.text = "Hello World!"
        self.append_child(self.label1)
```

### - events
- events can be connect
```python
from hufpy.widgets import Button

# codes here...
    btn1 = Button(self)
    btn1.text = "click me!"
    btn1.on_clicked = self.on_btn1_clicked

# codes here...
    def on_btn_clicked(self):
        print("you clicked me!")
```

### more example is in <a href="https://github.com/oyajiDev/hufpy/tree/master/test">"test"</a> directory
