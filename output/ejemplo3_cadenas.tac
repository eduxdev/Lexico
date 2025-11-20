CÓDIGO INTERMEDIO (TAC)
====================================================================================================

   1. nombre = "Python"
   2. apellido = "Compiler"
   3. t0 = len(nombre)
   4. len_nombre = t0
   5. t1 = len(apellido)
   6. len_apellido = t1
   7. print(len_nombre)
   8. print(len_apellido)
   9. t2 = len_nombre > 5
  10. if_false t2 goto L0
  11. print(1)
  12. goto L1
  13. L0:
  14. print(0)
  15. L1:
  16. t3 = len_apellido > len_nombre
  17. if_false t3 goto L2
  18. print(1)
  19. goto L3
  20. L2:
  21. print(0)
  22. L3:
  23. t4 = []
  24. palabras = t4
  25. palabras.append(nombre)
  26. palabras.append(apellido)
  27. t5 = len(palabras)
  28. print(t5)
  29. saludo = "Hola"
  30. t6 = len(saludo)
  31. len_saludo = t6
  32. print(len_saludo)
  33. t7 = nombre == "Python"
  34. if_false t7 goto L4
  35. print(1)
  36. goto L5
  37. L4:
  38. print(0)
  39. L5:
  40. t8 = len(palabras)
  41. t9 = t8 == 2
  42. if_false t9 goto L6
  43. print(1)
  44. goto L7
  45. L6:
  46. print(0)
  47. L7:
