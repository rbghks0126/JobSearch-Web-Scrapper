import csv

def save_to_file(jobs):
  out_file = open("jobs.csv", mode="w")
  writer = csv.writer(out_file)
  writer.writerow(["Title", "Company", "location", 
  "link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  out_file.close()
  return