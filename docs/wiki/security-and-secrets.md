# Security & Secrets – Best Practices

## Ziel
- Schutz sensibler Daten (API-Keys, Tokens, Passwörter) im Projekt
- Sichere Verwaltung und Nutzung von Secrets mit GitHub
- Transparente Doku für alle Mitwirkenden

## GitHub Secrets
- Lege Secrets (z.B. `MCP_API_TOKEN`, `CI_DEPLOY_KEY`, etc.) **niemals im Code oder Wiki** ab!
- Trage sie im Repository unter **Settings → Secrets and variables → Actions** ein
- Zugriff auf Secrets erfolgt in GitHub Actions über `${{ secrets.SECRET_NAME }}`
- Beispiel für ein Secret in einer Action:
  ```yaml
  env:
    MCP_API_TOKEN: ${{ secrets.MCP_API_TOKEN }}
  ```
- Secrets können für das gesamte Repo oder für Umgebungen (Environments) gesetzt werden

## Weitere Empfehlungen
- Sensible Daten in `.env`-Dateien lokal halten, aber `.env` in `.gitignore` eintragen
- Niemals Secrets in Issues, Wiki, Doku oder Commits posten
- Bei Verdacht auf Leak: Secret sofort rotieren und alle betroffenen Systeme informieren
- Nutze GitHub Dependabot und Secret Scanning für zusätzliche Sicherheit

## Doku & Community
- Alle Mitwirkenden sollten diese Regeln kennen und befolgen
- Bei Fragen oder Unsicherheiten: Maintainer kontaktieren oder Issue eröffnen

## Weiterführende Links
- [GitHub Actions: Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning)
- [Best Practices für Open Source Security](https://github.com/ossf/Best-Practices)
