#!/usr/bin/env python
# Import required modules/libraries 
import unittest
import os

# Import required class
from ParamChecker import ParamChecker


# Unittest class for the ParamChecker test.
class TestParamChecker(unittest.TestCase):
	
	# Set up required 
	def setUp(self):
		self.paramCheck = ParamChecker()
		self.paramList = {'vcfin': 'testdata/vcfDir',
			'bamin': 'testdata/bamDir',
			'valbam': 'testdata/valbam.bam',
			'valfastq1': 'testdata/fqDir/vaseval_F.fq.gz',
			'valfastq2': 'testdata/fqDir/vaseval_R.fq.gz',
			'fastqout': 'testdata/outDir',
			'varcon': 'testdata/outDir/varcon.txt',
			'varbread': 'testdata/outDir/varbread.txt',
			'nistbread': 'testdata/outDir/nistbread.txt'
		}
	
	
	
	# Tests that the --log will be written to the log file.
	def test_checkLog_pos(self):
		assertEqual(self.paramCheck.checkLog("testdata/outDir/vaseutest.log"), "testdata/outDir/vaseutest.log", "The log location should have been testdata/outDir/vaseutest.log")
	
	# Tests that the --log parameter has not been set and the log will therfore be written to VaSeBuilder.log 
	def test_checkLog_noParamSet(self):
		assertEqual(self.paramCheck.checkLog(None), "VaSeBuilder.log", "The log location should have been VaSeBuilder.log")
	
	# Tests that the --log parameter has been set but the filename does not end with .log and will therefore be written to VaSeBuilder.log
	def test_checkLog_noLog(self):
		assertEqual(self.paramCheck.checkLog("testdata/outDir/logfile.file"), "VaSeBuilder.log", "The log location should have been VaSeBuilder.log")
	
	# Test that the --log parameter has been set but the filename does not end with .txt  and will therefore be written to VaSeBuilder.log
	def test_checkLog_noTxt(self):
		assertEqual(self.paramCheck.checkLog("testdata/outDir/logfile.file"), "VaSeBuilder.log", "The log location should have been VaSeBuilder.log")
	
	
	
	# Tests that the povided testdata folder 'bamDir' indeed contains two BAM files.
	def test_checkFolderContents_pos(self):
		assertEqual(self.paramCheck.checkFolderContents("testdata/bamDir", "bam"), 2, "Two bam files should have been found")
	
	# Tests that the provided testdata folder 'bamDir' contains no VCF files
	def test_checkFolderContents_neg(self):
		assertEqual(self.paramCheck.checkFolderContents("testdata/bamDir", "vcf"), 0, "No VCF files should have been found")
	
	
	
	# Tests that the provided testdata folder 'bamDir' exists and contains BAM files.
	def test_checkFoldersExist_pos(self):
		assertListEqual(self.paramCheck.checkFoldersExist(['testdata/bamDir'], 'bam'), ['testdata/bamDir'], "The folder should have been testdata/bamDir")
	
	# Tests that the provided testdata folder 'bamDir' exists and does not contain VCF files.
	def test_checkFoldersExist_neg(self):
		assertListEqual(self.paramCheck.checkFoldersExist(['testdata/bamDir'], 'vcf'), [], "There should be no folder")
	
	
	
	# Tests that a provided file indeed exists.
	def test_checkFileExists_pos(self):
		assertTrue(self.paramCheck.checkFileExists("testdata/bamDir/vaseutest_1.bam") , "File should exist")
	
	# Tests whether a non existing file indeed does not exist.
	def test_checkFileExists_neg(self):
		assertFalse(self.paramCheck.checkFileExists(""), "There should be no file")
	
	
	
	# Test that the output location for out.txt is valid.
	def test_isValidOutputLocation_pos(self):
		assertTrue(self.paramCheck.isValidOutputLocation("testdata/outDir/out.txt"))
	
	# Test that the output location for out.txt is invalid.
	def test_isValidOutputLocation_neg(self):
		assertFalse(self.paramCheck.isValidOutputLocation("testdata/doesnotexist/out.txt"))
	
	
	
	# Tests that the foldername a file is located in gets returned properly.
	def test_getFolderName_pos(self):
		assertEqual(self.paramCheck.getFolderName("testdata/noSampleDir/noSampleBam.bam"), "noSampleDir", "Folder names should be equal bur are not")
	
	# Test that the foldername is empty.
	def test_getFolderName_neg(self):
		assertEqual(self.paramCheck.getFolderName(""), "", "Folder names should both be empty.")
	
	
	
	# Tests that all provided parameters are ok. First test should return True, all others false due to one parameter missing
	def test_checkParameters_pos(self):
		assertTrue(self.paramCheck(self.paramList))
	
	def test_checkParameters_noVcfIn(self):
		parList = self.paramList.copy()
		parList['vcfin'] = 'testdata/doesnotexist'	# Set the list VCF folders to a folder that does not exist.
		assertFalse(self.paramCheck(parList))
	
	def test_checkParameters_noBamIn(self):
		parList = self.paramList.copy()
		parList['bamin'] = 'testdata/doesnotexist'	# Set the list BAM folders to a folder that does not exist.
		assertFalse(self.paramCheck(parList))
	
	def test_checkParameters_noValBam(self):
		parList = self.paramList.copy()
		parList['valbam'] = 'testdata/doesnotexist.bam'	# Set the location of the bam file to one that does not exist.
		assertFalse(self.paramCheck(parList))
	
	def test_checkParameters_noValFq1(self):
		parList = self.paramList.copy()
		parList['valfastq1'] = 'testdata/doesnotexist.fq'	# Set the location of the fastq file to one that does not exist.
		assertFalse(self.paramCheck(parList))
	
	def test_checkParameters_noValFq2(self):
		parList = self.paramList.copy()
		parList['valfastq2'] = 'testdata/doesnotexist.fq'	# Set the location of the fastq file to one that does not exist.
		assertFalse(self.paramCheck(parList))
	
	def test_checkParameters_noFqOut(self):
		parList = self.paramList.copy()
		parList['fastqout'] = 'testdata/doesnotexist/faqOut.fq'	# Set the output location of the fastq file to a folder that does not exist
		assertFalse(self.paramCheck(parList))
	
	def test_checkParameters_noVarcon(self):
		parList = self.paramList.copy()
		parList['varcon'] = 'testdata/doesnotexist/varcon.txt'	# Set the location for the varcon output file to a folder that does not exist.
		assertFalse(self.paramCheck(parList))
	
	def test_checkParameters_noVarBread(self):
		parList = self.paramList.copy()
		parList['varbread'] = 'testdata/doesnotexist/varbread.txt'	# Set the location for the varbread output file to a folder that does not exist.
		assertFalse(self.paramCheck(parList))
	
	def test_checkParameters_noNistBread(self):
		parList = self.paramList.copy()
		parList['nistbread'] = 'testdata/doesnotexist/nistbread.txt'	# Set the location for the nistbread output file to a folder that does not exist.
		assertFalse(self.paramCheck(parList))
	
	
	
	# Clean up
	def tearDown(self):
		self.paramCheck.dispose()
		self.paramList.dispose()
