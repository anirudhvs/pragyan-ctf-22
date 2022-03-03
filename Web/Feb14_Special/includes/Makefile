build:
	mkdir ./build
	emcc ./src/main.c -O3 -s WASM=1 -o ./build/index.html --shell-file ./src/chall_template.html -s NO_EXIT_RUNTIME=1 -s LINKABLE=1 -s EXTRA_EXPORTED_RUNTIME_METHODS='["ccall"]'
clean:
	rm -rf ./build/