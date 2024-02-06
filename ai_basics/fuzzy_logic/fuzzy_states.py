import enum
import math
from typing import Dict, Callable, Tuple


class DistanceStates(enum.Enum):
    # NEGATIVE_BIG = 'NEGATIVE_BIG'
    # NEGATIVE_MEDIUM = 'NEGATIVE_MEDIUM'
    # ZERO = 'ZERO'
    # POSITIVE_MEDIUM = 'POSITIVE_MEDIUM'
    # POSITIVE_BIG = 'POSITIVE_BIG'

    NEGATIVE = 'NEGATIVE'
    ZERO = 'ZERO'
    POSITIVE = 'POSITIVE'

class AccelerationStates(enum.Enum):
    # NEGATIVE_BIG = 'NEGATIVE_BIG'
    # NEGATIVE_MEDIUM = 'NEGATIVE_MEDIUM'
    # ZERO = 'ZERO'
    # POSITIVE_MEDIUM = 'POSITIVE_MEDIUM'
    # POSITIVE_BIG = 'POSITIVE_BIG'

    NEGATIVE = 'NEGATIVE'
    ZERO = 'ZERO'
    POSITIVE = 'POSITIVE'

class DiffAccelerationStates(enum.Enum):
    # NEGATIVE_BIG = 'NEGATIVE_BIG'
    # NEGATIVE_MEDIUM = 'NEGATIVE_MEDIUM'
    # ZERO = 'ZERO'
    # POSITIVE_MEDIUM = 'POSITIVE_MEDIUM'
    # POSITIVE_BIG = 'POSITIVE_BIG'

    NEGATIVE = 'NEGATIVE'
    ZERO = 'ZERO'
    POSITIVE = 'POSITIVE'


def center_state(state: DiffAccelerationStates) -> float:
    center = 0.

    # match state:
        # case DiffAccelerationStates.NEGATIVE_BIG:
        #     center = DiffANEGATIVE_BIG.get_center()
        # case DiffAccelerationStates.NEGATIVE_MEDIUM:
        #     center = DiffANEGATIVE_MEDIUM.get_center()
        # case DiffAccelerationStates.ZERO:
        #     center = DiffAZERO.get_center()
        # case DiffAccelerationStates.POSITIVE_MEDIUM:
        #     center = DiffAPOSITIVE_MEDIUM.get_center()
        # case DiffAccelerationStates.POSITIVE_BIG:
        #     center = DiffAPOSITIVE_BIG.get_center()


    match state:
        case DiffAccelerationStates.NEGATIVE:
            center = GNEGATIVE.get_center()
        case DiffAccelerationStates.ZERO:
            center = GZERO.get_center()
        case DiffAccelerationStates.POSITIVE:
            center = GPOSITIVE.get_center()

    return center


def gaussian(x: float, c: float, sigma: float) -> float:
    return math.exp(-((x - c)/sigma) ** 2)


def trapeze_left(x: float, a: float, b: float) -> float:
    if x < a:
        return 0
    elif x >= b:
        return 1
    else:
        return 1 - (b - x) / (b - a)

def trapeze_right(x: float, a: float, b: float) -> float:
    if x <= a:
        return 1
    elif x > b:
        return 0
    else:
        return 1 - (x - a) / (b - a)

def triangle(x: float, a: float, b: float, c: float) -> float:
    if a <= x <= b:
        return 1 - (b - x) / (b - a)
    elif b <= x <= c:
        return 1 - (x - b) / (c - b)
    else:
        return 0

class NegativeBig:
    def __init__(self):
        self._c = -15
        self._a = -10
        self._b = -5

    def fuzzifying(self, x: float) -> float:
        return trapeze_right(x, self._a, self._b)

    def get_center(self) -> float:
        return 1 / 2 * (self._b + self._c) + self._b


class PositiveBig:
    def __init__(self):
        self._a = 5
        self._b = 10
        self._c = 15

    def fuzzifying(self, x: float) -> float:
        return trapeze_left(x, self._a, self._b)

    def get_center(self) -> float:
        return 1/2 * (self._c - self._a) + self._a


class NegativeMedium:
    def __init__(self):
        self._a = -10
        self._b = -5
        self._c = 0

    def fuzzifying(self, x: float) -> float:
        return triangle(x, self._a, self._b, self._c)

    def get_center(self) -> float:
        return self._b


class PositiveMedium:
    def __init__(self):
        self._a = 0
        self._b = 5
        self._c = 10

    def fuzzifying(self, x: float) -> float:
        return triangle(x, self._a, self._b, self._c)

    def get_center(self) -> float:
        return self._b


class Zero:
    def __init__(self):
        self._a = -5
        self._b = 0
        self._c = 5

    def fuzzifying(self, x: float) -> float:
        return triangle(x, self._a, self._b, self._c)

    def get_center(self) -> float:
        return self._b

class DiffANegativeBig:
    def __init__(self):
        self._c = -10
        self._a = -5
        self._b = -3

    def get_center(self) -> float:
        return 1 / 2 * (self._b + self._c) + self._b


class DiffAPositiveBig:
    def __init__(self):
        self._a = 3
        self._b = 5
        self._c = 10

    def get_center(self) -> float:
        return 1/2 * (self._c - self._a) + self._a


class DiffANegativeMedium:
    def __init__(self):
        self._a = -5
        self._b = -3
        self._c = 0

    def get_center(self) -> float:
        return self._b


class DiffAPositiveMedium:
    def __init__(self):
        self._a = 0
        self._b = 3
        self._c = 5

    def get_center(self) -> float:
        return self._b


class DiffAZero:
    def __init__(self):
        self._a = -3
        self._b = 0
        self._c = 3

    def get_center(self) -> float:
        return self._b


class Negative:
    def __init__(self):
        self._c = -15
        self._a = -5
        self._b = 0

    def fuzzifying(self, x: float) -> float:
        return trapeze_right(x, self._a, self._b)

    def get_center(self) -> float:
        return 1 / 2 * (self._b + self._c) + self._b


class Positive:
    def __init__(self):
        self._a = 0
        self._b = 5
        self._c = 15

    def fuzzifying(self, x: float) -> float:
        return trapeze_left(x, self._a, self._b)

    def get_center(self) -> float:
        return 1/2 * (self._c - self._a) + self._a


class ZeroAcceleration:
    def __init__(self):
        self._a = -5
        self._b = 0
        self._c = 5

    def fuzzifying(self, x: float) -> float:
        return triangle(x, self._a, self._b, self._c)


NEGATIVE_BIG = NegativeBig()
NEGATIVE_MEDIUM = NegativeMedium()
ZERO = Zero()
POSITIVE_MEDIUM = PositiveMedium()
POSITIVE_BIG = PositiveBig()

DiffANEGATIVE_BIG = DiffANegativeBig()
DiffANEGATIVE_MEDIUM = DiffANegativeMedium()
DiffAZERO = DiffAZero()
DiffAPOSITIVE_MEDIUM = DiffAPositiveMedium()
DiffAPOSITIVE_BIG = DiffAPositiveBig()

NEGATIVE = Negative()
ZERO_ACCELERATION = ZeroAcceleration()
POSITIVE = Positive()


class GNegative:
    def __init__(self):
        self._c = -50
        self._sigma = 50

    def fuzzifying(self, x: float) -> float:
        return gaussian(x, self._c, self._sigma)

    def get_center(self) -> float:
        return self._c


class GPositive:
    def __init__(self):
        self._c = 50
        self._sigma = 50

    def fuzzifying(self, x: float) -> float:
        return gaussian(x, self._c, self._sigma)

    def get_center(self) -> float:
        return self._c


class GZero:
    def __init__(self):
        self._c = 0
        self._sigma = 50

    def fuzzifying(self, x: float) -> float:
        return gaussian(x, self._c, self._sigma)

    def get_center(self) -> float:
        return self._c


GNEGATIVE = GNegative()
GZERO = GZero()
GPOSITIVE = GPositive()


distance_states_to_fuzzifying: Dict[DistanceStates, Callable] = {
    # DistanceStates.NEGATIVE_BIG: NEGATIVE_BIG.fuzzifying,
    # DistanceStates.NEGATIVE_MEDIUM: NEGATIVE_MEDIUM.fuzzifying,
    # DistanceStates.ZERO: ZERO.fuzzifying,
    # DistanceStates.POSITIVE_MEDIUM: POSITIVE_MEDIUM.fuzzifying,
    # DistanceStates.POSITIVE_BIG: POSITIVE_BIG.fuzzifying,

    DistanceStates.NEGATIVE: GNEGATIVE.fuzzifying,
    DistanceStates.ZERO: GZERO.fuzzifying,
    DistanceStates.POSITIVE: GPOSITIVE.fuzzifying,
}


a_states_to_fuzzifying: Dict[AccelerationStates, Callable] = {
    # AccelerationStates.NEGATIVE_BIG: NEGATIVE_BIG.fuzzifying,
    # AccelerationStates.NEGATIVE_MEDIUM: NEGATIVE_MEDIUM.fuzzifying,
    # AccelerationStates.ZERO: ZERO.fuzzifying,
    # AccelerationStates.POSITIVE_MEDIUM: POSITIVE_MEDIUM.fuzzifying,
    # AccelerationStates.POSITIVE_BIG: POSITIVE_BIG.fuzzifying,

    # AccelerationStates.NEGATIVE: NEGATIVE.fuzzifying,
    # AccelerationStates.ZERO: ZERO.fuzzifying,
    # AccelerationStates.POSITIVE: POSITIVE.fuzzifying,

    AccelerationStates.NEGATIVE: GNEGATIVE.fuzzifying,
    AccelerationStates.ZERO: GZERO.fuzzifying,
    AccelerationStates.POSITIVE: GPOSITIVE.fuzzifying,
}

# new_diff_a_states: Dict[Tuple[DistanceStates, AccelerationStates], DiffAccelerationStates] = {
#     (DistanceStates.NEGATIVE_BIG, AccelerationStates.NEGATIVE_BIG): DiffAccelerationStates.ZERO,
#     (DistanceStates.NEGATIVE_BIG, AccelerationStates.NEGATIVE_MEDIUM): DiffAccelerationStates.NEGATIVE_MEDIUM,
#     (DistanceStates.NEGATIVE_BIG, AccelerationStates.ZERO): DiffAccelerationStates.NEGATIVE_BIG,
#     (DistanceStates.NEGATIVE_BIG, AccelerationStates.POSITIVE_MEDIUM): DiffAccelerationStates.NEGATIVE_BIG,
#     (DistanceStates.NEGATIVE_BIG, AccelerationStates.POSITIVE_BIG): DiffAccelerationStates.NEGATIVE_BIG,
#
#     (DistanceStates.NEGATIVE_MEDIUM, AccelerationStates.NEGATIVE_BIG): DiffAccelerationStates.POSITIVE_MEDIUM,
#     (DistanceStates.NEGATIVE_MEDIUM, AccelerationStates.NEGATIVE_MEDIUM): DiffAccelerationStates.ZERO,
#     (DistanceStates.NEGATIVE_MEDIUM, AccelerationStates.ZERO): DiffAccelerationStates.NEGATIVE_MEDIUM,
#     (DistanceStates.NEGATIVE_MEDIUM, AccelerationStates.POSITIVE_MEDIUM): DiffAccelerationStates.NEGATIVE_BIG,
#     (DistanceStates.NEGATIVE_MEDIUM, AccelerationStates.POSITIVE_BIG): DiffAccelerationStates.NEGATIVE_BIG,
#
#     (DistanceStates.ZERO, AccelerationStates.NEGATIVE_BIG): DiffAccelerationStates.POSITIVE_BIG,
#     (DistanceStates.ZERO, AccelerationStates.NEGATIVE_MEDIUM): DiffAccelerationStates.POSITIVE_MEDIUM,
#     (DistanceStates.ZERO, AccelerationStates.ZERO): DiffAccelerationStates.ZERO,
#     (DistanceStates.ZERO, AccelerationStates.POSITIVE_MEDIUM): DiffAccelerationStates.NEGATIVE_MEDIUM,
#     (DistanceStates.ZERO, AccelerationStates.POSITIVE_BIG): DiffAccelerationStates.NEGATIVE_BIG,
#
#     (DistanceStates.POSITIVE_MEDIUM, AccelerationStates.NEGATIVE_BIG): DiffAccelerationStates.POSITIVE_BIG,
#     (DistanceStates.POSITIVE_MEDIUM, AccelerationStates.NEGATIVE_MEDIUM): DiffAccelerationStates.POSITIVE_BIG,
#     (DistanceStates.POSITIVE_MEDIUM, AccelerationStates.ZERO): DiffAccelerationStates.POSITIVE_MEDIUM,
#     (DistanceStates.POSITIVE_MEDIUM, AccelerationStates.POSITIVE_MEDIUM): DiffAccelerationStates.ZERO,
#     (DistanceStates.POSITIVE_MEDIUM, AccelerationStates.POSITIVE_BIG): DiffAccelerationStates.NEGATIVE_MEDIUM,
#
#     (DistanceStates.POSITIVE_BIG, AccelerationStates.NEGATIVE_BIG): DiffAccelerationStates.POSITIVE_BIG,
#     (DistanceStates.POSITIVE_BIG, AccelerationStates.NEGATIVE_MEDIUM): DiffAccelerationStates.POSITIVE_BIG,
#     (DistanceStates.POSITIVE_BIG, AccelerationStates.ZERO): DiffAccelerationStates.POSITIVE_BIG,
#     (DistanceStates.POSITIVE_BIG, AccelerationStates.POSITIVE_MEDIUM): DiffAccelerationStates.POSITIVE_MEDIUM,
#     (DistanceStates.POSITIVE_BIG, AccelerationStates.POSITIVE_BIG): DiffAccelerationStates.ZERO,
# }

# diff_a_states: Dict[Tuple[DistanceStates, AccelerationStates], DiffAccelerationStates] = {
    # (DistanceStates.NEGATIVE_BIG, AccelerationStates.NEGATIVE): DiffAccelerationStates.NEGATIVE_BIG,
    # (DistanceStates.NEGATIVE_BIG, AccelerationStates.ZERO): DiffAccelerationStates.NEGATIVE_MEDIUM,
    # (DistanceStates.NEGATIVE_BIG, AccelerationStates.POSITIVE): DiffAccelerationStates.ZERO,
    #
    # (DistanceStates.NEGATIVE_MEDIUM, AccelerationStates.NEGATIVE): DiffAccelerationStates.NEGATIVE_MEDIUM,
    # (DistanceStates.NEGATIVE_MEDIUM, AccelerationStates.ZERO): DiffAccelerationStates.ZERO,
    # (DistanceStates.NEGATIVE_MEDIUM, AccelerationStates.POSITIVE): DiffAccelerationStates.ZERO,
    #
    # (DistanceStates.ZERO, AccelerationStates.NEGATIVE): DiffAccelerationStates.ZERO,
    # (DistanceStates.ZERO, AccelerationStates.ZERO): DiffAccelerationStates.ZERO,
    # (DistanceStates.ZERO, AccelerationStates.POSITIVE): DiffAccelerationStates.ZERO,
    #
    # (DistanceStates.POSITIVE_MEDIUM, AccelerationStates.NEGATIVE): DiffAccelerationStates.ZERO,
    # (DistanceStates.POSITIVE_MEDIUM, AccelerationStates.ZERO): DiffAccelerationStates.ZERO,
    # (DistanceStates.POSITIVE_MEDIUM, AccelerationStates.POSITIVE): DiffAccelerationStates.POSITIVE_MEDIUM,
    #
    # (DistanceStates.POSITIVE_BIG, AccelerationStates.NEGATIVE): DiffAccelerationStates.ZERO,
    # (DistanceStates.POSITIVE_BIG, AccelerationStates.ZERO): DiffAccelerationStates.POSITIVE_MEDIUM,
    # (DistanceStates.POSITIVE_BIG, AccelerationStates.POSITIVE): DiffAccelerationStates.POSITIVE_BIG,
# }

diff_a_states: Dict[Tuple[DistanceStates, AccelerationStates], DiffAccelerationStates] = {
    (DistanceStates.NEGATIVE, AccelerationStates.NEGATIVE): DiffAccelerationStates.NEGATIVE,
    (DistanceStates.NEGATIVE, AccelerationStates.ZERO): DiffAccelerationStates.ZERO,
    (DistanceStates.NEGATIVE, AccelerationStates.POSITIVE): DiffAccelerationStates.ZERO,

    (DistanceStates.ZERO, AccelerationStates.NEGATIVE): DiffAccelerationStates.ZERO,
    (DistanceStates.ZERO, AccelerationStates.ZERO): DiffAccelerationStates.ZERO,
    (DistanceStates.ZERO, AccelerationStates.POSITIVE): DiffAccelerationStates.ZERO,

    (DistanceStates.POSITIVE, AccelerationStates.NEGATIVE): DiffAccelerationStates.ZERO,
    (DistanceStates.POSITIVE, AccelerationStates.ZERO): DiffAccelerationStates.ZERO,
    (DistanceStates.POSITIVE, AccelerationStates.POSITIVE): DiffAccelerationStates.POSITIVE,
}