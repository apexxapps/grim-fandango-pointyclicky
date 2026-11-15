#!/usr/bin/env python3
"""tap2.py <feet x> <feet y> <ds>: tap 110 px above Manny's line for ds units along the push (+) or pull (-), near x 400 in tr setup 2."""
import sys
fx, fy, s = map(float, sys.argv[1:4])
print('%d %d' % (round(fx + s * 48 * 0.985 + 110 * 0.17), round(fy + s * 48 * 0.17 - 110 * 0.985)))
