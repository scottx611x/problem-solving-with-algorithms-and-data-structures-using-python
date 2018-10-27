from unittest import TestCase, mock
from section1.logic_gates import (LogicGate, NotGate, OrGate, AndGate, NorGate,
                                  NandGate, XorGate, HalfAdder, FullAdder,
                                  FullAdder8Bit)


class LogicGateTests(TestCase):
    def setUp(self):
        self.logic_gate = LogicGate()

    def test_get_label(self):
        self.assertEqual(self.logic_gate.get_label(), None)

    def test_get_output(self):
        with mock.patch.object(LogicGate, "perform_gate_logic",
                               return_value=1):
            output = self.logic_gate.get_output()
        self.assertEqual(output, 1)

    def test_perform_gate_logic(self):
        with self.assertRaises(NotImplementedError):
            self.logic_gate.perform_gate_logic()


class BinaryGateTests(TestCase):
    def test_and_gate_1(self):
        self.assertEqual(AndGate(1, 1).output, 1)

    def test_and_gate_0(self):
        outputs = [AndGate(1, 0).output, AndGate(0, 1).output,
                   AndGate(0, 0).output]
        for output in outputs:
            self.assertEqual(output, 0)

    def test_or_gate_1(self):
        outputs = [OrGate(1, 0).output, OrGate(0, 1).output,
                   OrGate(1, 1).output]
        for output in outputs:
            self.assertEqual(output, 1)

    def test_or_gate_0(self):
        self.assertEqual(OrGate(0, 0).output, 0)

    def test_nor_gate_1(self):
        self.assertEqual(NorGate(0, 0).output, 1)

    def test_nor_gate_0(self):
        outputs = [NorGate(1, 0).output, NorGate(0, 1).output,
                   NorGate(1, 1).output]
        for output in outputs:
            self.assertEqual(output, 0)

    def test_nand_gate_1(self):
        outputs = [NandGate(1, 0).output, NandGate(0, 1).output,
                   NandGate(0, 0).output]
        for output in outputs:
            self.assertEqual(output, 1)

    def test_nand_gate_0(self):
        self.assertEqual(NandGate(1, 1).output, 0)

    def test_xor_gate_1(self):
        outputs = [XorGate(1, 0).output, XorGate(0, 1).output]
        for output in outputs:
            self.assertEqual(output, 1)

    def test_xor_gate_0(self):
        outputs = [XorGate(0, 0).output, XorGate(1, 1).output]
        for output in outputs:
            self.assertEqual(output, 0)


class UnaryGateTests(TestCase):
    def test_not_gate_1(self):
        self.assertEqual(NotGate(1).output, 0)

    def test_not_gate_0(self):
        self.assertEqual(NotGate(0).output, 1)


class HalfAdderTests(TestCase):
    def test_0_0(self):
        self.assertEqual(
            HalfAdder(0, 0).output, (0, 0)
        )

    def test_0_1(self):
        self.assertEqual(
            HalfAdder(0, 1).output, (1, 0)
        )

    def test_1_0(self):
        self.assertEqual(
            HalfAdder(1, 0).output, (1, 0)
        )

    def test_1_1(self):
        self.assertEqual(
            HalfAdder(1, 1).output, (0, 1)
        )


class FullAdderTests(TestCase):
    def test_0_0_0(self):
        self.assertEqual(FullAdder(0, 0, 0).output, (0, 0))

    def test_0_0_1(self):
        self.assertEqual(FullAdder(0, 0, 1).output, (1, 0))

    def test_0_1_0(self):
        self.assertEqual(FullAdder(0, 1, 0).output, (1, 0))

    def test_0_1_1(self):
        self.assertEqual(FullAdder(0, 1, 1).output, (0, 1))

    def test_1_0_0(self):
        self.assertEqual(FullAdder(1, 0, 0).output, (1, 0))

    def test_1_0_1(self):
        self.assertEqual(FullAdder(1, 0, 1).output, (0, 1))

    def test_1_1_0(self):
        self.assertEqual(FullAdder(1, 1, 0).output, (0, 1))

    def test_1_1_1(self):
        self.assertEqual(FullAdder(1, 1, 1).output, (1, 1))


class FullAdder8BitTests(TestCase):
    def test_full_adder_8_bit(self):
        self.assertEqual(FullAdder8Bit(23, 46).output, 69)