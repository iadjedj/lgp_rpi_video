# Create a text file using the following format
#
# file 'video1.mp4'
# file 'video2.mp4'
# file 'video3.mp4'
#
# then launch

ffplay -f concat -loop 0 -i mylist.txt