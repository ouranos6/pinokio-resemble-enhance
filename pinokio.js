module.exports = {
  "version": "6.0.0",
  "title": "Resemble Enhance",
  "description": "AI-powered speech denoising + enhancement (Gradio web demo + CLI).",
  "icon": "icon.png",
  "menu": async (kernel, info) => {
    const installed = info.exists("app/env") && info.exists("app/app.py")

    const running = {
      install: info.running("install.json"),
      start: info.running("start.json"),
      update: info.running("update.json"),
      reset: info.running("reset.json"),
    }

    if (running.install) {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Installing",
        href: "install.json",
      }]
    } else if (installed) {
      if (running.start) {
        const local = info.local("start.json")
        if (local && local.url) {
          return [{
            default: true,
            icon: "fa-solid fa-rocket",
            text: "Open Web UI",
            href: local.url,
          }, {
            icon: "fa-solid fa-terminal",
            text: "Terminal",
            href: "start.json",
          }]
        }
        return [{
          default: true,
          icon: "fa-solid fa-terminal",
          text: "Terminal",
          href: "start.json",
        }]
      } else if (running.update) {
        return [{
          default: true,
          icon: "fa-solid fa-terminal",
          text: "Updating",
          href: "update.json",
        }]
      } else if (running.reset) {
        return [{
          default: true,
          icon: "fa-solid fa-terminal",
          text: "Resetting",
          href: "reset.json",
        }]
      }

      return [{
        default: true,
        icon: "fa-solid fa-power-off",
        text: "Start (web demo)",
        href: "start.json",
      }, {
        icon: "fa-solid fa-plug",
        text: "Update",
        href: "update.json",
      }, {
        icon: "fa-solid fa-plug",
        text: "Install",
        href: "install.json",
      }, {
        icon: "fa-regular fa-circle-xmark",
        text: "Reset",
        href: "reset.json",
        confirm: "Are you sure you wish to reset the app?"
      }]
    } else {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Install",
        href: "install.json"
      }]
    }
  }
}
