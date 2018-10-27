# coding=utf-8


class LogicGate:
    def __init__(self):
        self.label = None
        self.output = None

    def __repr__(self):
        return self.__str__()

    def get_label(self):
        return self.label

    def get_output(self):
        self.output = self.perform_gate_logic()
        return self.output

    def perform_gate_logic(self):
        raise NotImplementedError


class BinaryGate(LogicGate):
    def __init__(self, input_a=None, input_b=None):
        super().__init__()
        self.input_a = input_a
        self.input_b = input_b

    def __str__(self):
        return f"{self.label}: {self.input_a}, {self.input_b}"


class UnaryGate(LogicGate):
    def __init__(self, input):
        super().__init__()
        self.input = input

    def __str__(self):
        return f"{self.label}: {self.input}"


class AndGate(BinaryGate):
    def __init__(self, input_a, input_b):
        self.label = "AND"
        super().__init__(input_a, input_b)
        self.get_output()

    def perform_gate_logic(self):
        return self.input_a & self.input_b


class OrGate(BinaryGate):
    def __init__(self, input_a, input_b):
        self.label = "OR"
        super().__init__(input_a, input_b)
        self.get_output()

    def perform_gate_logic(self):
        return self.input_a | self.input_b


class NotGate(UnaryGate):
    def __init__(self, input):
        self.label = "NOT"
        super().__init__(input)
        self.get_output()

    def perform_gate_logic(self):
        return int(not self.input)


class NorGate(OrGate):
    def __init__(self, input_a, input_b):
        self.label = "NOR"
        super().__init__(input_a, input_b)

    def perform_gate_logic(self):
        return NotGate(super().perform_gate_logic()).output


class NandGate(AndGate):
    def __init__(self, input_a, input_b):
        self.label = "NAND"
        super().__init__(input_a, input_b)

    def perform_gate_logic(self):
        return NotGate(super().perform_gate_logic()).output


class XorGate(OrGate):
    def __init__(self, input_a, input_b):
        self.label = "XOR"
        super().__init__(input_a, input_b)

    def perform_gate_logic(self):
        if self.input_a and self.input_b == 1:
            return 0
        else:
            return super().perform_gate_logic()


class HalfAdder:
    def __init__(self, input_a, input_b):
        self.inputa = input_a
        self.inputb = input_b
        self.output = self.perform_gate_logic()

    def perform_gate_logic(self):
        return (
            XorGate(self.inputa, self.inputb).output,
            AndGate(self.inputa, self.inputb).output
        )


class FullAdder:
    def __init__(self, input_a, input_b, carry_in):
        self.inputa = input_a
        self.inputb = input_b
        self.carry_in = carry_in
        self.output = self.perform_gate_logic()

    def perform_gate_logic(self):
        sum_a, carry_a = HalfAdder(self.inputa, self.inputb).output
        sum_out, carry_b = HalfAdder(self.carry_in, sum_a).output
        return sum_out, OrGate(carry_a, carry_b).output


class FullAdder8Bit:
    def __init__(self, inputa, inputb):
        self.inputa = self._to_8_bit(inputa)
        self.inputb = self._to_8_bit(inputb)
        self.output = self._to_int(self.perform_gate_logic())

    def _to_8_bit(self, input):
        return [int(c) for c in list('{0:08b}'.format(input))]

    def _to_int(self, input):
        return int(input, 2)

    def perform_gate_logic(self):
        output = ""
        carry = None
        self.inputa.reverse()
        self.inputb.reverse()
        for i, a in enumerate(self.inputa):
            if carry is None:
                s, carry = HalfAdder(a, self.inputb[i]).output
            else:
                s, carry = FullAdder(a, self.inputb[i], carry).output
            output = str(s) + output
        return output