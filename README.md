# qiskit2020
UCLA 239 Qiskit Project
# Use:


The following applies to each of the Deutsch-Jozsa and Bernstein-Vazirani Algorithms:
- Create an instance of the oracle circuit using a method in the dj.py or bv.py files (e.g. dj_oracle). In the case of the Deutsch-Jozsa algorithm, this takes the case (0 for balanced, 1 for constant) and a size n, whereas for Bernstein-Vazirani this takes the hidden string s and a size n. The proper call is `oracle = bv.bv_oracle(hiddenstr,n)`.
- Create an an instance of the corresponding class. For example, `groverObject = Grover()`.
- Create and execute the circuit by calling `xxxObject.run(circ,n)`, where `n` is number of bits that the function takes as input and `xxxObject` is your class instance. The return values are as follows:
  - Deutsch-Jozsa: The value of the 1024 trials Qiskit performs by default.
  - Bernstein-Vazirani: The value of the 1024 trials Qiskit performs by default. This should include `a`, the hidden string. . 

The following applies to each of the Simon's, and Grover's Algorithms:
- Create an an instance of the corresponding class. For example, `groverObject = Grover()`.
- Create your function `f` that takes an integer `x` as a parameter such that `log(x) < n`, where `n` is the number of input bits to your function. For example, instead of passing the binary integer `110` as input to `f`, one would pass the decimal integer `4`.
- Create and execute the circuit by calling `xxxObject.run(f,n)`, where `n` is number of bits that `f` takes as input and `xxxObject` is your class instance. The return values are as follows:
  - Simon's: the value `s` such that for any `x`, `y`, `f(x) = f(y)` iff `x XOR y = s`
  - Grover's: the integer value `x` such that `f(x) = 1`, where `f` is the input function. More directly, the function returns the value of the 1024 trials Qiskit performs by default, which includes `x`.
