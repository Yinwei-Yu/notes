def perm1(arr,m):# 对于arr,生成从m开始的所有排列(前m-1个元素已经生成过了排列不要动)
    if m==len(arr):
        print(arr)
    for j in range(m,len(arr)):
        arr[j],arr[m] = arr[m],arr[j] # 为了生成m后的元素的排列,需要依次把后面的每一个元素拿到第一位,然后生成后面的排列
        perm1(arr,m+1) # 递归调用
        arr[j],arr[m] = arr[m],arr[j] # 恢复原状


n = 4
P = list(range(1,n+1))
perm1(P,0)
print("="*50)

def perm2(arr,m):
    if m==0:
      print(arr)
    for j in range(len(arr)):
        if arr[j]==0:
            arr[j]=m
            perm2(arr,m-1)
            arr[j]=0

n2 = 4
P2 = [0]*n
perm2(P2,n2)
