# Imitator of near real ingest pulse values stream
## Introducing 3 groups
### Each group has its own distribution of probability values 
#### Probabilities
- equaled probability distribution in [min, max] pulse values; distribution #1
- probability of the pulse value change; distribution #2
- probability of the change [2 - 6] percents, probability of the change [7 - 15] percents , probability of the change [16 - 50] percents, probability of the change [51 - 110] percents; distribution #3
- probability of increasing at the changing; distribution #4
### Common rules
- current pulse value cannot be lessa than min value and greater than max value
### Algorithm of creating the current pulse value
1. First pulse value is taken from distribution #1 (for example 70)
2. Next number is taken according to  distribution #2 <br>
2.1. Change probability. For example, prob = 15% , number from 1 to 100, if number <= 15 than there is a change (15%), otherwise no change<br>
2.2. Value of change is defined according distribution #3 . Example 20%, 10%, 50%, 20%
2.3. According  to distribution #4 either change value will be incremented or decremented
## Example of groups
### Group1
- [50-210]
- prob#2: 10%
- Prob#3.1 : 20%, Prob#3.2: 30%, Prob#3.3: 20%, Prob#3.4: 30%
- Prob#4 : 70%
### Group2
- [40-220]
- prob#2: 20%
- Prob#3.1 : 40%, Prob#3.2: 10%, Prob#3.3: 10%, Prob#3.4: 40%
- Prob#4 : 50%
### Group1
- [60-180]
- prob#2: 40%
- Prob#3.1 : 50%, Prob#3.2: 30%, Prob#3.3: 10%, Prob#3.4: 10%
- Prob#4 : 50%
## 5 devices
- device-1 belongs to group1
- device-2 belongs to group1
- device-3 belongs to group2
- device-4 belongs to group3
- device-5 belongs to group2
