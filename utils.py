# utils.py

def circle_rect_collision(cx, cy, radius, rect):
    rx, ry, rw, rh = rect
    nearest_x = max(rx, min(cx, rx + rw))
    nearest_y = max(ry, min(cy, ry + rh))
    dx = cx - nearest_x
    dy = cy - nearest_y
    return (dx*dx + dy*dy) < radius*radius
