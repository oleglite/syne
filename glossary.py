signal1 = (0.1, 0.2, 0.3)   # (activity, activity, ...)
signal2 = (0.0, 0.7, 0.2)
message = (signal1, signal2)


def impulses(signal):
    return tuple(range(signal))


sample = (None, 0, 1, 4, None)  # None - not active, number - impulse

pattern = Matrix([  # matrix like message, but with weights
    [0.1, 0.8],
    [0.4, 0.3],
    [0.0, 0.9],
])
