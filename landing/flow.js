// Peragaan alur: ganti adegan tiap 5 detik, berhenti saat disorot/difokus, tidak berputar bila pengguna memilih gerak minimal.
(function () {
  var root = document.querySelector("[data-flow]");
  if (!root) return;
  var tabs = root.querySelectorAll("[role=tab]"), scenes = root.querySelectorAll(".scene");
  var dur = 5000, i = 0, timer = null, paused = false;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  root.style.setProperty("--dur", dur + "ms");
  function show(n) {
    i = n;
    tabs.forEach(function (t, k) { t.setAttribute("aria-selected", k === n ? "true" : "false"); });
    scenes.forEach(function (s, k) {
      s.classList.remove("on");
      s.setAttribute("aria-hidden", k === n ? "false" : "true");
      if (k === n) { void s.offsetWidth; s.classList.add("on"); }  // reflow agar animasi adegan diulang
    });
    schedule();
  }
  function schedule() {
    clearTimeout(timer);
    if (!paused && !still) timer = setTimeout(function () { show((i + 1) % scenes.length); }, dur);
  }
  function pause(p) { paused = p; root.classList.toggle("paused", p || still); schedule(); }
  tabs.forEach(function (t, k) { t.addEventListener("click", function () { show(k); }); });
  root.addEventListener("mouseenter", function () { pause(true); });
  root.addEventListener("mouseleave", function () { pause(false); });
  root.addEventListener("focusin", function () { pause(true); });
  root.addEventListener("focusout", function () { pause(false); });
  root.classList.toggle("paused", still);
  show(0);
})();
