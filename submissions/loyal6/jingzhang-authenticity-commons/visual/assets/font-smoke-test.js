(function () {
  "use strict";

  var family = "JZAC Noto Sans SC";
  var critical = ["京张验真公地", "公众判据", "临时边界", "概念建议", "待授权实测"];

  function publish(passed, details) {
    var state = passed ? "pass" : "fail";
    document.documentElement.setAttribute("data-cjk-font-smoke", state);
    if (details && typeof details === "object") {
      document.documentElement.setAttribute("data-cjk-font-exact-face", details.exactFaceLoaded ? "true" : "false");
      document.documentElement.setAttribute("data-cjk-font-face-count", String(details.loadedFaceCount || 0));
      document.documentElement.setAttribute("data-cjk-critical-text", details.criticalTextPresent ? "true" : "false");
    }
    window.__JZAC_CJK_FONT_SMOKE__ = {
      passed: passed,
      family: family,
      criticalStrings: critical.slice(),
      details: details
    };
    var output = document.getElementById("cjk-font-smoke-status");
    if (output) {
      output.value = passed ? "通过 / PASS" : "失败 / FAIL";
      output.textContent = output.value;
    }
  }

  async function run() {
    if (!document.fonts || typeof document.fonts.load !== "function") {
      publish(false, "Font Loading API unavailable");
      return;
    }
    try {
      var probe = critical.join("｜");
      var loadedFaces = await document.fonts.load('700 20px "' + family + '"', probe);
      await document.fonts.ready;
      var exactFaceLoaded = Array.prototype.some.call(loadedFaces, function (face) {
        return String(face.family).replace(/["']/g, "") === family && face.status === "loaded";
      });
      var fontLoaded = exactFaceLoaded && document.fonts.check('700 20px "' + family + '"', probe);
      var bodyText = document.body ? document.body.innerText : "";
      var visibleTextPresent = critical.every(function (value) {
        return bodyText.indexOf(value) !== -1;
      });
      publish(fontLoaded && visibleTextPresent, {
        fontLoaded: fontLoaded,
        exactFaceLoaded: exactFaceLoaded,
        loadedFaceCount: loadedFaces.length,
        criticalTextPresent: visibleTextPresent
      });
    } catch (error) {
      publish(false, String(error && error.message ? error.message : error));
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run, { once: true });
  } else {
    run();
  }
})();
