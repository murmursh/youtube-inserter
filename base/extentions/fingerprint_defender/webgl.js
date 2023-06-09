

var inject = function () {
    const UNMASKED_VENDOR_WEBGL = 0x9245;
    const VENDOR = 0x1F00;
    const MAX_VARYING_VECTORS = 0x8DFC;
    const DEPTH_BITS = 0x0D56;
    const STENCIL_BITS = 0x0D57;
    const RENDERER = 7937;
    const MAX_TEXTURE_SIZE = 3379;
    const MAX_VERTEX_UNIFORM_VECTORS = 36347;
    const MAX_CUBE_MAP_TEXTURE_SIZE = 34076;
    const MAX_RENDERBUFFER_SIZE = 34024;
    const MAX_VIEWPORT_DIMS = 3386;
    const ALPHA_BITS = 3413;
    const BLUE_BITS = 3412;
    const GREEN_BITS = 3411;
    const RED_BITS = 3410;
    const MAX_TEXTURE_MAX_ANISOTROPY_EXT = 34047;
    const MAX_TEXTURE_IMAGE_UNITS = 34930;
    const MAX_VERTEX_ATTRIBS = 34921;
    const MAX_VERTEX_TEXTURE_IMAGE_UNITS = 35660;
    const MAX_COMBINED_TEXTURE_IMAGE_UNITS = 35661;
    const MAX_FRAGMENT_UNIFORM_VECTORS = 36349;
    const ALIASED_LINE_WIDTH_RANGE = 33902;
    const ALIASED_POINT_SIZE_RANGE = 33901;
    const UNMASKED_RENDERER_WEBGL = 37446;
    const VERSION = 7938;
    const SHADING_LANGUAGE_VERSION = 35724;
        var config = {
        "random": {
            "value": function (key = false) {
                let rand;
                if (key) {
                    let get = localStorage.getItem("webgl_rv_" + key);
                    rand = get ? get : Math.random();
                    if (!get)
                        localStorage.setItem("webgl_rv_" + key, rand);
                } else {
                    rand = Math.random();
                }
                return rand;
            },
            "item": function (key, e) {
                let get = localStorage.getItem("webgl_" + key);
                let rand = get ? get : e.length * config.random.value();
                if (!get)
                    localStorage.setItem("webgl_" + key, rand);
                return e[Math.floor(rand)];
            },
            "number": function (key, power) {
                var tmp = [];
                for (var i = 0; i < power.length; i++) {
                    tmp.push(Math.pow(2, power[i]));
                }
                /*  */
                return config.random.item(key, tmp);
            },
            "int": function (key, power) {
                var tmp = [];
                for (var i = 0; i < power.length; i++) {
                    var n = Math.pow(2, power[i]);
                    tmp.push(new Int32Array([n, n]));
                }
                /*  */
                return config.random.item(key, tmp);
            },
            "float": function (key, power) {
                var tmp = [];
                for (var i = 0; i < power.length; i++) {
                    var n = Math.pow(2, power[i]);
                    tmp.push(new Float32Array([1, n]));
                }
                /*  */
                return config.random.item(key, tmp);
            }
        },
        "spoof": {
            "webgl": {
                "buffer": function (target) {
                    var proto = target.prototype ? target.prototype : target.__proto__;
                    const bufferData = proto.bufferData;
                    Object.defineProperty(proto, "bufferData", {
                        "value": function () {
                            var index = Math.floor(config.random.value('bufferDataIndex') * arguments[1].length);
                            var noise = arguments[1][index] !== undefined ? 0.1 * config.random.value('bufferDataNoise') * arguments[1][index] : 0;
                            //
                            arguments[1][index] = arguments[1][index] + noise;
                            window.top.postMessage("webgl-fingerprint-defender-alert", '*');
                            //
                            return bufferData.apply(this, arguments);
                        }
                    });
                },
                "parameter": function (target) {
                    var proto = target.prototype ? target.prototype : target.__proto__;
                    const getParameter = proto.getParameter;
                    Object.defineProperty(proto, "getParameter", {
                        "value": function () {
                            console.log(arguments);

                            if (arguments[0] === STENCIL_BITS) return 0;
                            else if (arguments[0] === DEPTH_BITS) return 24;
                            else if (arguments[0] === MAX_VARYING_VECTORS) return 30;
                            else if (arguments[0] === VENDOR) return "NVIDIA Corporation"; //
                            else if (arguments[0] === UNMASKED_VENDOR_WEBGL) return "Google Inc. (NVIDIA)"; //
                            else if (arguments[0] === RENDERER) return "NVIDIA GeForce";//
                            else if (arguments[0] === MAX_TEXTURE_SIZE) return config.random.number('3379', [14, 15]);
                            else if (arguments[0] === MAX_VERTEX_UNIFORM_VECTORS) return config.random.number('36347', [12, 13]);
                            else if (arguments[0] === MAX_CUBE_MAP_TEXTURE_SIZE) return config.random.number('34076', [14, 15]);
                            else if (arguments[0] === MAX_RENDERBUFFER_SIZE) return config.random.number('34024', [14, 15]);
                            else if (arguments[0] === MAX_VIEWPORT_DIMS) return config.random.int('3386', [13, 14, 15]);
                            else if (arguments[0] === ALPHA_BITS) return config.random.number('3413', [1, 2, 3, 4]);
                            else if (arguments[0] === BLUE_BITS) return config.random.number('3412', [1, 2, 3, 4]);
                            else if (arguments[0] === GREEN_BITS) return config.random.number('3411', [1, 2, 3, 4]);
                            else if (arguments[0] === RED_BITS) return config.random.number('3410', [1, 2, 3, 4]);
                            else if (arguments[0] === MAX_TEXTURE_MAX_ANISOTROPY_EXT) return config.random.number('34047', [1, 2, 3, 4]);
                            else if (arguments[0] === MAX_TEXTURE_IMAGE_UNITS) return config.random.number('34930', [1, 2, 3, 4]);
                            else if (arguments[0] === MAX_VERTEX_ATTRIBS) return config.random.number('34921', [1, 2, 3, 4]);
                            else if (arguments[0] === MAX_VERTEX_TEXTURE_IMAGE_UNITS) return config.random.number('35660', [1, 2, 3, 4]);
                            else if (arguments[0] === MAX_COMBINED_TEXTURE_IMAGE_UNITS) return config.random.number('35661', [4, 5, 6, 7, 8]);
                            else if (arguments[0] === MAX_FRAGMENT_UNIFORM_VECTORS) return config.random.number('36349', [10, 11, 12, 13]);
                            else if (arguments[0] === ALIASED_LINE_WIDTH_RANGE) return config.random.float('33902', [0, 10, 11, 12, 13]);
                            else if (arguments[0] === ALIASED_POINT_SIZE_RANGE) return config.random.float('33901', [0, 10, 11, 12, 13]);
                            else if (arguments[0] === UNMASKED_RENDERER_WEBGL) return config.random.item('37446', ["ANGLE (NVIDIA GeForce GTX 980 Ti Direct3D11 vs_5_0 ps_5_0)"]);//
                            else if (arguments[0] === VERSION) return config.random.item('7938', ["WebGL 1.0 (OpenGL ES 3.0)"]);//
                            else if (arguments[0] === SHADING_LANGUAGE_VERSION) return config.random.item('35724', ["WebGL GLSL ES 1.0"]);//
                            return getParameter.apply(this, arguments);
                        }
                    });
                }
            }
        }
    };
    //
    config.spoof.webgl.buffer(WebGLRenderingContext);
    config.spoof.webgl.buffer(WebGL2RenderingContext);
    config.spoof.webgl.parameter(WebGLRenderingContext);
    config.spoof.webgl.parameter(WebGL2RenderingContext);
    //
    document.documentElement.dataset.wgscriptallow = true;
};

var script_1 = document.createElement("script");
script_1.textContent = "(" + inject + ")()";
document.documentElement.appendChild(script_1);
script_1.remove();

if (document.documentElement.dataset.wgscriptallow !== "true") {
    var script_2 = document.createElement("script");
    script_2.textContent = `{
    const iframes = [...window.top.document.querySelectorAll("iframe[sandbox]")];
    for (var i = 0; i < iframes.length; i++) {
      if (iframes[i].contentWindow) {
        if (iframes[i].contentWindow.WebGLRenderingContext) {
          iframes[i].contentWindow.WebGLRenderingContext.prototype.bufferData = WebGLRenderingContext.prototype.bufferData;
          iframes[i].contentWindow.WebGLRenderingContext.prototype.getParameter = WebGLRenderingContext.prototype.getParameter;
        }
        if (iframes[i].contentWindow.WebGL2RenderingContext) {
          iframes[i].contentWindow.WebGL2RenderingContext.prototype.bufferData = WebGL2RenderingContext.prototype.bufferData;
          iframes[i].contentWindow.WebGL2RenderingContext.prototype.getParameter = WebGL2RenderingContext.prototype.getParameter;
        }
      }
    }
  }`;
    //
    window.top.document.documentElement.appendChild(script_2);
    script_2.remove();
}


