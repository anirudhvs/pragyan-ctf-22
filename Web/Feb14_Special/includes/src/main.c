#include <stdio.h>
#include <string.h>
#include <emscripten/emscripten.h>

#ifdef __cplusplus
extern "C"
{
#endif

    EMSCRIPTEN_KEEPALIVE
    int start(char a[])
    {
        if (a[0] == 'l')
        {
            int finalResult = EM_ASM_INT(
                {
                    var result = Module.ccall('__call01', 'int', ['string'], [UTF8ToString($0)]);
                    return result;
                },
                a);
            return finalResult;
        }
        return 0;
    }

    EMSCRIPTEN_KEEPALIVE
    int __call01(char b[])
    {
        int Result1 = EM_ASM_INT(
            {
                if (UTF8ToString($0)[1] == String.fromCharCode(parseInt('6F', 16)))
                {
                    var result = Module.ccall('__call02', 'int', ['string'], [UTF8ToString($0)]);
                    return result;
                }
                return 0;
            },
            b);
        return Result1;
    }

    EMSCRIPTEN_KEEPALIVE
    int __call02(char c[])
    {
        int Result2 = EM_ASM_INT(
            {
                if (UTF8ToString($0)[2].charCodeAt(0) == 118)
                {
                    var result = Module.ccall('__call03', 'int', ['string'], [UTF8ToString($0)]);
                    return result;
                }
                return 0;
            },
            c);
        return Result2;
    }

    EMSCRIPTEN_KEEPALIVE
    int __call03(char d[])
    {
        int Result3 = EM_ASM_INT(
            {
                if (UTF8ToString($0)[3] == (6^8).toString(16))
                {
                    var result = Module.ccall('__call04', 'int', ['string'], [UTF8ToString($0)]);
                    return result;
                }
                return 0;
            },
            d);
        return Result3;
    }

    EMSCRIPTEN_KEEPALIVE
    int __call04(char e[])
    {
        int Result4 = EM_ASM_INT(
            {
                if (btoa(UTF8ToString($0)[4]) == "dQ==")
                {
                    var result = Module.ccall('__call05', 'int', ['string'], [UTF8ToString($0)]);
                    return result;
                }
                return 0;
            },
            e);
        return Result4;
    }

    EMSCRIPTEN_KEEPALIVE
    int __call05(char f[])
    {
        char wasm[97] ={170,203,217,199,171,170,170,170,171,44,42,42,42,170,171,202,171,213,171,213,169,40,42,42,42,170,171,170,174,46,42,42,42,170,171,218,170,170,175,41,42,42,42,170,171,170,171,172,43,42,42,42,170,170,173,56,42,42,42,170,168,172,199,207,199,197,216,211,168,170,175,197,194,245,196,197,170,170,160,39,42,42,42,170,171,45,42,42,42,170,170,138,170,235,173,236,161,};
        for (int i = 0; i < 97; i++)
        {
            wasm[i] = (wasm[i] ^ 0xaa) & 0xff;
        }
        int Result5 = EM_ASM_INT(
            {
                var wasm_array = new Uint8Array($2);
                for (var i = 0; i < $2; i++)
                {
                    wasm_array[i] = getValue($1 + i);
                }
                var module = new WebAssembly.Module(wasm_array);
                var module_instance = new WebAssembly.Instance(module);
                var wasmResult = module_instance.exports.oh_no(6);
                if (parseInt(UTF8ToString($0)[5]) == wasmResult+3)
                {
                    var result = Module.ccall('__call06', 'int', ['string'], [UTF8ToString($0)]);
                    return result;
                }
                return 0;
            },
            f, wasm, 97);
        return Result5;
    }

    EMSCRIPTEN_KEEPALIVE
    int __call06(char g[])
    {
        int Result6 = EM_ASM_INT(
            {
                var wasm_array = new Uint8Array([ 0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x06, 0x01, 0x60, 0x01, 0x7f, 0x01, 0x7f, 0x03, 0x02, 0x01, 0x00, 0x07, 0x0a, 0x01, 0x06, 0x5f, 0x6f, 0x68, 0x5f, 0x6e, 0x6f, 0x00, 0x00, 0x0a, 0x09, 0x01, 0x07, 0x00, 0x20, 0x00, 0x41, 0x04, 0x46, 0x0b ]);
                var module = new WebAssembly.Module(wasm_array);
                var module_instance = new WebAssembly.Instance(module);
                var wasmResult = module_instance.exports._oh_no(7);
                if (parseInt(UTF8ToString($0)[6]) == wasmResult)
                {
                    var result = Module.ccall('__call07', 'int', ['string'], [UTF8ToString($0)]);
                    return result;
                }
                return 0;
            },
            g);
        return Result6;
    }

    EMSCRIPTEN_KEEPALIVE
    int __call07(char h[])
    {
        int Result7 = EM_ASM_INT(
            {
                var wasm = new Uint8Array([
                    0, 97, 115, 109, 1, 0, 0, 0, 1, 134, 128, 128, 128, 0, 1, 96, 1, 127, 1, 127, 3, 130,
                    128, 128, 128, 0, 1, 0, 4, 132, 128, 128, 128, 0, 1, 112, 0, 0, 5, 131, 128, 128,
                    128, 0, 1, 0, 1, 6, 129, 128, 128, 128, 0, 0, 7, 146, 128, 128, 128, 0, 2, 6, 109,
                    101, 109, 111, 114, 121, 2, 0, 5, 111, 104, 95, 110, 111, 0, 0, 10, 141, 128, 128,
                    128, 0, 1, 135, 128, 128, 128, 0, 0, 32, 0, 65, 9, 70, 11
                ]);

                var module = new WebAssembly.Module(wasm);
                var module_instance = new WebAssembly.Instance(module);
                var wasmResult = module_instance.exports.oh_no(8);
                if (parseInt(UTF8ToString($0)[7]) == wasmResult)
                {
                    var result = Module.ccall('__call08', 'int', ['string'], [UTF8ToString($0)]);
                    return result;
                }
                return 0;
            },
            h);
        return Result7;
    }

    EMSCRIPTEN_KEEPALIVE
    int __call08(char i[])
    {
        if (i[8] == '0')
        {
            emscripten_run_script("eval(atob('YWxlcnQoJ0NvbmdyYXRzLiBIZXJlIGlzIHlvdXIgZmxhZzogcF9jdGZ7dzNiX2EyMjNtYjF5X3cxbGxfYjNfdGgzX2Z1NHR1cjN9Jyk7'))");
            return 1;
        }
        return 0;
    }

#ifdef __cplusplus
}
#endif
