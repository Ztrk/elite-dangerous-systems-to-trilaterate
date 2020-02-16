to_origin = lambda x : x - (x + 5) % 10

x, y, z, r = input('x, y, z, radius: ').split(',')
r = float(r)
x = to_origin(float(x) - r)
y = to_origin(float(y) - r)
z = to_origin(float(z) - r)
print(x, y, z)
