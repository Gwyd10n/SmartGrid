#!/usr/bin/env python
# Gwydion Oostvogel, Sophie Schubert

import sys
from helpers.clui import clui
from helpers.clui_test import clui_test
from helpers.kmeans import kmeans
# from helpers.helpers import move


if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        clui_test()
    else:
        clui()
