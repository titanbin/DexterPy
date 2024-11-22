# Installation:
You need `pygame`, `pygame_textinput`, `pymupdf` and `numpy`.

They are all available through pip.

# How to run:
Run the script with your image/pdf file as an argument, i.e. :

```
dexter.py /absolute/path/to/your/image.png
```

# How to use:
- trace the x and y axes by click and dragging lines (horizontal lines will be automatically assigned to the x axis, vertical lines to the y axis). Make sure to start and end the lines at marked values.
- write down the corresponding values on the axis (`tab` to move to the next text area, `shift` + `tab` to move to the previous one).
- click anywhere to set data points. You can remove a data point by clicking anywhere near it.
- press `Enter` and the corresponding data points in axis-space will be printed to your terminal. 

# To do:
- make pymupdf an optional thing.
- make the UI better.
