#constant variables used by the ctf challenge

#length of plain text message
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

#time limit
time_limit = 30
