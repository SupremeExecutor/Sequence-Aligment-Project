import time
import psutil
import sys
import math

#Define mismatch cost:
mismatch_dict = {
    ('A','C'):110,
    ('C','A'):110,
    ('A','G'):48,
    ('G','A'):48,
    ('A','T'):94,
    ('T','A'):94,
    ('C','G'):118,
    ('G','C'):118,    
    ('C','T'):48,
    ('T','C'):48, 
    ('G','T'):110,  
    ('T','G'):110,  
    ('A','A'):0,
    ('C','C'):0,
    ('G','G'):0,
    ('T','T'):0
}

def main():
    input = sys.argv[1]
    output = sys.argv[2]

    file = open(input, "r")
    lines = file.readlines()
    str1 = lines[0].strip()
    n1 = []
    str2 = ""
    n2 = []
    parseStr2 = False
    for l in lines[1:]:
        l = l.strip()
        if l.isalpha():
            str2 = l
            parseStr2 = True
            continue
        if parseStr2:
            n2.append(int(l))
        else:
            n1.append(int(l))
    str1 = generateStr(str1, n1)
    str2 = generateStr(str2, n2)
    
    time, score, a1, a2 = time_wrapper(str1, str2)
    memory = process_memory()
    file_output(output, score, a1, a2, time, memory)
    return 0

def generateStr(str, n):
    for i in n:
        str = str[:i+1]+str+str[i+1:]
    return str

def print_alignment(aligned_s1,aligned_s2):
    num_to_print=len(aligned_s1)
    for i in range(num_to_print):
        print(aligned_s1[i],end="")
    print()
    for i in range(num_to_print):
        if aligned_s1[i] == aligned_s2[i]:
            print("|",end="")
        else:
            print(" ",end="")
    print()
    for i in range(num_to_print):
        print(aligned_s2[i],end="")

#output txt
def file_output(f, score, aligned_s1, aligned_s2, time, memory):
    with open(f, "+w") as file:
        file.write(str(score))
        file.write("\n")

        num_to_print=len(aligned_s1)

        for i in range(num_to_print):
            file.write(aligned_s1[i])
        file.write("\n")

        for i in range(num_to_print):
            file.write(aligned_s2[i])
        file.write("\n")
        
        file.write(str(time))
        file.write("\n")
        file.writelines(str(memory))

        file.close()

#calculate memory usage:
def process_memory():
    process = psutil.Process() 
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed

#calculate time usage:
def time_wrapper(s1, s2): 
    start_time = time.time() 
    score, a1, a2 = efficient_dp(s1, s2) #solution func
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    return time_taken, score, a1, a2

def showTable(t):
    for i in range(len(t)):
        print(t[i])
    return 0 
#solution function

def efficient_dp(s1, s2):
    if len(s1) <= 2 or len(s2) <= 2:
        return basic_dp(s1, s2)
    sl = s1[:len(s1)//2]
    sr = s1[len(s1)//2:]

    minscore = math.inf
    
    scorel = breakPoint(sl, s2)
    scorer = breakPoint(sr[::-1], s2[::-1])
    bestp = -1

    for i in range(len(s2)+1):
        # if i == len(s2):
        #     total = scorel[-1]+scorer[0]
        # if i == 0:
        #     total = scorel[0]+scorer[-1]
        total = scorel[i]+scorer[len(s2)-i]
        
        if total < minscore:
            bestp = i
            minscore = total
    
    score1, a11, a12 = efficient_dp(sl, s2[:bestp])
    score2, a21, a22 = efficient_dp(sr, s2[bestp:])
    
    return score1+score2, a11+a21, a12+a22

def breakPoint(s1, s2, match=0, gap=30):
    ncols = len(s2)+1
    scores = [[0 for _ in range(ncols)] for _ in range(2)]
    for i in range(len(s2)):
        scores[0][i+1] = s2[:i+1]
    scores[0][0] = "_"
    
    for i2 in range(ncols):
        if i2 == 0:
            scores[1][i2] = 0
        else:
            scores[1][i2] = gap*len(scores[0][i2])

    for i in range(len(s1)):
        temp = [0 for _ in range(ncols)]
        temp[0] = gap*(i+1)
        
        for j in range(1, ncols):
            
            opt1 = scores[1][j-1]
            align_score = match if s1[i] == scores[0][j][-1] else mismatch_dict[(s1[i],scores[0][j][-1])]
            score_opt1 = opt1 + align_score

            opt2 = scores[1][j]
            score_opt2 = opt2 + gap

            opt3 = temp[j-1]
            score_opt3 = opt3 + gap

            temp[j] = min(score_opt1, score_opt2, score_opt3)
            #print("temp after: ", temp)
        #print("score after: ", temp)
        scores[1] = temp
    #showTable(scores)
    return scores[1]

def basic_dp(s1, s2, match_score=0, gap_score=30):

    nrows = len(s1)+2
    ncols = len(s2)+2

    scores = [[ 0 for _ in range(ncols)] for _ in range(nrows)]
    aligned = [[ 0 for _ in range(ncols)] for _ in range(nrows)]

    scores[0][0] = ""
    scores[1][0] = '_'
    scores[0][1] = '_'
    aligned[0][0] = ""
    aligned[1][0] = '_'
    aligned[0][1] = '_'


    for i in range(len(s2)):
        scores[0][i+2] = s2[:i+1]
        aligned[0][i+2] = s2[:i+1]
    for j in range(len(s1)):
        scores[j+2][0] = s1[:j+1]
        aligned[j+2][0] = s1[:j+1]
        
    for s2_index in range(1, ncols):
        if s2_index == 1:
            scores[1][s2_index] = 0
            aligned[1][s2_index] = ("","")
        else:
            s2_part = scores[0][s2_index]
            scores[1][s2_index] = gap_score*len(s2_part)
            aligned[1][s2_index] = ("".join(["_" for i in range(len(s2_part))]),s2_part)

    for s1_index in range(1, nrows):
        if s1_index == 1:
            scores[s1_index][1] = 0
            aligned[s1_index][1] = ("","")
        else:
            s1_part = scores[s1_index][0]
            scores[s1_index][1] = gap_score*len(s1_part)
            aligned[s1_index][1] = (s1_part, "".join(["_" for i in range(len(s1_part))]))
    
   
    for i in range(2, nrows):
        for j in range(2, ncols):
            
            opt1_s1_index = i-1
            opt1_s2_index = j-1
            align_score = match_score if scores[i][0][-1] == scores[0][j][-1] else mismatch_dict[(scores[i][0][-1],scores[0][j][-1])]
            score_opt1 = scores[opt1_s1_index][opt1_s2_index] + align_score
            s1_aligned_opt1 = aligned[opt1_s1_index][opt1_s2_index][0]+aligned[i][0][-1]
            s2_aligned_opt1 = aligned[opt1_s1_index][opt1_s2_index][1]+aligned[0][j][-1]

            opt2_s1_index = i-1
            opt2_s2_index = j
            score_opt2 = scores[opt2_s1_index][opt2_s2_index] + gap_score
            s1_aligned_opt2 = aligned[opt2_s1_index][opt2_s2_index][0]+aligned[i][0][-1]
            s2_aligned_opt2 = aligned[opt2_s1_index][opt2_s2_index][1]+"_"
            
            opt3_s1_index = i
            opt3_s2_index = j-1
            score_opt3 = scores[opt3_s1_index][opt3_s2_index] + gap_score
            s1_aligned_opt3 = aligned[opt3_s1_index][opt3_s2_index][0]+"_"
            s2_aligned_opt3 = aligned[opt3_s1_index][opt3_s2_index][1]+aligned[0][j][-1]
            
            scores[i][j] = min(score_opt1,score_opt2,score_opt3)
            if min(score_opt1,score_opt2,score_opt3) == score_opt1:
                aligned[i][j] = (s1_aligned_opt1,s2_aligned_opt1)
            elif min(score_opt1,score_opt2,score_opt3) == score_opt2:
                aligned[i][j] = (s1_aligned_opt2,s2_aligned_opt2)
            else:
                aligned[i][j] = (s1_aligned_opt3,s2_aligned_opt3) 
            
    final_score = scores[nrows-1][ncols-1]
    aligned_s1 = aligned[nrows-1][ncols-1][0]
    aligned_s2 = aligned[nrows-1][ncols-1][1]
    
    return final_score, aligned_s1, aligned_s2



#main:
if __name__=="__main__": 
    main() 