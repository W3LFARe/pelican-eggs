# 🥚 W3LFARe's Auto-Updating Pelican & Pterodactyl Eggs

![Validate Pelican Eggs](https://github.com/W3LFARe/pelican-eggs/actions/workflows/validate-eggs.yml/badge.svg)

A collection of custom **Pelican Panel** (and Pterodactyl Panel) Eggs for Modded Minecraft servers, powered by W3LFARe's automated 6-hour upstream GitHub workflows.

Unlike standard static Eggs that require you to manually look up CurseForge file IDs or download URLs every time a modpack updates, these Eggs pull directly from W3LFARe's auto-updated repositories (`docker-allthemods10` and `docker-allthemods10-tts`) while running inside Pelican's native **`ghcr.io/pelican-eggs/yolks:java_21`** runtime image.

---

## 📦 Available Eggs

*(Right-click the **Download Egg JSON** link and select **Save Link As...** to download the Egg file for import)*

| Modpack | Egg JSON Download | Upstream Auto-Updater Repo | Required Java Yolk | Recommended RAM |
| :--- | :--- | :--- | :--- | :--- |
| **All the Mods 10 (ATM10)** | [**Download Egg JSON**](https://raw.githubusercontent.com/W3LFARe/pelican-eggs/main/allthemods10/egg-all-the-mods-10.json) | [`W3LFARe/docker-allthemods10`](https://github.com/W3LFARe/docker-allthemods10) | `ghcr.io/pelican-eggs/yolks:java_21` | 8 GB – 12 GB+ |
| **All the Mods 10: To The Sky (ATM10-TTS)** | [**Download Egg JSON**](https://raw.githubusercontent.com/W3LFARe/pelican-eggs/main/allthemods10-tts/egg-all-the-mods-10-tts.json) | [`W3LFARe/docker-allthemods10-tts`](https://github.com/W3LFARe/docker-allthemods10-tts) | `ghcr.io/pelican-eggs/yolks:java_21` | 6 GB – 10 GB+ |

---

## ✨ Key Features

* **🔄 Smart `AUTO_UPDATE` Toggle:** Choose between hands-off automatic updates on every server restart (`AUTO_UPDATE=1`) or locking your server to its current version (`AUTO_UPDATE=0`) until you and your players are ready to update.
* **⚡ Native Pelican Yolk Integration:** Runs on Pelican's official `yolks:java_21` image for accurate PID tracking, graceful stops, SFTP compatibility, and automatic `server.properties` port binding.
* **⏱️ 6-Hour Upstream Sync:** Our upstream GitHub Actions check CurseForge every 6 hours for new releases and automatically update the `launch.sh` installer script.
* **🛡️ GitHub Outage Protection:** Built-in fallback checks ensure that if GitHub is ever unreachable during a reboot, your server safely falls back to its existing local `launch.sh` script and boots normally.

---

## 🚀 How to Import & Create a Server

### 1. Import the Egg
1. Download the desired `.json` file from the table above.
2. Open your **Pelican Admin Panel** and navigate to **Eggs** -> **Import**.
3. Upload the `.json` file (if using Pterodactyl Panel, select your **Minecraft** Nest and click **Import Egg**).

### 2. Deploy the Server
1. Go to **Servers** -> **Create Server**.
2. Select either **All the Mods 10 (W3LFARe Auto-Updating)** or **All the Mods 10: To The Sky (W3LFARe Auto-Updating)**.
3. Allocate sufficient memory (at least **8192 MB** recommended) and match your `JVM_OPTS` variable to your container's RAM allocation.
4. Click **Create Server**. The installer will set up the environment, and the first boot will download and install the modpack and NeoForge automatically.

---

## ⚙️ Startup Variables & Configuration

All variables are configurable directly inside the server's **Startup** tab in Pelican/Pterodactyl:

| Variable Name | Environment Variable | Default Value | Description |
| :--- | :--- | :--- | :--- |
| **Auto Update on Reboot** | `AUTO_UPDATE` | `1` (Enabled) | When enabled (`1`/`true`), pulls the latest `launch.sh` from GitHub on every restart and upgrades the modpack in place if a new release is out. Disable (`0`/`false`) to lock your current version. |
| **JVM Arguments** | `JVM_OPTS` | `-Xms4096m -Xmx8192m` | Custom Java memory flags passed to `user_jvm_args.txt`. Adjust `-Xmx` to stay ~1–2 GB below your container's hard memory limit to prevent OOM kills. |
| **Server MOTD** | `MOTD` | `All the Mods 10 Server Powered by W3LFARe` | Message of the day displayed in the Minecraft multiplayer server list. |
| **World Name** | `LEVEL` | `world` | Name of the world save directory (`level-name` in `server.properties`). |
| **Minecraft Operators** | `OPS` | *(Blank)* | Comma-separated list of Minecraft usernames to automatically grant Operator (`op`) permissions on boot (e.g., `Player1,Player2`). |

---

## 🔄 How Updating Works

### Mode 1: Automatic Updates on Restart (`AUTO_UPDATE = 1`)
Leave **Auto Update on Reboot** enabled in the **Startup** tab. Whenever a new version of ATM10 or ATM10-TTS is detected by the upstream GitHub repo, simply **Restart** your server in the panel. The startup script will automatically pull the updated installer, replace the outdated `mods/` and `config/` folders while preserving your `world/` save and `server.properties`, and boot the upgraded server.

### Mode 2: Version-Locked / Manual Updates (`AUTO_UPDATE = 0`)
If you are playing with a group and don't want a scheduled nightly restart to upgrade the server before everyone updates their CurseForge client:
1. Set **Auto Update on Reboot** to `0` (`false`) in the **Startup** tab.
2. When a new modpack update drops and your players are ready:
   * Either temporarily flip **Auto Update on Reboot** back to `1` and restart the server, **OR**
   * Go to **Settings** -> **Reinstall Server** in Pelican Panel to pull the latest version without touching your world data.

---

## 🐳 Looking for Unraid or Standalone Docker Instead?

If you run **Unraid** or standalone **Docker Compose**, check out the upstream repositories and Unraid Community Applications templates:
* **Unraid Templates:** [`W3LFARe/unraid_templates`](https://github.com/W3LFARe/unraid_templates)
* **ATM10 Docker Image:** [`w3lfare/allthemods10` on Docker Hub](https://hub.docker.com/r/w3lfare/allthemods10)
* **ATM10: To The Sky Docker Image:** [`w3lfare/allthemods10-tts` on Docker Hub](https://hub.docker.com/r/w3lfare/allthemods10-tts)
