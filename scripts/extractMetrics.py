import json, re

"""
extract all the metrics of all the cite numbers (e.g. "[41]") from data.json
and write in metrics.json with this structure:
{
	"[41]": ["metric_1", "metric_2", ...],
	"[42]": [...],
	...
}

"""

with open("..\\..\\data.json", encoding="utf-8") as file:
	data = json.load(file)

out_metrics = {}


for i in data:
	for j in i["LearningActivities"]:
		for k in j["indicator"]:
			cite_nr = set(re.findall(r"\[[\d]*\]", k["metrics"]))
			cite_nr = cite_nr.pop()
			metrics = [i.replace(cite_nr[:-1], "").strip() for i in k["metrics"].split("],")]
			metrics[-1] = metrics[-1][:-1].strip() 
			#print(metrics)
			#print(cite_nr)
			if cite_nr in out_metrics:
				if metrics != out_metrics[cite_nr]:
					pass
					#out_metrics[cite_nr+"²"] = metrics
			else:
				out_metrics[cite_nr] = metrics
			#break
		#break
	#break

with open("..\\..\\metrics.json", "w", encoding="utf-8") as file:
	json.dump(out_metrics, file, indent=4, default=str)
