from delay_gates import *
from delay_circuit import *


def summarize_outputs(outputs):
    print("------")
    for (gate,port), value, settle, segment, abs_t, rel in outputs:
        print("%s port:%s = %s" % (gate,port,value))
        print("   settling time =\t%e" % (settle))
        print("   relative delay =\t%e" % (rel))
        print("   absolute delay =\t%e" % (abs_t))
        print("   segment time =\t%e" % (segment) )
        print("")


def test_input():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    inx = circ.add_gate(Input("Y"))
    inx = circ.add_gate(Input("Z"))
    timing, traces = circ.simulate({"X":4, "Y":7, "Z":2})
    circ.render("test_input.png",timing,traces)
    circ.render_circuit("test_input_circ")
    summarize_outputs(circ.get_outputs(timing,traces))


def test_last_arrival_gate():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    iny = circ.add_gate(Input("Y"))
    la = circ.add_gate(LastArrival())
    circ.add_wire(inx,la,"A")
    circ.add_wire(iny,la,"B")

    timing,traces = circ.simulate({"X":4,"Y":7})
    circ.render("test_la.png",timing,traces)
    circ.render_circuit("test_la_circ")
    summarize_outputs(circ.get_outputs(timing,traces))


def test_first_arrival_gate():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    iny = circ.add_gate(Input("Y"))
    fa = circ.add_gate(FirstArrival())
    circ.add_wire(inx,fa,"A")
    circ.add_wire(iny,fa,"B")

    timing,traces = circ.simulate({"X":4,"Y":7})
    circ.render("test_fa.png",timing,traces)
    circ.render_circuit("test_fa_circ")
    summarize_outputs(circ.get_outputs(timing,traces))


def test_delay_gate():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    delay = circ.add_gate(DelayGate(2*circ.segment_time))
    circ.add_wire(inx,delay,"A")

    circ.render_circuit("test_del_circ")
    timing,traces = circ.simulate({"X":4})
    circ.render("test_del1.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))

    timing,traces = circ.simulate({"X":6})
    circ.render("test_del2.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))


def test_inh_gate():
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    iny = circ.add_gate(Input("Y"))
    inh = circ.add_gate(Inhibition())
    circ.add_wire(inx,inh,"A")
    circ.add_wire(iny,inh,"B")

    circ.render_circuit("test_inh_circ")
    timing,traces = circ.simulate({"X":4,"Y":7})
    circ.render("test_inh1.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))

    timing,traces = circ.simulate({"X":7,"Y":4})
    circ.render("test_inh2.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))


def test_less_than_5():
    input_x = 3
    input_y = 7
    circ = DelayBasedCircuit()
    inx = circ.add_gate(Input("X"))
    iny = circ.add_gate(Input("Y"))
    inc = circ.add_gate(Input("C"))
    ind = circ.add_gate(Input("D"))
    inh1 = circ.add_gate(Inhibition())
    inh2 = circ.add_gate(Inhibition())
    la = circ.add_gate(LastArrival())
    circ.add_wire(inx, inh1, "B")
    circ.add_wire(inc, inh1, "A")
    circ.add_wire(iny, inh2, "B")
    circ.add_wire(ind, inh2, "A")
    circ.add_wire(inh1, la, "A")
    circ.add_wire(inh2, la, "B")
    
    circ.render_circuit("test_less_than_5_circ")
    timing,traces = circ.simulate({"X":input_x,"Y":input_y, "C":5, "D":5})
    circ.render("test_less_than_5.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))


def test_more_than_5():
    input_x = 2
    input_y = 3
    circ = DelayBasedCircuit()
    inx1 = circ.add_gate(Input("X1"))
    iny1 = circ.add_gate(Input("Y1"))
    inx2 = circ.add_gate(Input("X2"))
    iny2 = circ.add_gate(Input("Y2"))
    inc = circ.add_gate(Input("C"))
    delay1 = circ.add_gate(DelayGate(0*circ.segment_time))
    delay2 = circ.add_gate(DelayGate(0*circ.segment_time))
    delay3 = circ.add_gate(DelayGate(0*circ.segment_time))
    circ.add_wire(inc, delay1, "A")
    circ.add_wire(inx2, delay2, "A")
    circ.add_wire(iny2, delay3, "A")
    la1 = circ.add_gate(LastArrival())
    la3 = circ.add_gate(LastArrival())
    circ.add_wire(inx1, la1, "A")
    circ.add_wire(iny1, la1, "B")
    circ.add_wire(delay2, la3, "A")
    circ.add_wire(delay3, la3, "B")
    inh = circ.add_gate(Inhibition())
    circ.add_wire(la1, inh, "A")
    circ.add_wire(delay1, inh, "B")
    la2 = circ.add_gate(LastArrival())
    circ.add_wire(inh, la2, "A")
    circ.add_wire(la3, la2, "B")
    
    circ.render_circuit("test_more_than_5_circ")
    timing,traces = circ.simulate({"X1":input_x,"Y1":input_y, "X2":input_x, "Y2":input_y, "C":5})
    circ.render("test_more_than_5.png",timing,traces)
    summarize_outputs(circ.get_outputs(timing,traces))


# test_input()
# test_first_arrival_gate()
# test_last_arrival_gate()
# test_inh_gate()
# test_delay_gate()
# test_less_than_5()
test_more_than_5()