def max_number(arr):
  ans,hp = 0,0
  for n in arr:
    if hp == 0 :
      ans,hp =n,1
    else: hp+=1 if ans == n else -1
  print(ans)

v = [1,1,2,2,2,2,2,2,2,2,2,3,4,5,6,6,6]
max_number(v)