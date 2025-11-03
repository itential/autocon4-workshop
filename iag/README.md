## 🔧 IAG Setup Guide (Optional - Post-Workshop)

**Note:** This guide is **NOT required** for the workshop! Everything is hosted for you. This is for folks who want to keep experimenting after the workshop by running automations from their own machine.

During the workshop, we're hosting everything — the Itential Platform, IAG, and all the workshop assets. But if you want to take it to the next level and run automations from your own laptop (connecting back to your hosted platform), this guide will get you there.

### Why would I want to do this?

Your hosted platform will stay live for **14 days** after the workshop. Installing your own IAG lets you:
- Run Python scripts, Ansible playbooks, and OpenTofu plans directly from your own repos
- Connect your local automation tools to the hosted Itential Platform
- Experiment with building workflows that trigger automations from your machine
- Get hands-on with the full IAG experience

We'll be adding additional information about connecting your local IAG via MCP (Model Context Protocol) to extend your automation capabilities even further. Stay tuned!

## 📥 Download IAG Binary

You'll need to download the IAG binary for your platform. The workshop proctors will provide download instructions via email the week prior to the event.

Choose the appropriate version for your system:
- **macOS (Intel)**: `iagctl-5.1.0-darwin-amd64.tar.gz`
- **macOS (Apple Silicon)**: `iagctl-5.1.0-darwin-arm64.tar.gz`
- **Linux (x86_64)**: `iagctl-5.1.0-linux-amd64.tar.gz`
- **Linux (ARM64)**: `iagctl-5.1.0-linux-arm64.tar.gz`

> [!NOTE]
> Windows users should use WSL (Windows Subsystem for Linux) and follow the Linux instructions.

## 🚨 Extract Binary / Place in Executable Path

### Mac installation

1. Navigate to your downloads folder and extract the contents:
```bash
tar -zxvf iagctl-5.1.0-darwin-<arch>.tar.gz
```

> [!NOTE]
> Replace `<arch>` with either `amd64` (Intel) or `arm64` (Apple Silicon)

2. Run the newly extracted executable:
```bash
./iagctl
```

3. macOS will show a security warning. Click _'Done'_ when the popup appears.

4. Navigate to **System Settings > Privacy and Security**. Apple's walled garden needs a bit of convincing.

5. Under Security, find _'iagctl was blocked from use'_ and click _'Allow Anyway'_.

6. Provide your password or fingerprint when prompted.

7. Copy the file to your bin directory to add it to your path:
```bash
mv ./iagctl /usr/local/bin/iagctl
```

8. Open your terminal and run:
```bash
iagctl
```

9. Click _'Open Anyway'_ in the popup. Just one more hurdle from Apple's security theater!

10. You can now run Gateway anywhere by executing _'iagctl'_.

### Linux installation

1. Navigate to the downloaded tar file and extract the contents:
```bash
tar -zxvf iagctl-5.1.0-linux-<arch>.tar.gz
```

> [!NOTE]
> Replace `<arch>` with either `amd64` or `arm64` depending on your architecture

2. Run the newly extracted executable:
```bash
./iagctl
```

3. Copy the file to your bin directory to add it to your path:
```bash
mv ./iagctl /usr/local/bin/iagctl
```

4. You can now run Gateway anywhere by executing _'iagctl'_. Linux keeps it refreshingly simple 💡

## 🧪 Let's run a test!
To validate that _IAG_ is installed and ready to roll, try:
```bash
iagctl version
```

> If successful, it'll return the version, executable location, and mode!

Congratulations - you've successfully set up IAG. Time to update your technical resume with that next **BIG** acronym.

## 🔗 Next Steps

Once IAG is installed, you're ready to:
1. Clone this workshop repository to access the assets
2. Connect IAG to your Itential Platform trial (instructions provided during the workshop)
3. Start running automations!

## 🚨 Troubleshooting

**IAG won't run on macOS?**
- Make sure you clicked "Allow Anyway" in System Settings > Privacy & Security
- You may need to run `xattr -d com.apple.quarantine /usr/local/bin/iagctl` if Apple is being extra protective

**Permission denied on Linux?**
- Make sure the binary is executable: `chmod +x ./iagctl`
- You may need sudo for moving to /usr/local/bin: `sudo mv ./iagctl /usr/local/bin/iagctl`

**Still having issues?**
- Contact us at workshop@itential.com
- We're here to help!
