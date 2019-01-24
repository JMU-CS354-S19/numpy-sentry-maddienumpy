#!/usr/bin/env python

""" 
SentryBot lets us know if an intruder walks past.

Author: 
Version:
"""

import rospy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np


class SentryNode(object):
    """Monitor a vertical scan through the depth map and create an
    audible signal if the change exceeds a threshold.

    Subscribes:
         /camera/depth_registered/image
       
    Publishes:
        /mobile_base/commands/sound

    """

    def __init__(self):
        """ Set up the Sentry node. """
        rospy.init_node('sentry')
        self.cv_bridge = CvBridge()
        rospy.Subscriber('/camera/depth_registered/image',
                         Image, self.depth_callback, queue_size=1)
        rospy.spin()
	#vertical scan from previous callback 
	self.prev = None
	self.alpha = .3
	self.threshold = 1.2
	self.average = 1

    def depth_callback(self, depth_msg):
        """ Handle depth callbacks. """

        # Convert the depth message to a numpy array
        depth = self.cv_bridge.imgmsg_to_cv2(depth_msg)

        # YOUR CODE HERE.
        # HELPER METHODS ARE GOOD.
	depthArray = np.array(depth)
	
	#dimensions of the depthArray
	dim = depthArray.shape

	#middle column of the depthArray
	middle = dim[1]/2

	#current vertical scan
	curr = depthArray[:, middle - 1]
	curr = curr[~np.isnan(curr)]

	#if we have a prev scan then calculate the norm
	if not self.prev:
		norm = curr - prev
		norm = np.abs(norm)
		norm = norm.sum()
		self.average = self.average*self.alpha + norm*(1- self.alpha) 
	self.prev = curr

	if norm/self.average > self.threshold:
		#beep
		rospy.Publisher('/mobile_base/commands/sound', sound, queue = 1)

if __name__ == "__main__":
    SentryNode()
