#thiss only uses the json package
import json

# Open the file for reading
in_file = open("sensorVar1.json","r")

# Load the contents from the file, which creates a new dictionary
new_dict = json.load(in_file)

# Close the file... we don't need it anymore  
in_file.close()

# Print the contents of our freshly loaded dictionary

print new_dict["sensorVar"]["tempVar"]


#out_file = open("sensorVar.json", "wb")

#json.dump(new_dict, out_file, indent=4)

#out_file.close()*/
