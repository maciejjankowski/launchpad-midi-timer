import rtmidi
import time
import sys

MINUTES_ARG = 15
if len(sys.argv) > 1:
    MINUTES_ARG = int(sys.argv[1])


NOTE_ON = 0x90
CLEAR_MESSAGE = [176, 0, 0]

COLOR_OFF = 0x0C
COLOR_RED_LOW = 0x0D
COLOR_RED_FULL = 0x0F
COLOR_AMBER_LOW = 0x1D
COLOR_AMBER_FULL = 0x3F
COLOR_YELLOW_FULL = 0x3E
COLOR_GREEN_LOW = 0x1C
COLOR_GREEN_FULL = 0x3C

midi_port = ''

def get_port():
    global midi_port
    mo = rtmidi.MidiOut()
    for port_no in range(mo.get_port_count()):
            port_name = mo.get_port_name(port_no)
            # print("MIDI out:", port_name)
            if port_name.find('Launchpad Mini') > -1: 
                # or 'Launchpad Pro Standalone Port'
                return mo.open_port(port_no)


def prepare_message_xy(x, y, color):
    return [x + y * 0x10, color]


def prepare_message(position, color):
    return [NOTE_ON, position, color]


def clear():
    midi_port.send_message(CLEAR_MESSAGE)

def light_up(position, color):
    raw_position = position // 8 * 0x10 + position % 8
    message = prepare_message(raw_position, color)
    midi_port.send_message(message)


def count_down(minutes=MINUTES_ARG):
    interval = minutes * 60 / 64
    for i in range(64):
        light_up(i, COLOR_GREEN_FULL)
        time.sleep(interval)
    flash(5)

def flash(times, from_color=COLOR_RED_FULL, to_color=COLOR_OFF):
    for i in range(64):
        light_up(i, from_color)
    time.sleep(0.1)
    for i in range(64):
        light_up(i, to_color)
    time.sleep(0.1)

if (__name__ == '__main__'):
    # main()
    midi_port = get_port()
    clear()
    count_down()
else:
    print("wat?", __name__)
