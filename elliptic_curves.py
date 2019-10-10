class CurvePoint:
    def __init__(self, x, y, curve):
        if not (isinstance(curve, EllipticCurve)):
            raise ValueError("Curve should be instances of EllipticCurve!")
        self.x = x
        self.y = y
        self.curve = curve

    def __add__(self, other):
        if other not in self.curve:
            raise LookupError("Not on the curve!")
        if self != other and self != CurvePoint(other.x, other.x + other.y,
                                                other.curve):
            lmbd = int(((other.y - self.y) / (other.x - self.x)) % self.curve.p)
            x = int((lmbd ** 2 - self.x - other.x) % self.curve.p)
            y = int((lmbd * (self.x - x) - self.y) % self.curve.p)
            return CurvePoint(x, y, self.curve)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise ValueError
        temp = self
        for i in range(other // 2):
            temp = temp.__duplicate()
        if other % 2:
            return temp + self
        return temp

    def __duplicate(self):
        if self != CurvePoint(self.x, self.x + self.y, self.curve):
            lmbd = int(((
                                3 * self.x ** 2 + self.curve.a) / 2 * self.y) % self.curve.p)
            x = int((lmbd ** 2 - self.x - self.x) % self.curve.p)
            y = int((lmbd * (self.x - x) - self.y) % self.curve.p)
            return CurvePoint(x, y, self.curve)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f"Point ({self.x}, {self.y})"


# y^2=x^3+ax+b Over Fp
class EllipticCurve:
    def __init__(self, a, b, p):
        if not (isinstance(a, int) and isinstance(b, int)):
            raise ValueError("Invalid constructor param!")
        if -16 * (4 * a ** 3 + 27 * b ** 2) == 0:
            raise ValueError("Invalid coefficients, D=0!")
        self.a = a
        self.b = b
        self.p = p

    def __contains__(self, item):
        if abs(((item.y ** 2) % self.p) - ((
                                                   item.x ** 3 + self.a * item.x + self.b) % self.p)) < 0.00000001:
            return True
        print(item.y ** 2)
        print(item.x ** 3 + self.a * item.x + self.b)
        return False


if __name__ == "__main__":
    p = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F"
    curve = EllipticCurve(0, 7, int(p, 16))  # Secp256k1
    px = "5506626302227734366957871889516853432625" \
         "0603453777594175500187360389116729240"
    py = "32670510020758816978083085130507043184471" \
         "273380659243275938904335757337482424"
    first_point = CurvePoint(int(px), int(py), curve)
    print(first_point)
    second_point = first_point * 2
    print(second_point)
    result = second_point + first_point
    print(f"Sum: {result}")
