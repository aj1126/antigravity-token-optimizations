# Global Rules

## Worker Thread Management
- **Clean Exit**: Do not use `worker.terminate()` on clean paths. Post `{ action: "close" }` to worker to close port and exit cleanly.
- **Defer Forced Exit**: Wrap `worker.terminate()` in `setImmediate()` or `setTimeout()` inside its own event callbacks (`message`, `error`) to avoid re-entrancy segfaults (exit `0xC0000005`).
  ```javascript
  worker.on("message", (msg) => {
      if (isFinished) setImmediate(() => worker.terminate().then(resolve));
  });
  ```

## PDF.js / Ingestion Invariant Rules
- **Unified PDFParse Args**: Always pass document data buffer and options as a single options object:
  ```javascript
  const parser = new PDFParse({ data: wasmData, disableFontFace: false, standardFontDataUrl: standardFontsPath });
  ```
- **Font Paths**: `standardFontDataUrl` must use forward slashes (`/`) and end with trailing `/`. Convert backslashes using `.replace(/\\/g, '/')`.

## PowerShell Rule: Automatic Variable Constraints
- **Automatic Variables**: Do not assign values directly to PowerShell automatic variables (e.g., `$PSScriptRoot`, `$ErrorActionPreference`, `$args`).
- **Custom Local Variables**: Copy automatic variables to local variables (e.g., `$ScriptDir = $PSScriptRoot`) and reference them.
