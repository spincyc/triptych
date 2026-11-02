import json,hashlib,sys
source,recipe,destination=sys.argv[1:]
b=open(source,"rb").read(); r=json.load(open(recipe)); assert hashlib.sha256(b).hexdigest()==r["input_sha256"]
lines=b.decode("utf-8").split("\n"); excluded={x["line"]:x["source"] for x in r["excluded_lines"]}
for i,s in excluded.items(): assert lines[i-1]==s
kept=[]
for i in r["ordered_physical_lines"]:
 kept.append("" if i in excluded else lines[i-1])
out="\n\n".join(" ".join(x.split()) for x in "\n".join(kept).split("\n\n") if x.strip())+"\n"
assert hashlib.sha256(out.encode()).hexdigest()==r["output_sha256"]
open(destination,"wb").write(out.encode())
