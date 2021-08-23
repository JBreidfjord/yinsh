## YINSH
A Python implementation of the abstract strategy game YINSH.
Rules for the game can be found [here](https://s3.amazonaws.com/geekdo-files.com/bgg181418?response-content-disposition=inline%3B%20filename%3D%22huc_15_6101_GIPF_Project_YINSH_Auflage_A_2016_AL_sc.pdf%22&response-content-type=application%2Fpdf&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJYFNCT7FKCE4O6TA%2F20210823%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210823T050747Z&X-Amz-SignedHeaders=host&X-Amz-Expires=120&X-Amz-Signature=ebe40149a280b30cb406ac48c4da610c226b764c115602c189f80b4454df18e9).

Currently the game can be played in a rough way via the command line by running play_yinsh.py. This will pit you against a fully randomized opponent.

The game itself is fully written using only the standard library so the only requirement is an up-to-date version of Python.

## To-do
- [x] Core functionality written in Python
- [x] Tests for core functionality
- [ ] Web interface written in JavaScript, with API calls to a Python FastAPI server
- [ ] Websockets to enable online competitive play
- [ ] Refactor core to Rust
- [ ] Smarter AI using MCTS
- [ ] Refactor web interface to use Rust through WebAssembly
