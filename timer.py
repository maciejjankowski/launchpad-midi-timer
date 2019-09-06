import rtmidi
import time
import sys


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
            print("MIDI out:", port_name)
            if port_name.find('Launchpad Mini') > -1: 
                # or 'Launchpad Pro Standalone Port'
                return mo.open_port(port_no)


def prepare_message_xy(x, y, color):
    return [x + y * 0x10, color]


def prepare_message(position, color):
    return [NOTE_ON, position, color]


def light_up(position, color):
    raw_position = position // 8 * 0x10 + position % 8
    message = prepare_message(raw_position, color)
    midi_port.send_message(message)


def all_lights_off():
    for i in range(64):
        light_up(i, COLOR_OFF)


def count_down():
    minutes = 15
    if len(sys.argv) >= 2:
        try:
            float(sys.argv[1])
            minutes = float(sys.argv[1])
        except ValueError:
            print(f'\n\"{sys.argv[1]}\" not an integer or a float. Setted default time.') 
        finally:
            if minutes <= 1:
                print(f'\nCounting down {minutes} minute.')
            else: 
                print(f'\nCounting down {minutes} minutes.')
            interval = minutes * 60 / 64
            for i in range(64):
                light_up(i, COLOR_GREEN_FULL)
                time.sleep(interval)


if (__name__ == '__main__'):
    # main()
    midi_port = get_port()
    all_lights_off()
    count_down()
else:
    print("wat?", __name__)
