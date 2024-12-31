#!/usr/bin/env python3
import os
import argparse
import threading
from inputs import UnpluggedError, get_gamepad

from cereal import messaging
from openpilot.common.numpy_fast import interp, clip
from openpilot.common.params import Params
from openpilot.common.realtime import Ratekeeper
from openpilot.system.hardware import HARDWARE
from openpilot.tools.lib.kbhit import KBHit


class Lightshow:
  def __init__(self):
    self.sequenceData = None
    self.lightshowData = {
      'headlights': False,
      'taillights': False
    }

  def readLightshowSequence(self):
    # TODO: Read lightshow sequence data from file
    return None

def exec_lightshow(lightshow):
  pm = messaging.PubMaster(['lightshowData'])

  rk = Ratekeeper(100, print_delay_threshold=None)

  while True:
    if rk.frame % 1000 == 0:
      break

    if rk.frame % 100 == 0:
      print("1 second?")

    lightshow_msg = messaging.new_message('lightshowData')
    lightshow_msg.valid = True
    lightshow_msg.lightshowData.headlights = rk.frame % 500 == 0
    lightshow_msg.lightshowData.taillights = rk.frame % 500 == 0

    pm.send('lightshowData', lightshow_msg)

    rk.keep_time()

def main():
  Params().put_bool('DoLightshow', True)

  lightshow = Lightshow()
  lightshow.readLightshowSequence()

  exec_lightshow(lightshow)

  Params().put_bool('DoLightshow', False)


if __name__ == '__main__':
  if not Params().get_bool("IsOffroad") and "ZMQ" not in os.environ:
    print("The car must be off before running lightshow_control.")
    exit()

  main()
