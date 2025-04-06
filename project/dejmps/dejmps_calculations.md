## DEJMPS

Bell state:
$$
\begin{equation}
\ket{\phi_{00}} = \frac{1}{\sqrt{2}} \left(\ket{00} + \ket{11}\right)
\end{equation}
$$

Werner state with depolarization probability $p$:
$$
\begin{equation}
\rho_j^{AB} = p \ket{\phi_{00}}\bra{\phi_{00}}_j^{AB} + \frac{1 - p}{4} \mathbb{I_4}
\end{equation}
$$

Initial state:
$$
\begin{equation} 
U       = \frac{1}{\sqrt{2}} \left(\ket{0} - i \ket{1}\right)\bra{0} + \frac{1}{\sqrt{2}} \left(\ket{1} - i \ket{0}\right)\bra{1} 
        = \begin{pmatrix}
             1 & -i \\
            -i &  1 \\
          \end{pmatrix}
\end{equation}
$$

Initial state:
$$
\begin{equation} 
\rho^{(0)} = \rho_1^{AB} \otimes \rho_2^{AB}
\end{equation}
$$

Applying $\left(U_1^A U_1^B\right) \otimes \left(U_1^A U_1^B\right)$ (noisy gates?):
$$
\begin{equation}
\rho^{(1)} = \left(U_1^A U_1^B \rho_1^{AB} {U_1^A}^\dagger {U_1^B}^\dagger\right) \otimes \left(U_2^A U_2^B \rho_2^{AB} {U_2^A}^\dagger {U_2^B}^\dagger\right)
\end{equation}
$$


Knowing that $U_A U_B^\dagger\ket{\phi_{00}} = \ket{\phi_{00}}$, we have that (in order: $\ket{1A,1B,2A,2B}$):
$$
\begin{equation*}
\begin{split}
\rho^{(1)} & = \rho_1^{AB} \otimes \rho_2^{AB} \\
           & = \left(p \ket{\phi_{00}}\bra{\phi_{00}}_1^{AB} + \frac{1 - p}{4} \mathbb{I_4}\right) 
                \otimes \left(p \ket{\phi_{00}}\bra{\phi_{00}}_2^{AB} + \frac{1 - p}{4} \mathbb{I_4}\right) \\
           & = p^2 \ket{\phi_{00}}\bra{\phi_{00}}_1^{AB} \otimes \ket{\phi_{00}}\bra{\phi_{00}}_2^{AB} + 
                \frac{p(1 - p)}{4} \ket{\phi_{00}}\bra{\phi_{00}}_1^{AB} \otimes \mathbb{I}_4 + 
                \frac{p(1 - p)}{4} \mathbb{I}_4 \otimes \ket{\phi_{00}}\bra{\phi_{00}}_2^{AB} + 
                \frac{(1 - p)^2}{16} \mathbb{I}_4 \otimes \mathbb{I}_4 \\

           & = \frac{p^2}{4} \left(\ket{00}\bra{00} + \ket{00}\bra{11} + \ket{11}\bra{00} + \ket{11}\bra{11}\right)_1^{AB} 
                \otimes \left(\ket{00}\bra{00} + \ket{00}\bra{11} + \ket{11}\bra{00} + \ket{11}\bra{11}\right)_2^{AB} \\
           & + \frac{p(1 - p)}{8} \left(\ket{00}\bra{00} + \ket{00}\bra{11} + \ket{11}\bra{00} + \ket{11}\bra{11}\right)_1^{AB} 
                \otimes \left(\ket{00}\bra{00} + \ket{01}\bra{01} + \ket{10}\bra{10} + \ket{11}\bra{11}\right)_2^{AB} \\
           & + \frac{p(1 - p)}{8} \left(\ket{00}\bra{00} + \ket{01}\bra{01} + \ket{10}\bra{10} + \ket{11}\bra{11}\right)_1^{AB} 
                \otimes \left(\ket{00}\bra{00} + \ket{00}\bra{11} + \ket{11}\bra{00} + \ket{11}\bra{11}\right)_2^{AB} \\
           & + \frac{(1 - p)^2}{16} \left(\ket{00}\bra{00} + \ket{01}\bra{01} + \ket{10}\bra{10} + \ket{11}\bra{11}\right)_1^{AB} 
                \otimes \left(\ket{00}\bra{00} + \ket{01}\bra{01} + \ket{10}\bra{10} + \ket{11}\bra{11}\right)_2^{AB} \\

           & = \frac{p^2}{4} \left(
                \ket{0000}\bra{0000} + \ket{0000}\bra{0011} + \ket{0011}\bra{0000} + \ket{0011}\bra{0011} + 
                \ket{0000}\bra{1100} + \ket{0000}\bra{1111} + \ket{0011}\bra{1100} + \ket{0011}\bra{1111} + 
                \ket{1100}\bra{0000} + \ket{1100}\bra{0011} + \ket{1111}\bra{0000} + \ket{1111}\bra{0011} + 
                \ket{1100}\bra{1100} + \ket{1100}\bra{1111} + \ket{1111}\bra{1100} + \ket{1111}\bra{1111}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + \ket{0001}\bra{0001} + \ket{0010}\bra{0010} + \ket{0011}\bra{0011} + 
                \ket{0000}\bra{1100} + \ket{0001}\bra{1101} + \ket{0010}\bra{1110} + \ket{0011}\bra{1111} + 
                \ket{1100}\bra{0000} + \ket{1101}\bra{0001} + \ket{1110}\bra{0010} + \ket{1111}\bra{0011} + 
                \ket{1100}\bra{1100} + \ket{1101}\bra{1101} + \ket{1110}\bra{1110} + \ket{1111}\bra{1111}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + \ket{0000}\bra{0011} + \ket{0011}\bra{0000} + \ket{0011}\bra{0011} + 
                \ket{0100}\bra{0100} + \ket{0100}\bra{0111} + \ket{0111}\bra{0100} + \ket{0111}\bra{0111} + 
                \ket{1000}\bra{1000} + \ket{1000}\bra{1011} + \ket{1011}\bra{1000} + \ket{1011}\bra{1011} + 
                \ket{1100}\bra{1100} + \ket{1100}\bra{1111} + \ket{1111}\bra{1100} + \ket{1111}\bra{1111}
                \right)_{12}^{AB} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{0000}\bra{0000} + \ket{0001}\bra{0001} + \ket{0010}\bra{0010} + \ket{0011}\bra{0011} + 
                \ket{0100}\bra{0100} + \ket{0101}\bra{0101} + \ket{0110}\bra{0110} + \ket{0111}\bra{0111} + 
                \ket{1000}\bra{1000} + \ket{1001}\bra{1001} + \ket{1010}\bra{1010} + \ket{1011}\bra{1011} + 
                \ket{1100}\bra{1100} + \ket{1101}\bra{1101} + \ket{1110}\bra{1110} + \ket{1111}\bra{1111}
                \right)_{12}^{AB} \\
\end{split}
\end{equation*}
$$


Applying $\text{CNOT}_{1A,2A}$ and $\text{CNOT}_{1B,2B}$ gates (in order: $\ket{1A,1B,2A,2B}$):
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = \frac{p^2}{4} \left(
                \ket{0000}\bra{0000} + \ket{0000}\bra{0011} + \ket{0011}\bra{0000} + \ket{0011}\bra{0011} + 
                \ket{0000}\bra{1111} + \ket{0000}\bra{1100} + \ket{0011}\bra{1111} + \ket{0011}\bra{1100} + 
                \ket{1111}\bra{0000} + \ket{1111}\bra{0011} + \ket{1100}\bra{0000} + \ket{1100}\bra{0011} + 
                \ket{1111}\bra{1111} + \ket{1111}\bra{1100} + \ket{1100}\bra{1111} + \ket{1100}\bra{1100}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + \ket{0001}\bra{0001} + \ket{0010}\bra{0010} + \ket{0011}\bra{0011} + 
                \ket{0000}\bra{1111} + \ket{0001}\bra{1110} + \ket{0010}\bra{1101} + \ket{0011}\bra{1100} + 
                \ket{1111}\bra{0000} + \ket{1110}\bra{0001} + \ket{1101}\bra{0010} + \ket{1100}\bra{0011} + 
                \ket{1111}\bra{1111} + \ket{1110}\bra{1110} + \ket{1101}\bra{1101} + \ket{1100}\bra{1100}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + \ket{0000}\bra{0011} + \ket{0011}\bra{0000} + \ket{0011}\bra{0011} + 
                \ket{0101}\bra{0101} + \ket{0101}\bra{0110} + \ket{0110}\bra{0101} + \ket{0110}\bra{0110} + 
                \ket{1010}\bra{1010} + \ket{1010}\bra{1001} + \ket{1001}\bra{1010} + \ket{1001}\bra{1001} + 
                \ket{1111}\bra{1111} + \ket{1111}\bra{1100} + \ket{1100}\bra{1111} + \ket{1100}\bra{1100}
                \right)_{12}^{AB} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{0000}\bra{0000} + \ket{0001}\bra{0001} + \ket{0010}\bra{0010} + \ket{0011}\bra{0011} + 
                \ket{0101}\bra{0101} + \ket{0100}\bra{0100} + \ket{0111}\bra{0111} + \ket{0110}\bra{0110} + 
                \ket{1010}\bra{1010} + \ket{1011}\bra{1011} + \ket{1000}\bra{1000} + \ket{1001}\bra{1001} + 
                \ket{1111}\bra{1111} + \ket{1110}\bra{1110} + \ket{1101}\bra{1101} + \ket{1100}\bra{1100}
                \right)_{12}^{AB} \\
\end{split}
\end{equation*}
$$



Measuring values $a$ and $b$ in qubits $2A$ and $2B$:

1. If $a = 0$ and $b = 0$:
$$
\begin{equation*}
\begin{split}
\mu\rho^{(3)} & = \frac{p^2}{4} \left(
                \ket{0000}\bra{0000} + 
                \ket{0000}\bra{1100} + 
                \ket{1100}\bra{0000} +  
                \ket{1100}\bra{1100}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + 
                \ket{1100}\bra{1100}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + 
                \ket{1100}\bra{1100}
                \right)_{12}^{AB} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{0000}\bra{0000} +  
                \ket{0100}\bra{0100} +  
                \ket{1000}\bra{1000} +  
                \ket{1100}\bra{1100}
                \right)_{12}^{AB} \\
\end{split}
\end{equation*}
\text{where } \mu = \frac{1 - p + p^2}{4}
$$


2. If $a = 0$ and $b = 1$:
$$
\begin{equation*}
\begin{split}
\rho^{(3)} & = \frac{p(1 - p)}{8} \left(
                \ket{0001}\bra{0001} + 
                \ket{1101}\bra{1101}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0101}\bra{0101} +  
                \ket{1001}\bra{1001}
                \right)_{12}^{AB} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{0001}\bra{0001} +  
                \ket{0101}\bra{0101} +  
                \ket{1001}\bra{1001} + 
                \ket{1101}\bra{1101}
                \right)_{12}^{AB} \\
\end{split}
\end{equation*}
$$


3. If $a = 1$ and $b = 0$:
$$
\begin{equation*}
\begin{split}
\rho^{(3)} & = \frac{p(1 - p)}{8} \left(
                \ket{0010}\bra{0010} + 
                \ket{1110}\bra{1110}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0110}\bra{0110} + 
                \ket{1010}\bra{1010} + 
                \right)_{12}^{AB} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{0010}\bra{0010} +  
                \ket{0110}\bra{0110} + 
                \ket{1010}\bra{1010} +  
                \ket{1110}\bra{1110}
                \right)_{12}^{AB} \\
\end{split}
\end{equation*}
$$


4. If $a = 1$ and $b = 1$:
$$
\begin{equation*}
\begin{split}
\rho^{(3)} & = \frac{p^2}{4} \left(
                \ket{0011}\bra{0011} + 
                \ket{0011}\bra{1111} +  
                \ket{1111}\bra{0011} +  
                \ket{1111}\bra{1111} + 
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0011}\bra{0011} + 
                \ket{1111}\bra{1111}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0011}\bra{0011} + 
                \ket{1111}\bra{1111}
                \right)_{12}^{AB} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{0011}\bra{0011} + 
                \ket{0111}\bra{0111} + 
                \ket{1011}\bra{1011} + 
                \ket{1111}\bra{1111} + 
                \right)_{12}^{AB} \\
\end{split}
\end{equation*}
$$




Tracing out qubits $2A$ and $2B$:

1. If $a = 0$ and $b = 0$:
$$
\begin{equation*}
\begin{split}
\rho^{(4)} & = \frac{p^2}{4} \left(
                \ket{00}\bra{00} + 
                \ket{00}\bra{11} + 
                \ket{11}\bra{00} + 
                \ket{11}\bra{11}
                \right) \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{00}\bra{00} + 
                \ket{11}\bra{11}
                \right) \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{00}\bra{00} + 
                \ket{11}\bra{11}
                \right) \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{00}\bra{00} + 
                \ket{01}\bra{01} + 
                \ket{10}\bra{10} + 
                \ket{11}\bra{11}
                \right) \\

           & = \frac{p^2}{2} \ket{\phi_{00}}\bra{\phi_{00}} \\
           & + \frac{p(1 - p)}{4} \left(\ket{00}\bra{00} + \ket{11}\bra{11}\right) \\
           & + \frac{(1 - p)^2}{16} \mathbb{I}_4
\end{split}
\end{equation*}
$$


2. If $a = 0$ and $b = 1$:
$$
\begin{equation*}
\begin{split}
\rho^{(4)} & = \frac{p(1 - p)}{8} \left(
                \ket{00}\bra{00} + 
                \ket{11}\bra{11}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{01}\bra{01} +  
                \ket{10}\bra{10}
                \right)_{12}^{AB} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{00}\bra{00} +  
                \ket{01}\bra{01} +  
                \ket{10}\bra{10} + 
                \ket{11}\bra{11}
                \right)_{12}^{AB} \\

           & = \frac{1}{4} \mathbb{I}_4
\end{split}
\end{equation*}
$$


3. If $a = 1$ and $b = 0$:
$$
\begin{equation*}
\begin{split}
\rho^{(4)} & = \frac{p(1 - p)}{8} \left(
                \ket{00}\bra{00} + 
                \ket{11}\bra{11}
                \right)_{12}^{AB} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{01}\bra{01} + 
                \ket{10}\bra{10} + 
                \right)_{12}^{AB} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{00}\bra{00} +  
                \ket{01}\bra{01} + 
                \ket{10}\bra{10} +  
                \ket{11}\bra{11}
                \right)_{12}^{AB} \\

           & = \frac{1}{4} \mathbb{I}_4
\end{split}
\end{equation*}
$$


4. If $a = 1$ and $b = 1$:
$$
\begin{equation*}
\begin{split}
\rho^{(4)} & = \frac{p^2}{4} \left(
                \ket{00}\bra{00} + 
                \ket{00}\bra{11} +  
                \ket{11}\bra{00} +  
                \ket{11}\bra{11} 
                \right) \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{00}\bra{00} + 
                \ket{11}\bra{11}
                \right) \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{00}\bra{00} + 
                \ket{11}\bra{11}
                \right) \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{00}\bra{00} + 
                \ket{01}\bra{01} + 
                \ket{10}\bra{10} + 
                \ket{11}\bra{11}
                \right) \\

           & = \frac{p^2}{2} \ket{\phi_{00}}\bra{\phi_{00}} \\
           & + \frac{p(1 - p)}{4} \left(\ket{\phi_{00}}\bra{\phi_{00}} + \ket{\phi_{01}}\bra{\phi_{01}}\right) \\
           & + \frac{(1 - p)^2}{16} \mathbb{I}_4
\end{split}
\end{equation*}
$$


Finally, we have that:

1. If $a = b$, the output state is:
$$
\begin{equation*}
\rho^{(\text{out})} = \frac{1}{\mu} \left(\frac{p^2}{2} \ket{\phi_{00}}\bra{\phi_{00}} 
                    + \frac{p(1 - p)}{4} \left(\ket{\phi_{00}}\bra{\phi_{00}} + \ket{\phi_{01}}\bra{\phi_{01}}\right) 
                    + \frac{(1 - p)^2}{16} \mathbb{I}_4\right)

\text{, where } \mu = \frac{p^2}{2} + \frac{p(1 - p)}{2} + \frac{(1 - p)^2}{4} = \frac{1 + p^2}{4}
\end{equation*}
$$


2. If $a \ne b$, the output state is:
$$
\begin{equation*}
\rho^{(\text{out})} = \frac{1}{4} \mathbb{I}_4
\end{equation*}
$$












<!-- Swapping qubits 1B and 2A in kets (in order: $\ket{1A,2A,1B,2B}$):
$$
\begin{equation*}
\begin{split}
\rho^{(1)} & = \frac{p^2}{4} \left(
                \ket{0000}\bra{0000} + \ket{0000}\bra{0101} + \ket{0101}\bra{0000} + \ket{0101}\bra{0101} + 
                \ket{0000}\bra{1010} + \ket{0000}\bra{1111} + \ket{0101}\bra{1010} + \ket{0101}\bra{1111} + 
                \ket{1010}\bra{0000} + \ket{1010}\bra{0101} + \ket{1111}\bra{0000} + \ket{1111}\bra{0101} + 
                \ket{1010}\bra{1010} + \ket{1010}\bra{1111} + \ket{1111}\bra{1010} + \ket{1111}\bra{1111}
                \right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + \ket{0001}\bra{0001} + \ket{0100}\bra{0100} + \ket{0101}\bra{0101} + 
                \ket{0000}\bra{1010} + \ket{0001}\bra{1011} + \ket{0100}\bra{1110} + \ket{0101}\bra{1111} + 
                \ket{1010}\bra{0000} + \ket{1011}\bra{0001} + \ket{1110}\bra{0100} + \ket{1111}\bra{0101} + 
                \ket{1010}\bra{1010} + \ket{1011}\bra{1011} + \ket{1110}\bra{1110} + \ket{1111}\bra{1111}
                \right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + \ket{0000}\bra{0101} + \ket{0101}\bra{0000} + \ket{0101}\bra{0101} + 
                \ket{0010}\bra{0010} + \ket{0010}\bra{0111} + \ket{0111}\bra{0010} + \ket{0111}\bra{0111} + 
                \ket{1000}\bra{1000} + \ket{1000}\bra{1101} + \ket{1101}\bra{1000} + \ket{1101}\bra{1101} + 
                \ket{1010}\bra{1010} + \ket{1010}\bra{1111} + \ket{1111}\bra{1010} + \ket{1111}\bra{1111}
                \right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{0000}\bra{0000} + \ket{0001}\bra{0001} + \ket{0100}\bra{0100} + \ket{0101}\bra{0101} + 
                \ket{0010}\bra{0010} + \ket{0011}\bra{0011} + \ket{0110}\bra{0110} + \ket{0111}\bra{0111} + 
                \ket{1000}\bra{1000} + \ket{1001}\bra{1001} + \ket{1100}\bra{1100} + \ket{1101}\bra{1101} + 
                \ket{1010}\bra{1010} + \ket{1011}\bra{1011} + \ket{1110}\bra{1110} + \ket{1111}\bra{1111}
                \right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$


Applying $\text{CNOT}_{1A,2A}$ and $\text{CNOT}_{1B,2B}$ gates (in order: $\ket{1A,2A,1B,2B}$):
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = \frac{p^2}{4} \left(
                \ket{0000}\bra{0000} + \ket{0000}\bra{0101} + \ket{0101}\bra{0000} + \ket{0101}\bra{0101} + 
                \ket{0000}\bra{1111} + \ket{0000}\bra{1010} + \ket{0101}\bra{1111} + \ket{0101}\bra{1010} + 
                \ket{1111}\bra{0000} + \ket{1111}\bra{0101} + \ket{1010}\bra{0000} + \ket{1010}\bra{0101} + 
                \ket{1111}\bra{1111} + \ket{1111}\bra{1010} + \ket{1010}\bra{1111} + \ket{1010}\bra{1010}
                \right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + \ket{0001}\bra{0001} + \ket{0100}\bra{0100} + \ket{0101}\bra{0101} + 
                \ket{0000}\bra{1111} + \ket{0001}\bra{1110} + \ket{0100}\bra{1011} + \ket{0101}\bra{1010} + 
                \ket{1111}\bra{0000} + \ket{1110}\bra{0001} + \ket{1011}\bra{0100} + \ket{1010}\bra{0101} + 
                \ket{1111}\bra{1111} + \ket{1110}\bra{1110} + \ket{1011}\bra{1011} + \ket{1010}\bra{1010}
                \right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{8} \left(
                \ket{0000}\bra{0000} + \ket{0000}\bra{0101} + \ket{0101}\bra{0000} + \ket{0101}\bra{0101} + 
                \ket{0011}\bra{0011} + \ket{0011}\bra{0110} + \ket{0110}\bra{0011} + \ket{0110}\bra{0110} + 
                \ket{1100}\bra{1100} + \ket{1100}\bra{1001} + \ket{1001}\bra{1100} + \ket{1001}\bra{1001} + 
                \ket{1111}\bra{1111} + \ket{1111}\bra{1010} + \ket{1010}\bra{1111} + \ket{1010}\bra{1010}
                \right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{16} \left(
                \ket{0000}\bra{0000} + \ket{0001}\bra{0001} + \ket{0100}\bra{0100} + \ket{0101}\bra{0101} + 
                \ket{0011}\bra{0011} + \ket{0010}\bra{0010} + \ket{0111}\bra{0111} + \ket{0110}\bra{0110} + 
                \ket{1100}\bra{1100} + \ket{1101}\bra{1101} + \ket{1000}\bra{1000} + \ket{1001}\bra{1001} + 
                \ket{1111}\bra{1111} + \ket{1110}\bra{1110} + \ket{1011}\bra{1011} + \ket{1010}\bra{1010}
                \right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$



Measuring values $a,b$ in qubits 2A and 2B (in order: $\ket{1A,2A,1B,2B}$):

1. If $a = 0$ and $b = 0$:
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = p^2 \left(\ket{0000}\bra{0000}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{0000}\bra{0000} + \ket{0100}\bra{0100}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{0000}\bra{0000} + \ket{1100}\bra{1100}\right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{4} \left(\ket{0000}\bra{0000} + \ket{0100}\bra{0100} + \ket{1100}\bra{1100} + \ket{1000}\bra{1000}\right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$

2. If $a = 0$ and $b = 1$:
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = p^2 \left(\ket{0101}\bra{0101}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{0001}\bra{0001} + \ket{0101}\bra{0101}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{0101}\bra{0101} + \ket{1001}\bra{1001}\right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{4} \left(\ket{0001}\bra{0001} + \ket{0101}\bra{0101} + \ket{1101}\bra{1101} + \ket{1001}\bra{1001}\right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$

3. If $a = 1$ and $b = 0$:
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = p^2 \left(\ket{1010}\bra{1010}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{1110}\bra{1110} + \ket{1010}\bra{1010}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{0110}\bra{0110} + \ket{1010}\bra{1010}\right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{4} \left(\ket{0010}\bra{0010} + \ket{0110}\bra{0110} + \ket{1110}\bra{1110} + \ket{1010}\bra{1010}\right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$

4. If $a = 1$ and $b = 1$:
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = p^2 \left(\ket{1111}\bra{1111}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{1111}\bra{1111} + \ket{1011}\bra{1011}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{0011}\bra{0011} + \ket{1111}\bra{1111}\right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{4} \left(\ket{0011}\bra{0011} + \ket{0111}\bra{0111} + \ket{1111}\bra{1111} + \ket{1011}\bra{1011}\right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$



Eliminating qubits 2A and 2B:

1. If $a = 0$ and $b = 0$:
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = p^2 \left(\ket{00}\bra{00}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{00}\bra{00} + \ket{01}\bra{01}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{00}\bra{00} + \ket{11}\bra{11}\right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{4} \left(\ket{00}\bra{00} + \ket{01}\bra{01} + \ket{11}\bra{11} + \ket{10}\bra{10}\right)_{AB}^{12} \\

           & = \frac{1}{4} \left((1 + p)^2\ket{00}\bra{00} + (1 - p^2)\ket{01}\bra{01} + (1 - p)^2\ket{10}\bra{10} + (1 - p^2)\ket{11}\bra{11}\right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$

2. If $a = 0$ and $b = 1$:
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = p^2 \left(\ket{01}\bra{01}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{00}\bra{00} + \ket{01}\bra{01}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{01}\bra{01} + \ket{10}\bra{10}\right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{4} \left(\ket{00}\bra{00} + \ket{01}\bra{01} + \ket{11}\bra{11} + \ket{10}\bra{10}\right)_{AB}^{12} \\

           & = \frac{1}{4} \left((1 - p^2)\ket{00}\bra{00} + (1 + p)^2\ket{01}\bra{01} + (1 - p^2)\ket{10}\bra{10} + (1 - p)^2\ket{11}\bra{11}\right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$

3. If $a = 1$ and $b = 0$:
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = p^2 \left(\ket{10}\bra{10}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{11}\bra{11} + \ket{10}\bra{10}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{01}\bra{01} + \ket{10}\bra{10}\right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{4} \left(\ket{00}\bra{00} + \ket{01}\bra{01} + \ket{11}\bra{11} + \ket{10}\bra{10}\right)_{AB}^{12} \\

           & = \frac{1}{4} \left((1 - p)^2\ket{00}\bra{00} + (1 - p^2)\ket{01}\bra{01} + (1 + p)^2\ket{10}\bra{10} + (1 - p^2)\ket{11}\bra{11}\right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$

4. If $a = 1$ and $b = 1$:
$$
\begin{equation*}
\begin{split}
\rho^{(2)} & = p^2 \left(\ket{11}\bra{11}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{11}\bra{11} + \ket{10}\bra{10}\right)_{AB}^{12} \\
           & + \frac{p(1 - p)}{2} \left(\ket{00}\bra{00} + \ket{11}\bra{11}\right)_{AB}^{12} \\
           & + \frac{(1 - p)^2}{4} \left(\ket{00}\bra{00} + \ket{01}\bra{01} + \ket{11}\bra{11} + \ket{10}\bra{10}\right)_{AB}^{12} \\

           & = \frac{1}{4} \left((1 - p^2)\ket{00}\bra{00} + (1 - p)^2\ket{01}\bra{01} + (1 - p^2)\ket{10}\bra{10} + (1 + p)^2\ket{11}\bra{11}\right)_{AB}^{12} \\
\end{split}
\end{equation*}
$$ -->