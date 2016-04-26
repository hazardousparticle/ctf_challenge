#constant variables used by the ctf challenge

#length of plain text message
# should be 16, 24 or 32 bytes for AES 128, 192 and 256
MESSAGE_LENGTH=32


#add to start and end of message then encrypt.
#so user knows when they have found the correct password
KNOWN_MSG_START=b"#$!PASS="
KNOWN_MSG_END=b"=WORD!$#"

#key range
MIN_KEY=400
#keep the key + char less than 0x03ff
MAX_KEY=(0x03ff - ord('z'))

#message which must be AES'd
KNOWN_MESSAGE=b"Let Me In!"

#time limit (secs) takes about 10 ms to bruteforce
time_limit = 1

#log file:
log_file_name = "winners.log"


#tcp server settings
port = 37133
max_threads = 20
use_ip6 = False #TODO: automatically detect this
