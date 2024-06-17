def turn_cube(n, x, y, z, rotations):
    def turn_point(axis, k, s, x, y, z):
        if axis == 'X' and x == k:
            if s == 1:
                return x, z, n+1-y
            elif s == -1:
                return x, n+1-z, y
        elif axis == 'Y' and y == k:
            if s == 1:
                return z, y, n+1-x
            elif s == -1:
                return n+1-z, y, x
        elif axis == 'Z' and z == k:
            if s == 1:
                return y, n+1-x, z
            elif s == -1:
                return n+1-y, x, z
        return x, y, z

    for axis, k, s in rotations:
        x, y, z = turn_point(axis, k, s, x, y, z)
    return x, y, z


for l in range(1, 21):
    with open(rf"C:\Users\Admin\Downloads\Кубик Рубика1\input_s1_{l:02}.txt") as file:
        data = file.read().splitlines()
    file2 = open(rf"C:\Users\Admin\Downloads\Кубик Рубика1\output_s1_{l:02}.txt")
    n, m = map(int, data[0].split())
    x, y, z = map(int, data[1].split())

    rotations = []
    for i in range(2, 2 + m):
        parts = data[i].split()
        rotations.append((parts[0], int(parts[1]), int(parts[2])))

    x, y, z = turn_cube(n, x, y, z, rotations)
    right_ans = file2.read().splitlines()
    print(f"Test {l}: {[' '.join([str(x), str(y), str(z)])] == right_ans}")
    print(right_ans)
