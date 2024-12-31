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

  def readLightshowSequence(self):
    # TODO: Read lightshow sequence data from file
    return None

def exec_lightshow(lightshow):
  pm = messaging.PubMaster(['lightshowData'])

  rk = Ratekeeper(100, print_delay_threshold=None)

  while True:
    # max runtime of 10 seconds
    if rk.frame >= 1000:
      print("Finished lightshow")
      break

    lightshowData = {
      'headlights': rk.frame > 500,
      'taillights': rk.frame > 500
    }

    lightshow_msg = messaging.new_message('lightshowData')
    lightshow_msg.valid = True
    lightshow_msg.lightshowData.headlights = lightshowData['headlights']
    lightshow_msg.lightshowData.taillights = lightshowData['taillights']

    if rk.frame % 100 == 0:
      print('\n' + ', '.join(f'{name}: {v}' for name, v in lightshowData.items()))

    pm.send('lightshowData', lightshow_msg)

    rk.keep_time()

def main():
  Params().put_bool('DoLightshow', True)

  try:
    lightshow = Lightshow()
    lightshow.readLightshowSequence()

    exec_lightshow(lightshow)
  except Exception:
    print("Failed to run lightshow")
  finally:
    Params().put_bool('DoLightshow', False)


if __name__ == '__main__':
  if not Params().get_bool("IsOffroad") and "ZMQ" not in os.environ:
    print("The car must be off before running lightshow_control.")
    exit()

  main()
