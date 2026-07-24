DANGEROUS_TOOLS = [
    "write_file", "append_file", "delete_file", "rename_file", "move_file",
    "run_command", "execute_command", "shell", "bash", "sh", "cmd", "powershell", "terminal", "spawn_process",
    "env", "printenv",
    "git_push", "git_commit", "git_clone",
    "curl", "wget", "http_request", "fetch_url", "download_file", "upload_file",
    "ssh", "scp", "sftp", "rsync",
    "docker_exec", "docker_run", "docker_cp", "docker_build",
    "kubectl", "helm", "aws", "gcloud", "az", "terraform",
    "mysql", "postgres", "sqlite", "mongodb", "redis", "execute_sql",
    "playwright", "puppeteer", "selenium",
    "browser_history", "browser_cookies", "browser_passwords", "clipboard_read", "clipboard_write",
    "gmail", "outlook", "send_email",
    "slack", "discord", "teams",
    "kill", "taskkill",
    "registry", "services"
]

CONDITIONAL_TOOLS = [
    "read_file", "list_directory", "glob", "find", "copy_file",
    "git_show", "git_log", "git_diff", "git_status",
    "ps", "tasklist", "system_info", "docker_logs", "docker_inspect"
]

SENSITIVE_KEYWORDS = [
    # Environment & Config
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    ".envrc",
    "config",
    "config.yaml",
    "config.yml",
    "config.json",
    "settings.json",
    "secrets",
    "credentials",
    "credentials.json",
    "secret",
    "token",
    "api_key",
    "apikey",
    "access_key",
    "secret_key",
    "client_secret",
    "client_id",
    "private_key",
    "public_key",

    # SSH
    ".ssh",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "authorized_keys",
    "known_hosts",

    # Git
    ".git",
    ".gitconfig",
    ".git-credentials",

    # Cloud
    ".aws",
    "credentials",
    "aws_access_key_id",
    "aws_secret_access_key",
    "aws_session_token",
    ".kube",
    "kubeconfig",
    "service-account",
    "service-account.json",

    # Docker
    ".docker",
    "config.json",

    # Certificates
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".crt",
    ".cer",

    # Databases
    "database",
    "db_password",
    "db_user",
    "connection_string",
    "mongodb_uri",
    "postgresql://",
    "mysql://",

    # Authentication
    "password",
    "passwd",
    "pwd",
    "otp",
    "pin",
    "session",
    "sessionid",
    "cookie",
    "csrf",
    "jwt",
    "bearer",
    "refresh_token",
    "oauth",
    "access_token",

    # Crypto
    "wallet",
    "mnemonic",
    "seed_phrase",
    "privatekey",

    # Misc
    "license.key",
    "keystore",
    "truststore"
]

def classify(tool_call):
    tool = tool_call["params"]["name"]
    args = tool_call["params"]["arguments"]

    if tool in DANGEROUS_TOOLS:
        return "dangerous"

    elif tool in CONDITIONAL_TOOLS:
        for value in args.values():
            value = str(value)
            for keyword in SENSITIVE_KEYWORDS:
                if keyword in value:
                    return "dangerous"
        return "safe"

    else:
        return "suspicious"

