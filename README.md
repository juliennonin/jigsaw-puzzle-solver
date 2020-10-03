# Solver for jigsaw puzzles

Solver for jigsaw puzzle based on Pomeranz et al. [1].

## Contribution
Contributors:
* [Rony Abecidan](https://github.com/RonyAbecidan/)
* [Maxence Giraud](https://github.com/MaxenceGiraud/)
* [Zhengyang Lan](https://github.com/LANZhengyang)
* [Julien Nonin](https://github.com/JulienNonin)

See also [commit naming conventions](docs/CONTRIBUTING.md)

## Requirements

To install the requirements, do the following command :

```python
pip install -r requirements.txt
```

## How to use

```python
import jigsolver
import matplotlib.pyplot as plt
img = plt.imread("img/eiffel.jpg")

# Create the Puzzle
puzzle = jigsolver.Puzzle(patch_size=100) 
puzzle.create_from_img(img) 

# Display the completed Puzzle
puzzle.display() 

# Shuffle the pieces
puzzle.shuffle()

# Solve the Puzzle (randomly for now)
jigsolver.random_solver(puzzle,plotsteps=False)
puzzle.display()
```

Further examples can be found in the notebook "sandbox.ipynb"

## Todo 
- [x] Implement Puzzle
- [x] Add the Compatibility matrix
- [x] Implement Placer 
- [x] Implement Segmenter
- [ ] Implement Shifter


## References 

[1]: Pomeranz, D., Shemesh, M., & Ben-Shahar, O. (2011, June). A fully automated greedy square jigsaw puzzle solver. In CVPR 2011 (pp. 9-16). IEEE.