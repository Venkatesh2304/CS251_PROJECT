import os 
os.system("cat out_* > output.txt") 
with open("output.txt") as f : 
     lines = f.read().split("\n")
     values = []
     for i in lines : 
         if "sent" in i : 
             values.append([True,float(i.split(" ")[1])])
         if "rece" in i : 
             values.append([False,float(i.split(" ")[1])])
    
     values.sort(key = lambda x : x[1])
     t = values[int(len(values)/2)][1] 
     delta = 5
    #  print(values[-1][1] - values[0][1])
     window = [ i for i in values if abs(i[1] - t) <= delta ]
     x , y = 0 , 0  
     for i in window : 
         if i[0] :
            x += 1 
         else : 
            y += 1 
     input_thr = x/delta  
     output_thr = y/delta  
     l = len([ i for i in values if i[0]])
     #print( l ,len([ i[1] for i in values if  not i[0] ]) )
     latency = (sum([ i[1] for i in values if  not i[0] ][:l]) - sum([ i[1] for i in values if  i[0] ])) / l
     print("Latency :: ", latency)
     print("InputThroughPut :: ",input_thr)
     print("OutputPut :: ",output_thr)

         