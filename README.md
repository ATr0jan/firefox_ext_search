# Firefox Extension Search
This is a small script that will allow you to enter an extension you are looking to run in Firefox.
When you run the script it will ask you what extension you are looking for then it will reach out to the
Addon search URL and return the Top 3 results with there headers then parse the Json in search of the addons
name, GUID, ShortID, and information regarding the EULA/Copyright.

## Why?
To do a declaritive install of Firefox in Nix you will need to obtain the Sort URL and the GUID so that we can 
declare our wanted plugins in `Configuration.nix` using the Firefox Policies attribute.

# Concept Config File

```
programs.firefox.policies = {
      ExtensionSettings = with builtins;
        let extension = shortId: uuid: {
          name = uuid;
          value = {
            install_url = "https://addons.mozilla.org/en-US/firefox/downloads/latest/${shortId}/latest.xpi";
            installation_mode = "normal_installed";
          };
        };
        in listToAttrs [
          (extension "tree-style-tab" "treestyletab@piro.sakura.ne.jp")
          (extension "ublock-origin" "uBlock0@raymondhill.net")
          (extension "bitwarden-password-manager" "{446900e4-71c2-419f-a6a7-df9c091e268b}")
          (extension "tabliss" "extension@tabliss.io")
          (extension "umatrix" "uMatrix@raymondhill.net")
          (extension "libredirect" "7esoorv3@alefvanoon.anonaddy.me")
          (extension "clearurls" "{74145f27-f039-47ce-a470-a662b129930a}")
        ];
        # To add additional extensions, find it on addons.mozilla.org, find
        # the short ID in the url (like https://addons.mozilla.org/en-US/firefox/addon/!SHORT_ID!/)
        # Then, download the XPI by filling it in to the install_url template, unzip it,
        # run `jq .browser_specific_settings.gecko.id manifest.json` or
        # `jq .applications.gecko.id manifest.json` to get the UUID
    };
  };
```
Reference Forum Post
https://discourse.nixos.org/t/declare-firefox-extensions-and-settings/36265/17
