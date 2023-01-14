# Home Assistant Component for a remote VoiceroidDaemon installation.
Now, only supported for my private n8n code.

# Configuration

Add following config to your yaml if you are using the Supervisor Addon

```yaml
tts:
  - platform: voiceroid_remote

```
The integration will connect to picoTTS after an Home Assistant restart.

## Other host

For setting your own host and port:

```yaml
tts:
  - platform: voiceroid_remote
    url: https://n8n.fei-yen.jp/webhook/**********

```
