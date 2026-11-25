import re

with open('/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/presentation.tex') as f:
    text = f.read()

# Replace Shillong with Sohra
text = text.replace('Shillong, India', 'Sohra, India')

# Replace Slide 12 with compact version
old_pattern = r'\\begin\{frame\}\{Experimental Results \(Held-Out Test Set\)\}.*?\\end\{frame\}'
new_slide = r'''\begin{frame}{Experimental Results (Held-Out Test Set)}
  \begin{center}
  \renewcommand{\arraystretch}{1.15}
  \scriptsize
  \begin{tabular}{|l|c|c|c|c|}
    \hline
    \textbf{Method / Architecture} & \textbf{Parent A} & \textbf{Parent B} & \textbf{Full Lineage} & \textbf{Latency} \\ \hline \hline
    Global SSCD Baseline & 100.00\% & 51.11\% & 51.11\% & \textbf{193 ms} \\ \hline
    Uniform Local (Rigid $2\times2, 3\times3$) & 100.00\% & 53.33\% & 53.33\% & 2277 ms \\ \hline
    \textbf{Uniform Local (Dynamic Overlap)} & 100.00\% & \textbf{75.56\%} & \textbf{75.56\%} & 2117 ms \\ \hline
    SSCD + MLP Gate (Rigid) & 100.00\% & 82.22\% & 82.22\% & 2265 ms \\ \hline
    \rowcolor{green!15}
    \textbf{SSCD + MLP Gate (Dynamic) [Ours]} & \textbf{100.00\%} & \textbf{88.89\%} & \textbf{88.89\%} & 2125 ms \\ \hline
  \end{tabular}
  \end{center}
  \vspace{-0.1cm}
  \begin{block}{Key Takeaways}
    \scriptsize
    \begin{itemize}
      \item \textbf{Global baseline misses half the donors:} Achieves only $51.11\%$ full lineage.
      \item \textbf{Dynamic slicing gives an instant $+22.23\%$ leap:} Proves boundary crossing was the main reason rigid grids failed.
      \item \textbf{Proposed system achieves $88.89\%$:} Near 9 out of 10 composites have both source parents retrieved in top 5!
    \end{itemize}
  \end{block}
\end{frame}'''

text = re.sub(old_pattern, new_slide, text, flags=re.DOTALL)

with open('/Users/viveknegi/.gemini/antigravity/scratch/multi_source_provenance/presentation.tex', 'w') as f:
    f.write(text)

print("Updated successfully!")
