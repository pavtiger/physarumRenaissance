# Physarum Renaissance
Setup VisPy OpenGL library:
```
  pip install vispy
```
and one more visualising library:
```
  pip install pyqt5
```



Class Particle has a few functions for life control:
```
p_share()
```
  share food to closest friends
```
p_test(y, x, var)
```
  remove amount var of food from x y
```
p_move()
```
  move particle by class parameters
```
p_rotate(sensor readings)
```
rotate by angle, depending on sensor value
```
p_sense()
```
get all sensor readings
