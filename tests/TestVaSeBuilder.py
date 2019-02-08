#!/usr/bin/env python
# Import required libraries/modules
import unittest
import os
import sys

# Import required class
sys.path.insert(0, './../')
from VaSeBuilder import VaSeBuilder


# Unittest class for the VaSeBuilder class.
class TestVaSeBuilder(unittest.TestCase):
	
	# Set up requirements for this test class.
	def setUp(self):
		self.vsBuilder = VaSeBuilder("aap")
		self.varConMap = {'SNP16_247990':['16', 247986, 56508478]}
	
	
	# Tests that two variant reads are obtained
	def test_getVariantReads_pos(self):
		answerList = ['SRR1039513.12406160', 'SRR1039513.12406160']
		varReads = self.vsBuilder.getVariantReads("16", 247990, "testdata/valbam/SRR1039513.bam")
		varReadNames = [x.query_name for x in varReads]
		self.assertListEqual(varReadNames, answerList, "The lists should be identical but are not")
	
	# Tests that no reads are obtained
	def test_getVariantReads_neg(self):
		self.assertListEqual(self.vsBuilder.getVariantReads("16", 1, "testdata/valbam/SRR1039513.bam"), [], "Both list should be empty")
	
	
	
	# Tests that the context of BAM reads associated to a variant is determined correctly.
	def test_determineContext_pos(self):
		answerList = ["16", 247986, 56508478]
		varReads = self.vsBuilder.getVariantReads("16", 247990, "testdata/valbam/SRR1039513.bam")
		resultList = self.vsBuilder.determineContext(varReads)
		self.assertListEqual(resultList, answerList, "The contexts should have been the same.")
		
	# Test that the context of none existing BAM reads has no context.
	def test_determineContext_neg(self):
		answerList = []
		varReads = self.vsBuilder.getVariantReads("16", 1, "testdata/valbam/SRR1039513.bam")
		resultList = self.vsBuilder.determineContext(varReads)
		self.assertListEqual(resultList, answerList, "")
	
	
	
	# Tests that a variant at position 250000 is within the context [247986 .. 56508478]
	def test_isInContext_pos(self):
		self.vsBuilder.variantContextMap = self.varConMap
		self.assertTrue(self.vsBuilder.isInContext('16', 250000))
		self.vsBuilder.variantContextMap = {}	# Reset the variantContextMap of the vsBuilder object.
	
	# Tests that a variant at position 247985 is not in the context [247986 .. 56508478]
	def test_isInContext_neg(self):
		self.vsBuilder.variantContextMap = self.varConMap
		self.assertFalse(self.vsBuilder.isInContext('16', 247985))
		self.vsBuilder.variantContextMap = {}	# Reset the variantContextMap of the vsBuilder object.
	
	
	
	#Tests that a variant has already been processed.
	def test_variantAlreadyProcessed_pos(self):
		self.vsBuilder.variantContextMap = {}
		self.vsBuilder.variantContextMap = self.varConMap
		self.assertTrue(self.vsBuilder.variantAlreadyProcessed('SNP16_247990'))
	
	#Tests that a variant hasn't been processed.
	def test_variantAlreadyProcessed_neg(self):
		self.vsBuilder.variantContextMap = {}
		self.vsBuilder.variantContextMap = self.varConMap
		self.assertFalse(self.vsBuilder.variantAlreadyProcessed('SNP16_250000'))
		
