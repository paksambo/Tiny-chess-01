# Tiny-chess-01
Chess engine entry for the make.fun tiny-chess-01 bounty.

## How it works :
1. main.py is the complete engine, a single file under 4096 bytes.
2. It reads a FEN position from stdin and prints the chosen move in UCI format (for example e2e4) to stdout.
3. Search: minimax with alpha-beta pruning.
4. Evaluation: material values with a small positional term.

## Run
echo "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" | python3 main.py

## License
MIT, see LICENSE.
