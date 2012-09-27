import pymongo

from clint.textui import puts, indent, colored

def is_balanced(output=False):
	
	connection = pymongo.Connection("localhost", 27017)

	chunks = {}
	nss = {}

	# Loop through each of the chunks, tallying things up
	for chunk in connection["config"]["chunks"].find():
		if "ns" in chunk:
			
			# Chunks per shard
			if chunk["ns"] in chunks:
				if chunk["shard"] in chunks[chunk["ns"]]:
					chunks[chunk["ns"]][chunk["shard"]] = chunks[chunk["ns"]][chunk["shard"]] + 1
				else:
					chunks[chunk["ns"]][chunk["shard"]] = 1
			else:
				chunks[chunk["ns"]] = {}
				chunks[chunk["ns"]][chunk["shard"]] = 1
			
			# Total chunks for the ns
			if chunk["ns"] in nss:
				nss[chunk["ns"]] = nss[chunk["ns"]] + 1
			else:
				nss[chunk["ns"]] = 1

	shardsCount = connection["config"]["shards"].count()
	chunksCount = connection["config"]["chunks"].count()

	# Different migration thresholds depending on cluster size
	# http://docs.mongodb.org/manual/core/sharding-internals/#sharding-migration-thresholds
	if chunksCount < 20:
		threshold = 2
	elif chunksCount < 80 and chunksCount > 21:
		threshold = 4
	else:
		threshold = 8

	isBalanced = True

	balanceStatus = {}

	# Loop through each ns and determine if it's balanced or not
	for ns in nss:
		balanced = nss[ns] / shardsCount

		if output == True:
			print ns

		balanceStatus[ns] = True

		for shard in chunks[ns]:
			if chunks[ns][shard] > balanced - threshold and chunks[ns][shard] < balanced + threshold:
				
				if output == True:
					with indent(4):
						puts(shard + colored.green(" balanced ") + "(" + str(chunks[ns][shard]) + ")")
			else:
				isBalanced = False
				balanceStatus[ns] = False
				if output == True:
					with indent(4):
						puts(shard + colored.red(" unbalanced ") + "(" + str(chunks[ns][shard]) + ")")

	return { "isBalanced" : isBalanced, "chunks" : chunks, "balanceStatus" : balanceStatus }