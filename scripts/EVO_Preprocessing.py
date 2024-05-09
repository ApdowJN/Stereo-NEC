import csv
import sys
import os.path

# Checking if the correct number of arguments is passed
if len(sys.argv) < 3:
    print("Please provide input file name as an argument.")
    print("Example: python EVO_Preprocessing.py est.txt est.csv gt.csv")
    exit()

# # Check if the input file exists
# if not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
#     print("Invalid input file path.")
#     print("Example: python EVO_Preprocessing.py est.csv gt.csv")
#     exit()

# # Get input filename from command line argument
est_txt_file = sys.argv[1] #txt
est_file = sys.argv[2] #csv
gt_file =  sys.argv[3] #csv

# Open the input file
# with open(est_txt_file, 'r') as infile:
#       plaintext = infile.read()

# plaintext = plaintext.replace(' ', ',')

# with open(est_file, 'w') as f:
#     f.write(plaintext)

with open(est_file, 'r') as infile:
    # Create a CSV reader
    reader = csv.reader(infile)

    # Skip the first row
    next(reader)

    # Open the output file
    output_file = est_file.split('.')[0] + '_tum.csv'
    with open(output_file, 'w') as outfile:

        # Create a CSV writer with space delimiter
        writer = csv.writer(outfile, delimiter=' ')

        # Process each row
        for row in reader:

            # Switch the 4th and 7th columns
            row[4], row[7] = row[7], row[4]

            # Write the modified row to the output file
            writer.writerow(row)


# with open(gt_file, 'r') as infile:

#     # Create a CSV reader
#     reader = csv.reader(infile)

#     # Skip the first row
#     next(reader)

#     # Open the output file
#     output_file = gt_file.split('.')[0] + '_euroc.csv'
#     with open(output_file, 'w') as outfile:

#         # Create a CSV writer with space delimiter
#         writer = csv.writer(outfile, delimiter=',')

#         # Process each row
#         for row in reader:

#             # Multiply the first column by 1e9
#             row[0] = str(float(row[0]) * 1e9)

#             # Write the modified row to the output file
#             writer.writerow(row)