import balanced
import datetime

class MongoBalanced (object):
	def __init__(self, agentConfig, checksLogger, rawConfig):
		self.agentConfig = agentConfig
		self.checksLogger = checksLogger
		self.rawConfig = rawConfig
		self.nextCheck = None

	def run(self):
		
		if self.nextCheck == None or datetime.datetime.utcnow() >= self.nextCheck:
			
			result = balanced.is_balanced()

			response = {}

			# For the graphs
			for chunk in result["chunks"]:
				for shard in result["chunks"][chunk]:
					response[chunk.replace(".", "-") + "-" + shard] = result["chunks"][chunk][shard]

			# For alerts
			for ns in result["balanceStatus"]:
				if result["balanceStatus"][ns] == True:
					response[ns.replace(".", "-")] = 1
				else:
					response[ns.replace(".", "-")] = 0
			
			if result["isBalanced"] == True:
				response["isBalanced"] = 1
			else:
				response["isBalanced"] = 0

			self.nextCheck = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

			return response

		else:

			return None