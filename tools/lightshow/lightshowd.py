#!/usr/bin/env python3

from cereal import messaging
from openpilot.common.realtime import Ratekeeper
from openpilot.common.swaglog import cloudlog


def lightshowd_thread():
  cloudlog.info("lightshowd is running")
  sm = messaging.SubMaster(['lightshowData'], frequency=100)
  pm = messaging.PubMaster(['carControl'])

  rk = Ratekeeper(100, print_delay_threshold=None)

  while True:
    sm.update(0)

    cc_msg = messaging.new_message('carControl')
    cc_msg.valid = True
    CC = cc_msg.carControl
    CC.leftBlinker = sm['lightshowData'].leftBlinker
    CC.rightBlinker = sm['lightshowData'].rightBlinker

    pm.send('carControl', cc_msg)

    rk.keep_time()

def main():
  lightshowd_thread()


if __name__ == "__main__":
  main()
