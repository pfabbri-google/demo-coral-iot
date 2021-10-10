# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import numpy as np
from PIL import Image
from PIL import ImageDraw
import cv2


class VirtualDisplay():

    def __init__(self, frame_size, display_title=""):
        self._frame_size = frame_size
        self._image = Image.new('RGB', (frame_size), 'white')
        self._title = display_title

    def show(self, msg, xy_offset=[0,0], delay_ms=1000):
        draw = ImageDraw.Draw(self._image)
        draw.rectangle([(0,0), (self._frame_size[0]-1,self._frame_size[1]-1)], 'black', 'white')
        draw.text((xy_offset), msg, fill='white')
        np_image = np.asarray(self._image)
        frame_bgr = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        cv2.imshow(self._title, frame_bgr)
        return cv2.waitKey(delay=delay_ms)
