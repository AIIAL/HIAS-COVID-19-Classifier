#!/usr/bin/env python
""" Abstract class representing a HIAS AI Model.

Represents a HIAS AI Model. HIAS AI Models are used by AI Agents to process
incoming data.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files(the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Contributors:
- Adam Milton-Barker - First version - 2021-5-1

"""

import cv2
import json
import os
import random
import requests
import time

import tensorflow as tf

from numpy.random import seed

from abc import ABC, abstractmethod

from modules.data import data

class AbstractModel(ABC):
	""" Abstract class representing a HIAS AI Model.

	This object represents a HIAS AI Model. HIAS AI Models are used by AI Agents
	to process incoming data.
	"""

	def __init__(self, helpers):
		"Initializes the AbstractModel object."
		super().__init__()

		self.helpers = helpers
		self.confs = self.helpers.confs

		os.environ["KMP_BLOCKTIME"] = "1"
		os.environ["KMP_SETTINGS"] = "1"
		os.environ["KMP_AFFINITY"] = "granularity=fine,verbose,compact,1,0"
		os.environ["OMP_NUM_THREADS"] = str(
			self.helpers.confs["agent"]["cores"])
		tf.config.threading.set_inter_op_parallelism_threads(1)
		tf.config.threading.set_intra_op_parallelism_threads(
			self.helpers.confs["agent"]["cores"])

		self.data = data(self.helpers)

		self.testing_dir = self.helpers.confs["data"]["test"]
		self.valid = self.helpers.confs["data"]["valid_types"]

		self.helpers.logger.info("Model class initialization complete.")

	def http_request(self, img_path):
		""" Sends image to the inference API endpoint. """

		self.helpers.logger.info("Sending request for: " + img_path)

		_, img_encoded = cv2.imencode('.png', cv2.imread(img_path))
		response = requests.post(
			self.addr, data=img_encoded.tostring(), headers=self.headers)
		response = json.loads(response.text)

		return response

	@abstractmethod
	def prepare_data(self):
		""" Prepares the model data """
		pass

	@abstractmethod
	def prepare_network(self):
		""" Builds the network """
		pass

	@abstractmethod
	def train(self):
		""" Trains the model """
		pass

	@abstractmethod
	def freeze_model(self):
		""" Freezes the model """
		pass

	@abstractmethod
	def save_model_as_json(self):
		""" Saves the model as JSON """
		pass

	@abstractmethod
	def save_weights(self):
		""" Saves the model weights """
		pass

	@abstractmethod
	def load(self):
		""" Loads the model """
		pass

	@abstractmethod
	def visualize_metrics(self):
		""" Visualize the metrics. """
		pass

	@abstractmethod
	def confusion_matrix(self):
		""" Prints/displays the confusion matrix. """
		pass

	@abstractmethod
	def figures_of_merit(self):
		""" Calculates/prints the figures of merit. """
		pass

	@abstractmethod
	def evaluate(self):
		""" Evaluates the model """
		pass

	@abstractmethod
	def predictions(self):
		""" Makes predictions on the train & test sets. """
		pass

	@abstractmethod
	def predict(self, img):
		""" Gets a prediction for an image. """
		pass

	@abstractmethod
	def reshape(self, img):
		""" Reshapes the image. """
		pass

	@abstractmethod
	def test(self):
		"""Local test mode

		Loops through the test directory and classifies the images.
		"""
		pass

	@abstractmethod
	def test_http(self):
		""" HTTP test mode

		Loops through the test directory and classifies the images
		by sending data to the classifier using HTTP requests.
		"""
		pass
