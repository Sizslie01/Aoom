"""
File:                       pulse_out.py

Library Call Demonstrated:  mcculw.ul.pulse_out_start()
                            mcculw.ul.pulse_out_stop()

Purpose:                    Controls an Output Timer Channel.

Demonstration:              Sends a frequency output to Timer 0.

Other Library Calls:        mcculw.ul.release_daq_device()

Special Requirements:       Device must have a Timer output.
"""
from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

from time import sleep


from mcculw import ul
from mcculw.enums import CounterChannelType
from mcculw.device_info import DaqDeviceInfo


try:
    from console_examples_util import config_first_detected_device
except ImportError:
    from .console_examples_util import config_first_detected_device


def run_example():
    # By default, the example detects and displays all available devices and
    # selects the first device listed. Use the dev_id_list variable to filter
    # detected devices by device ID (see UL documentation for device IDs).
    # If use_device_detection is set to False, the board_num variable needs to
    # match the desired board number configured with Instacal.
    use_device_detection = True
    dev_id_list = []
    board_num = 0

    try:
        if use_device_detection:
            config_first_detected_device(board_num, dev_id_list)

        daq_dev_info = DaqDeviceInfo(board_num)
        if not daq_dev_info.supports_counters:
            raise Exception('Error: The DAQ device does not support counters')

        print('\nActive DAQ device: ', daq_dev_info.product_name, ' (',
              daq_dev_info.unique_id, ')\n', sep='')

        ctr_info = daq_dev_info.get_ctr_info()

        # Find a pulse timer channel on the board
        first_chan = next((channel for channel in ctr_info.chan_info
                           if channel.type == CounterChannelType.CTRPULSE),
                          None)

        if not first_chan:
            raise Exception('Error: The DAQ device does not support '
                            'pulse timers')

        timer_num = first_chan.channel_num
        frequency = 100
        duty_cycle = 0.5

        # Start the pulse timer output (optional parameters omitted)
        actual_frequency, actual_duty_cycle, _ = ul.pulse_out_start(
            board_num, timer_num, frequency, duty_cycle)

        # Print information about the output
        print('Outputting', actual_frequency, 'Hz with a duty cycle of',
              actual_duty_cycle, 'to pulse timer channel', timer_num)

        # Wait for 5 seconds
        sleep(5)

        # Stop the pulse timer output
        ul.pulse_out_stop(board_num, timer_num)
        print('Timer output stopped')
    except Exception as e:
        print('\n', e)
    finally:
        if use_device_detection:
            ul.release_daq_device(board_num)


if __name__ == '__main__':
    run_example()
