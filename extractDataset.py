import ctakes_parser as parser

# Input directory should point to cTakes generared XMI-files
parser.ctakes_parser.parse_dir("inputDir", "dataset/cTakes/patients/training")