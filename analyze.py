import argparse
from utils.leaderdensity import LeaderDensity

def main():
	"""
	Main function for analyze
	"""
	parser = argparse.ArgumentParser(description='analyze - a capability to perform leadership and density graph analytics on information security data.')
	parser.add_argument("data",action='store',help='specify the input data for graph creation, can be file or folder')
	parser.add_argument('edges', action='store', help='specify the edges for the graph to create in the form of NodeX--NodeY,NodeY--NodeZ,...',metavar='edges')
	parser.add_argument("-v","--verbose", help="run analyze in verbose mode",action="store_true")
	parser.add_argument("-i","--inverse",help="run analyze and return inverse values",action="store_false")
	#parser.add_argument("-o","--output",type=str,action="store",help="specify file location to output results",metavar="file") # to be added
	'''
	# To be added 
	SplunkIngestType =parser.add_argument_group('SPLUNK INPUT ARGUMENTS')
	SplunkIngestType.add_argument('-url', dest='baseurl', type=str, action='store',
								  help='specify the url for the Splunk REST API (normally port 8089)',
								  metavar='https://[SPLUNK IP]:port')
	SplunkIngestType.add_argument('-user', dest='user_name', type=str, action='store',
								  help='specify the username for the splunk user', metavar='username')
	SplunkIngestType.add_argument('-pass', dest='user_pass', type=str, action='store',
								  help='specify the password for the splunk user', metavar='password')
	SplunkIngestType.add_argument('-trainquery', dest='trainquery', type=str, action='store',
								  help='specify splunk query for training time, use \'earliest=\' and \'latest=\' to specify timeframe',
								  metavar='trainquery')
	SplunkIngestType.add_argument('-testquery', dest='testquery', type=str, action='store',
								  help='specify splunk query for testing time, use \'earliest=\' and \'latest=\' to specify timeframe',
								  metavar='testquery')
	'''
	args=parser.parse_args()

	# Instantiate the Predictor class
	graph=LeaderDensity(args.verbose)

	# Ingest data
	graph.ingest_folder(args.data)

	# Check for input errors
	graph.feature_check(args.edges)

	# Process Graph
	graph.process()

	# Analyze Graph
	if args.inverse:
		graph.leadership()
		print(f'Leadership Value: {graph.return_leadership()}')
		graph.density()
		print(f'Density Value: {graph.return_density()}')
	else:
		graph.inv_leadership()
		print(f'Inverse Leadership Value: {graph.return_inv_leadership()}')
		graph.inv_density()
		print(f'Inverse Density Value: {graph.return_inv_density()}')


if __name__=="__main__":
	try:
		main()
	except Exception as err:
		print(repr(err))