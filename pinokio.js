module.exports = {
  "version": "2.0",
  "title": "Resemble Enhance",
  "description": "AI-powered speech denoising + enhancement (Gradio web demo + CLI).",
  "icon": "icon.png",
  "menu": async (kernel, info) => {
    // Consider installed if repo + venv exist.
    const installed = info.exists("app/resemble-enhance/README.md") && info.exists("app/env")

    // If start.json is running, Pinokio can surface the live URL from the terminal output.
    const local = info.local("start.json") || {}
    const url = local.url || "http://127.0.0.1:7860"

    if (installed) {
      return [{
        default: true,
        text: "start (web demo)",
        href: "start.json"
      }, {
        text: "open web UI",
        href: url
      }, {
        text: "update",
        href: "update.json"
      }, {
        text: "reset (delete env + repo)",
        href: "reset.json"
      }]
    }

    return [{
      default: true,
      text: "install",
      href: "install.json"
    }, {
      text: "start (web demo)",
      href: "start.json"
    }]
  }
}
