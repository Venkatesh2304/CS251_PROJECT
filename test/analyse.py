import os 
os.system("tail out_* > output.txt") 
with open("output.txt") as f : 
     lines = f.read().split("\n")
     t1 = 0
     t2 = 20
     t = t2 - t1 
     values = []
     for i in lines : 
         if "sent" in i : 
             values.append([True,float(i.split(" ")[1])])
         if "rece" in i : 
             values.append([False,float(i.split(" ")[1])])
         
     values.sort(key = lambda x : x[1])
     window = values[t1:t2]
     x , y = 0 , 0 
     for i in window : 
         if i[0] :
            x += 1 
         else : 
            y += 1 
     input_thr = x/t * 1000 
     output_thr = y/t * 1000 
     
     print("InputThroughPut :: ",input_thr)
     print("OutputPut :: ",output_thr)

         