"""Parche Windows para motion-doctrine/scripts/seam-gate.mjs (HeyGen, Apache-2.0).

1. process.kill(-pid) no mata el árbol de procesos en Windows -> el servidor de preview y Chrome quedaban
   huérfanos tras cada verificación. Se sustituye por `taskkill /T /F`.
2. Busca el Chrome que descarga `hyperframes browser ensure` en ~/.cache/hyperframes (Windows).

Idempotente: si ya está parcheado, no hace nada. Uso: python3 seam-gate-windows.py <ruta/seam-gate.mjs>
"""
import sys

p = sys.argv[1]
s = open(p, encoding="utf-8").read()
if "[VdL]" in s:
    print("seam-gate.mjs ya parcheado")
    sys.exit(0)


def rep(a, b):
    global s
    if s.count(a) != 1:
        sys.exit(f"ERROR: no encuentro (o hay varios) {a[:60]!r} — ¿cambió seam-gate.mjs upstream?")
    s = s.replace(a, b)


rep('import { spawn } from "node:child_process";', 'import { spawn, spawnSync } from "node:child_process";')
rep("const cleanup = [];", """const cleanup = [];
// [VdL] Windows: process.kill(-pid) no mata el árbol de procesos -> taskkill /T /F.
function killTree(pid, sig) {
  if (process.platform === "win32") {
    try { spawnSync("taskkill", ["/pid", String(pid), "/T", "/F"], { stdio: "ignore" }); } catch {}
    return;
  }
  process.kill(-pid, sig);
}""")
rep('process.kill(-child.pid, "SIGTERM");', 'killTree(child.pid, "SIGTERM");')
rep('process.kill(-child.pid, "SIGKILL");', 'killTree(child.pid, "SIGKILL");')
rep('  if (process.env.CHROME_PATH) return { bin: process.env.CHROME_PATH, headlessFlag: true };',
    '''  if (process.env.CHROME_PATH) return { bin: process.env.CHROME_PATH, headlessFlag: true };
  // [VdL] Windows: el Chrome que descarga `hyperframes browser ensure`.
  const hfCache = join(homedir(), ".cache", "hyperframes", "chrome", "chrome-headless-shell");
  if (process.platform === "win32" && existsSync(hfCache)) {
    for (const v of readdirSync(hfCache).sort().reverse()) {
      const bin = join(hfCache, v, "chrome-headless-shell-win64", "chrome-headless-shell.exe");
      if (existsSync(bin)) return { bin, headlessFlag: false };
    }
  }''')
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("seam-gate.mjs parcheado para Windows")
