"""

To run: python ersp.py < result1.txt > out.txt

There is no need to set source or destination as vm137.sysnet.ucsd.edu:xxxxx,
simply set it to 'vm137', 'vm141', 'vm143', 'vm144', or empty string '' if it does not
matter

The output will be the Time Passed (s) column , a few empty lines for separation,
then the Size of Packets column

"""
import sys

def main():
    
    # SET CUSTOM VARIABLES HERE
    source = 'vm137'
    destination = ''
    # printing not in use anymore
    printing = 2 #0 to print times, 1 to print lengths, 2 to print sum of lengths
    
    list1 = []
    while True:
        try:
            list0 = list(sys.stdin.readline())
            if len(list0) == 1 and list0[0] == '\n':
                break
            if len(list0) == 0:
                break
            list1a = []
            curr = []
            for i in range(len(list0)):
                if list0[i] == ' ' or list0[i] == '\n':
                    s = ''.join(curr)
                    list1a.append(s)
                    curr = []
                    continue
                curr.append(list0[i]);
            list1.append(list1a)
            
        except (EOFError):
            break
    
    # print out list1 (for checking only)
    """
    for i in range(len(list1)):
        print list1[i]
    """

    # get starting time
    timestamp = str(list1[0][0])
    ind = 0
    time = 0
    start = 0
    for k in range(len(timestamp)):
        if timestamp[k] == ':' or timestamp[k] == '.':
            if ind == 0:
                start = start + time * 3600 # 3600s in an hour
            elif ind == 1:
                start = start + time * 60 # 60s in a minute
            elif ind == 2:
                start = start + time
                break
            ind = ind + 1
            time = 0
            continue
        time = time * 10 + int(timestamp[k])

    times = []
    lengths = []
    for i in range(len(list1)):
        if len(list1[i]) < 5:
            continue
        source_str = list1[i][2]
        dest_str = list1[i][4]
        src = (source_str.split('.'))[0]
        dest = (dest_str.split('.'))[0]
        if (src == source or source == '') and (dest == destination or destination == ''):
            # get timestamp
            timestamp = str(list1[i][0])
            ind = 0
            time = 0
            seconds = 0
            for k in range(len(timestamp)):
                if timestamp[k] == ':' or timestamp[k] == '.':
                    if ind == 0:
                        seconds += time * 3600 # 3600s in an hour
                    elif ind == 1:
                        seconds += time * 60 # 60s in a minute
                    elif ind == 2:
                        seconds += time
                        break
                    ind = ind + 1
                    time = 0
                    continue
                time = time * 10 + int(timestamp[k])
            
            # get length
            for j in range(5, len(list1[i])):
                if list1[i][j] == 'length':
                    times.append(seconds - start)
                    length_str = list1[i][j+1]
                    sum = 0
                    for k in range(len(length_str)):
                        if length_str[k] == ':':
                            break
                        sum = sum * 10 + int(length_str[k])
                    lengths.append(sum)
                    break

    if len(times) != len(lengths):
        print "Uh oh, something went wrong!"
        return
    if len(times) == 0:
        print "No results found"
        return

    # calculate combined lengths
    currtime = times[0]
    lengthsum = 0
    totalsum = 0
    combined_times = []
    combined_lengths = []
    combined_lengths_sum = []
    for i in range(len(times)):
        if times[i] == currtime:
            lengthsum = lengthsum + int(lengths[i])
            totalsum = totalsum + int(lengths[i])
        else:
            combined_times.append(currtime)
            currtime = times[i]
            combined_lengths.append(lengthsum)
            lengthsum = int(lengths[i])
            combined_lengths_sum.append(totalsum)

    # print depending on the value of printing
    """
    for i in range(len(combined_times)):
        if printing == 0:
            print combined_times[i]
        elif printing == 1:
            print combined_lengths[i]
        elif printing == 2:
            print combined_lengths_sum[i]
    """
    for i in range(len(combined_times)):
        print combined_times[i]
    print "\n\n\n\n"
    for i in range(len(combined_lengths)):
        print combined_lengths[i]

if __name__ == '__main__':
    main()
