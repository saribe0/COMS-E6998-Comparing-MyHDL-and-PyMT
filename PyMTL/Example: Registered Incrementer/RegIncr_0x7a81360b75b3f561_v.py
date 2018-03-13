#=======================================================================
# VRegIncr_0x7a81360b75b3f561_v.py
#=======================================================================
# This wrapper makes a Verilator-generated C++ model appear as if it
# were a normal PyMTL model.

import os

from pymtl import *
from cffi  import FFI

#-----------------------------------------------------------------------
# RegIncr_0x7a81360b75b3f561
#-----------------------------------------------------------------------
class RegIncr_0x7a81360b75b3f561( Model ):
  id_ = 0

  def __init__( s ):

    # initialize FFI, define the exposed interface
    s.ffi = FFI()
    s.ffi.cdef('''
      typedef struct {

        // Exposed port interface
        unsigned char * reset;
      unsigned char * in_;
      unsigned char * clk;
      unsigned char * out;

        // Verilator model
        void * model;

        // VCD state
        int _vcd_en;

      } VRegIncr_0x7a81360b75b3f561_t;

      VRegIncr_0x7a81360b75b3f561_t * create_model( const char * );
      void destroy_model( VRegIncr_0x7a81360b75b3f561_t *);
      void eval( VRegIncr_0x7a81360b75b3f561_t * );
      void trace( VRegIncr_0x7a81360b75b3f561_t *, char * );

    ''')

    # Import the shared library containing the model. We defer
    # construction to the elaborate_logic function to allow the user to
    # set the vcd_file.

    s._ffi = s.ffi.dlopen('./libRegIncr_0x7a81360b75b3f561_v.so')

    # dummy class to emulate PortBundles
    class BundleProxy( PortBundle ):
      flip = False

    # define the port interface
    s.reset = InPort( 1 )
    s.in_ = InPort( 8 )
    s.clk = InPort( 1 )
    s.out = OutPort( 8 )

    # increment instance count
    RegIncr_0x7a81360b75b3f561.id_ += 1

    # Defer vcd dumping until later
    s.vcd_file = None

    # Buffer for line tracing
    s._line_trace_str = s.ffi.new("char[512]")
    s._convert_string = s.ffi.string

  def __del__( s ):
    s._ffi.destroy_model( s._m )

  def elaborate_logic( s ):

    # Give verilator_vcd_file a slightly different name so PyMTL .vcd and
    # Verilator .vcd can coexist

    verilator_vcd_file = ""
    if s.vcd_file:
      filen, ext         = os.path.splitext( s.vcd_file )
      verilator_vcd_file = '{}.verilator{}{}'.format(filen, s.id_, ext)

    # Construct the model.

    s._m = s._ffi.create_model( s.ffi.new("char[]", verilator_vcd_file) )

    @s.combinational
    def logic():

      # set inputs
      s._m.reset[0] = s.reset
      s._m.in_[0] = s.in_

      # execute combinational logic
      s._ffi.eval( s._m )

      # set outputs
      # FIXME: currently write all outputs, not just combinational outs
      s.out.value = s._m.out[0]

    @s.posedge_clk
    def tick():

      s._m.clk[0] = 0
      s._ffi.eval( s._m )
      s._m.clk[0] = 1
      s._ffi.eval( s._m )

      # double buffer register outputs
      # FIXME: currently write all outputs, not just registered outs
      s.out.next = s._m.out[0]

  def line_trace( s ):
    if 0:
      s._ffi.trace( s._m, s._line_trace_str )
      return s._convert_string( s._line_trace_str )
    else:
      return ""

