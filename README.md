# 🥚 W3LFARe's Auto-Updating Pelican & Pterodactyl Eggs

![Validate Pelican Eggs](https://github.com/W3LFARe/pelican-eggs/actions/workflows/validate-eggs.yml/badge.svg)

A collection of custom **Pelican Panel** (and Pterodactyl Panel) Eggs for Modded Minecraft servers, powered by W3LFARe's automated 6-hour upstream GitHub workflows.

Unlike standard static Eggs that require you to manually look up CurseForge file IDs or download URLs every time a modpack updates, these Eggs pull directly from W3LFARe's auto-updated repositories (`docker-allthemods10` and `docker-allthemods10-tts`) while running inside Pelican's native **`ghcr.io/pelican-eggs/yolks:java_21`** runtime image.

---

## 📦 Available Eggs

*(Right-click **Download Egg JSON** and select **Save Link As...** to download the Egg file for import)*

| Icon | Modpack | Egg JSON Download | Icon URL (For Pelican UI) | Upstream Auto-Updater Repo | Recommended RAM |
| :---: | :--- | :--- | :--- | :--- | :--- |
| <img src="https://raw.githubusercontent.com/W3LFARe/pelican-eggs/main/allthemods10/icon.png" width="48" alt="ATM10"> | **All the Mods 10 (ATM10)** | [**Download Egg JSON**](https://raw.githubusercontent.com/W3LFARe/pelican-eggs/main/allthemods10/egg-all-the-mods-10.json) | [`icon.png`](https://raw.githubusercontent.com/W3LFARe/pelican-eggs/main/allthemods10/icon.png) | [`W3LFARe/docker-allthemods10`](https://github.com/W3LFARe/docker-allthemods10) | 8 GB – 12 GB+ |
| <img src="https://raw.githubusercontent.com/W3LFARe/pelican-eggs/main/allthemods10-tts/icon.png" width="48" alt="ATM10-TTS"> | **All the Mods 10: To The Sky** | [**Download Egg JSON**](https://raw.githubusercontent.com/W3LFARe/pelican-eggs/main/allthemods10-tts/egg-all-the-mods-10-tts.json) | [`icon.png`](https://raw.githubusercontent.com/W3LFARe/pelican-eggs/main/allthemods10-tts/icon.png) | [`W3LFARe/docker-allthemods10-tts`](https://github.com/W3LFARe/docker-allthemods10-tts) | 6 GB – 10 GB+ |

---

## ✨ Key Features

* **🔄 Smart `AUTO_UPDATE` Toggle:** Choose between hands-off automatic updates on every server restart (`AUTO_UPDATE=1`) or locking your server to its current version (`AUTO_UPDATE=0`) until you and your players are ready to update.
* **✅ Tested Releases Only:** Auto-update follows the newest upstream **GitHub Release**, which is only published after the upstream CI boot-tests the server — a broken commit on `main` never reaches your server. (Advanced: pin a version or follow `main` with the *Upstream Version* variable.)
* **🧩 Persistent `custom_mods/` & `custom_config/` Folders:** Drop extra server-side `.jar` mods into `custom_mods/` and custom configuration files (such as `Discord-Integration.toml`) into `custom_config/` so they automatically survive modpack upgrades.
* **📜 You Accept the EULA:** The Egg never accepts the Minecraft EULA for you — Pelican's built-in EULA prompt appears on first start and writes `eula.txt` when you agree.
* **🧠 Automatic Heap Sizing:** Leave `JVM_OPTS` blank and the Java heap is sized from the memory allocated to the server, so it can't exceed the container limit.
* **⚡ Native Pelican Yolk Integration:** Runs on Pelican's official `yolks:java_21` image for accurate PID tracking, graceful stops, SFTP compatibility, and automatic `SERVER_PORT` binding.
* **⏱️ 6-Hour Upstream Sync:** Our upstream GitHub Actions check CurseForge every 6 hours for new releases and automatically update `pack.env` and `launch.sh`.
* **🛡️ GitHub Outage Protection:** Downloads are all-or-nothing (`pack.env` + `launch.sh` together, HTTP errors are never saved as files). If GitHub is unreachable during a reboot, your server keeps its existing files and boots normally.

---

## 🚀 How to Import & Create a Server

### 1. Import the Egg
1. Download the desired `.json` file from the table above.
2. Open your **Pelican Admin Panel** and navigate to **Eggs** -> **Import**.
3. Upload the `.json` file (if using Pterodactyl Panel, select your **Minecraft** Nest and click **Import Egg**).

### 2. Deploy the Server
1. Go to **Servers** -> **Create Server**.
2. Select either **All the Mods 10 (W3LFARe Auto-Updating)** or **All the Mods 10: To The Sky (W3LFARe Auto-Updating)**.
3. Allocate sufficient memory (at least **8192 MB** recommended). Leave `JVM_OPTS` blank to size the Java heap automatically.
4. Click **Create Server**. The installer will set up the environment.
5. Start the server. When Pelican shows the **Minecraft EULA** prompt, read and accept it; the modpack and NeoForge then download and install automatically on the first boot.
6. `ENABLE_WHITELIST` defaults to `true`: add your usernames to **Whitelist Users** (and **OP Users**) before joining, or set it to `false`.

---

## ⚙️ Startup Variables & Configuration

All variables are configurable directly inside the server's **Startup** tab in Pelican/Pterodactyl:

| Variable Name | Environment Variable | Default Value | Description |
| :--- | :--- | :--- | :--- |
| **Auto Update on Reboot** | `AUTO_UPDATE` | `1` (Enabled) | `1`/`true`: on every start, switch to the newest **tested release** of the upstream repo and upgrade the modpack in place if a new version is out. `0`/`false`: stay on the installed version. |
| **JVM Arguments** | `JVM_OPTS` | *(Blank = automatic)* | Leave blank to size the Java heap from the memory allocated to the server (`Xmx` = allocation minus the larger of 1 GB / 15%, `Xms` = half of that). Set it yourself to override; keep `-Xmx` 1–2 GB below your allocation. For reference, the Unraid defaults are `-Xms8192m -Xmx12288m` (ATM10) and `-Xms6144m -Xmx8192m` (ATM10-TTS). |
| **Server MOTD** | `MOTD` | `All the Mods 10 Server Powered by W3LFARe` (ATM10)<br>`ATM10 To the Sky Server Powered by W3LFARe` (ATM10-TTS) | Message of the day displayed in the Minecraft multiplayer server list. |
| **Allow Flight** | `ALLOW_FLIGHT` | `true` | Whether players are allowed to fly in Survival mode (`true` or `false`). |
| **Max Players** | `MAX_PLAYERS` | `5` | Maximum number of players allowed on the server at once. |
| **Online Mode** | `ONLINE_MODE` | `true` | Verify player accounts against Mojang authentication servers (`true` or `false`). |
| **Enable Whitelist** | `ENABLE_WHITELIST` | `true` | Enable (`true`) / Disable (`false`) the whitelist. Same default as the Unraid template, so **add players to `WHITELIST_USERS`** (or set this to `false`) or nobody can join. |
| **Whitelist Users** | `WHITELIST_USERS` | *(Blank)* | Comma-separated list of Minecraft usernames to add to the whitelist on boot (e.g., `TestUserName1, TestUserName2`). |
| **OP Users** | `OP_USERS` | *(Blank)* | Comma-separated list of Minecraft usernames to automatically grant Operator (`op`) permissions on boot (e.g., `TestUserName1, TestUserName2`). |
| **Upstream Version (advanced)** | `UPSTREAM_REF` | *(Blank)* | Blank = newest tested GitHub Release. Set a tag (e.g. `v8.3`) to pin a version, or `main` to follow the untested development branch. |

---

## 🧩 Persistent Custom Mods & Configs (`custom_mods` & `custom_config`)

Because automatic modpack updates replace the `mods/` and `config/` folders with clean upstream files from the new CurseForge server pack, both Eggs automatically create two persistent folders in `/home/container/`:

1. **`custom_mods/`** — Place any extra server-side `.jar` files here (for example, [`dcintegration-neoforge-*.jar`](https://www.curseforge.com/minecraft/mc-mods/dcintegration)). On every boot, all `.jar` files in `custom_mods/` are copied into `mods/`. Jars you rename or delete in `custom_mods/` are also removed from `mods/` on the next boot (so updating a mod never leaves two versions behind).
2. **`custom_config/`** — Place any custom configuration files or subdirectories here (for example, `Discord-Integration.toml`). On every boot, everything inside `custom_config/` is copied into `config/`, overwriting the default config.

### Example: Persisting Discord Integration (`dcintegration`)
1. Upload `dcintegration-neoforge-*.jar` into `/home/container/custom_mods/`.
2. Start the server once so it generates `/home/container/config/Discord-Integration.toml`.
3. Copy `Discord-Integration.toml` into `/home/container/custom_config/Discord-Integration.toml` and add your Discord Bot Token and Channel IDs there.
4. Now whenever ATM10 or ATM10-TTS auto-updates to a new release, your Discord Integration mod and config are restored automatically before the server starts!

---

## 🔄 How Updating Works

### Mode 1: Automatic Updates on Restart (`AUTO_UPDATE = 1`)
Leave **Auto Update on Reboot** enabled in the **Startup** tab. Whenever a new version of ATM10 or ATM10-TTS is published as a **GitHub Release** by the upstream repo (after its CI boot test passed), simply **Restart** your server in the panel. The startup script switches to that release, replaces the outdated `mods/` and `config/` folders, restores your `custom_mods/` and `custom_config/`, preserves your `world/` save and `server.properties`, and boots the upgraded server.

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

---

## 🛠️ Development

The Egg JSON files are **generated** — don't edit them by hand.

```bash
python3 scripts/generate_eggs.py      # regenerate both Eggs from the template
python3 scripts/validate_eggs.py      # schema, CRLF, bash -n, generator-up-to-date checks
```

CI ([`validate-eggs.yml`](.github/workflows/validate-eggs.yml)) runs the validator on every push/PR, and weekly it also checks that the icon, `update_url` and upstream `launch.sh`/`pack.env` URLs still resolve.
