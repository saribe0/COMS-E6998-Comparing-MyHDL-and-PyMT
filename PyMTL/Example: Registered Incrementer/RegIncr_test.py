#=========================================================================
# RegIncr_test
#=========================================================================

from pymtl   import *
from RegIncr import RegIncr

# In py.test, unit tests are simply functions that begin with a "test_"
# prefix. PyMTL is setup to simplify dumping VCD. Simply specify
# "dump_vcd" as an argument to your unit test, and then you can dump VCD
# with the --dump-vcd option to py.test.

def test_basic( dump_vcd ):

  # Get list of input values from command line
  
  input_values = [ int(x,0) for x in argv[1:] ]
  
  # Add three zero values to end of list of input values
  
  input_values.extend( [0]*3 )

  # Elaborate the model

  model = RegIncr()
  model.vcd_file = dump_vcd
  model.elaborate()

  # Create and reset simulator

  sim = SimulationTool( model )
  sim.reset()
  print ""

  # Helper function

  def t( in_, out ):

    # Write input value to input port

    model.in_.value = in_

    # Ensure that all combinational concurrent blocks are called

    sim.eval_combinational()

    # Display a line trace

    sim.print_line_trace()

    # If reference output is not '?', verify value read from output port

    if ( out != '?' ):
      assert model.out == out

    # Tick simulator one cycle

    sim.cycle()

  # Apply input values and display output values

  for input_value in input_values:
    out = 0
    t(input_value, out)

    print " cycle = {}: in = {}, out = {}" \
      .format( sim.ncycles, model.in_, model.out )





