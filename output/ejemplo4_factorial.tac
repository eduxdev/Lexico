CÓDIGO INTERMEDIO (TAC)
====================================================================================================

   1. func_factorial:
   2. t0 = n == 0
   3. if_false t0 goto L0
   4. return 1
   5. goto L1
   6. L0:
   7. t1 = n - 1
   8. temp = t1
   9. t2 = factorial(temp)
  10. result = t2
  11. t3 = n * result
  12. return t3
  13. L1:
  14. return
  15. t4 = factorial(0)
  16. resultado1 = t4
  17. print(resultado1)
  18. t5 = factorial(1)
  19. resultado2 = t5
  20. print(resultado2)
  21. t6 = factorial(3)
  22. resultado3 = t6
  23. print(resultado3)
  24. t7 = factorial(5)
  25. resultado4 = t7
  26. print(resultado4)
