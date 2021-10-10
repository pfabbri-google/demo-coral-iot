# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time 
import logging
import argparse
import itertools
import numpy as np

from core import CloudIot

logger = logging.getLogger(__name__)

if os.getenv('DEVICE')=='LOCAL_MACHINE':
    print('Running on local machine')
    from display_emulator import VirtualDisplay
    RUN_ON_CORAL = False
    CONFIG_SECTION = 'LOCAL'
    virtual_display =  VirtualDisplay((128, 32))
    enviro = None
else:
    print('Assuming running on Coral')
    from luma.core.render import canvas
    from coral.enviro.board import EnviroBoard
    RUN_ON_CORAL = True
    CONFIG_SECTION = 'DEFAULT'
    enviro = EnviroBoard()

    

CONFIG_DEFAULT = os.path.join(os.path.dirname(__file__), 'device_config.ini')


def update_display(display, msg):
    with canvas(display) as draw:
        draw.text((0, 0), msg, fill='white')

def _none_to_nan(val):
    return float('nan') if val is None else val

def create_callback(enviro):
    callbacks = {}
    def on_message(unused_client, unused_userdata, message):
        payload = str(message.payload)
        print('received command msg: {}'.format(payload))
        if enviro:
            update_display(enviro.display, payload)

    callbacks['on_message'] = on_message
    return callbacks


def main():
    # Pull arguments from command line.
    parser = argparse.ArgumentParser(description='Cloud IoT Demo')
    parser.add_argument('--display_duration',
                        help='Measurement display duration (seconds)', 
                        type=int,
                        default=5)
    parser.add_argument('--upload_delay', 
                        help='Cloud upload delay (seconds)',
                        type=int, 
                        default=60)
    parser.add_argument('--cloud_config_file',
                        help='Cloud IoT config file',
                        default=CONFIG_DEFAULT)
    parser.add_argument('--cloud_config_section',
                        help='Cloud IoT config section',
                        default=CONFIG_SECTION)
    
    args = parser.parse_args()

    sensors = {} 
    with CloudIot(args.cloud_config_file, args.cloud_config_section) as cloud:
        # Indefinitely update display and upload to cloud.

        cloud.register_message_callbacks(create_callback(enviro))
        
        for read_count in itertools.count():
            if RUN_ON_CORAL:
                sensors['temperature'] = enviro.temperature
                sensors['humidity'] = enviro.humidity
                sensors['ambient_light'] = enviro.ambient_light
                sensors['pressure'] = enviro.pressure
            else:
                sensors['temperature'] = np.random.randint(24,27)
                sensors['humidity'] = np.random.randint(53,55)
                sensors['ambient_light'] = np.random.randint(900,1000)
                sensors['pressure'] = np.random.randint(999,1010)   

            # First display temperature and RH.
            msg = 'T:%.2f C,' % _none_to_nan(sensors['temperature'])
            msg += 'H:%.2f %%\n' % _none_to_nan(sensors['humidity'])
            msg += 'L:%.2f lux,' % _none_to_nan(sensors['ambient_light'])
            msg += 'P:%.2f kPa\n' % _none_to_nan(sensors['pressure'])
           
            if RUN_ON_CORAL:
                update_display(enviro.display, msg)
                time.sleep(args.upload_delay)
            else:
                virtual_display.show(msg, delay_ms=1)

            # Attempt cloud upload.
            if cloud.enabled():
                cloud.publish_message(sensors)


if __name__ == '__main__':
    main()