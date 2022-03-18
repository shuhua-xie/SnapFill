# SnapFill
CSE291 WI22 group project

SnapFill is a PBE tool that re-implements the core features of BlinkFill in Python and extends it towards conditionals. While not typically used for synthesis, Python as the language of choice allows us to achieve a better understanding of the algorithm. Given the goal of synthesizing with relatively few examples, using Python does not pose a performance issue. Furthermore, since SnapFill is not integrated with any spreadsheet like tool, the programs must be exported somehow in order for the synthesized scripts to be useful. We have chosen to output python programs that can process csv files, which we believe is reasonably suited for nearly any application of this tool.

### Demo
Just run `demo.sh` and hit enter when necessary. Files will be generated under `demo/` and two scripts will be generated in the base folder.

### Benchmark Edits:
- Benchmarks taken from SyGuS 2019 PBE String track
- Removed files with constraints with multiple inputs as given by grep: 
  - `grep -Lr 'constraint (= (f "[^"]*") "[^"]*")' *.sl | xargs -L1 rm`

