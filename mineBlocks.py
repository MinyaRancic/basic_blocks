import re
import json

# Input: sudo perf script -F +brstackinsn,+cpu | xed -F insn: -A -64 > dump.txt

#want a datastrcutore func_name -> [bb list]

filename = "dump.txt"
#            a.out 55326 52484.139686:       6721 cycles:  ffffffffb87042ea rcu_accelerate_cbs ([kernel.kallsyms])
# binary idk idk: \d+ cycles:  address symbol ()

def parseFile(filename):
    outStruct = {}
    currFunc = None
    curr_block = []
    with open(filename, "r") as file:
        i = 0
        for line in file:
            #if i % 10000 == 0:
             #   print(i)
            #i += 1
            header_re = r"\s+\S+ \d+ \d+\.\d+:\s+(\d+) cycles:\s+\S+ (\S+)"
            inst_re = r"\s+\S+\s+(.*)"
            end_block_re = r".*\#"
            nothing_block_re = r"\s+\S+:"

            nothing_block_match = re.search(nothing_block_re, line)
            header_match = re.search(header_re, line)
            inst_match = re.search(inst_re, line)
            end_block_match = re.search(end_block_re, line)
            

            if header_match: # this is a header field
                function = header_match.group(2)
                cycles = header_match.group(1)
                if function not in outStruct:
                    outStruct[function] = []
                currFunc = function
                curr_block = []
            elif nothing_block_match:
                continue
            elif end_block_match:
                # print("End of Block Reached")
                curr_inst = inst_match.group(1)
                idx = curr_inst.find('#')
                curr_inst = curr_inst[0:idx].strip()
                curr_block.append(curr_inst)
                # print(curr_block)
                if curr_block not in outStruct[currFunc]:
                    outStruct[currFunc].append(curr_block)
                curr_block = []
            elif inst_match:
                # print(inst_match.group(1))
                # print(line)
                curr_block.append(inst_match.group(1))
    # print(json.dumps(outStruct, indent = 4))
    return outStruct

def compareInstructions(inst1, inst2):
    split1 = inst1.split(' ')
    split2 = inst2.split(' ')
    # print(split1[0])
    return split1[0] == split2[0]

def compareBlocks(block1, block2):
    for (inst1, inst2) in zip(block1, block2):
        if not compareInstructions(inst1, inst2):
            return False

    return True

def findCommonBlocks(func1, func2):
    commonBlocks = []
    for block1  in func1:
        for block2 in func2:
            if compareBlocks(block1, block2):
                commonBlocks.append(block1)
            else:

    return commonBlocks

block_struct = parseFile(filename)

print("Done Parsing!")

func1 = block_struct['foo']
func2 = block_struct['bar']

# print(func1)
# print(func2)


print(findCommonBlocks(func1, func2))
