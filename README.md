# DASTR
Red-black tree and Binonial heap implementation 
Binomial heap
![image](https://user-images.githubusercontent.com/50024077/187700538-9ef7446e-7508-462b-b669-fb7b6261a3ce.png)

insert - 1, 2, 3, 4, 5, 6, 7
  - tree 0 - has root with key 7
  - tree 1 - has root with key 5
           - has left child with key 6
  - tree 2 - has root with key 1
           - has left child with key 3
           - has right child with key 2
           - node 3 has left child with key 4
delete smallest is anagolic 

RBT

![image](https://user-images.githubusercontent.com/50024077/187701702-30e08920-f5b7-4b90-b0cb-f867a653e01f.png)

insert - 5, 3, 8, 1, 4, 6, 9, 7, 10
  - root is 5 (black)
  - right child of 5 is 8 (red)
      - right child of 8 is 6 (black)
        - right child of 6 is 7 (red)
      - right child of 8 is 9 (black)
        - right child of 9 is 10 (red)
  - left child of 5 is 3 (black)
    - left child of 3 is 1 (red)
    - right child of 3 is 4 (red)
