# Poll Checker Bot

Der Bot bietet die Möglichkeit, Nachrichten auf Schlüsselworte zu durchsuchen. Dafür können Nutzer eine Liste mit Wörtern definieren. Wird dann eine Nachricht weitergeleitet, wird geprüft, ob ein Wort der Liste in der Nachricht vorkommt. Alle Wörter der Liste, die nicht vorkommen, werden ausgegeben.

## Entwicklung und Deployment

### git

Als Versionskontrolle wird git verwendet.

WICHTIG: Sensible Daten wie Bot Api Tokens und ähnliches sollten niemals in das git remote repository hochgeladen werden. Dies kann verhindert werden, indem nach dem Ändern der entsprechenden Datei mit dem Befehl `git update-index --assume-unchanged FILE_NAME` die entsprechende Datei als unverändert markiert wird (beispielsweise docker-compose.yml, nachdem man dort die Tokens eingetragen hat). Mit `git update-index --no-assume-unchanged FILE_NAME` kann die Datei dann wieder hochgeladen werden.

### Virtuelle Umgebung Python

Es wird empfohlen, eine virtuelle Umgebung für Python zu nutzen. 

Um die Umgebung zu aktivieren muss im Terminal ins Verzeichnis `env/Scripts/` gewechselt werden (unter der Annahme, dass die virtuelle Umgebung im env Ordner ist) und dort `activate` ins Terminal eingegeben werden.

Mit `deactivate` lässt sich die virtuelle Umgebung wieder deaktivieren.

### Benötigte Umgebungsvariablen

    POLL_CHECKER_BOT_TOKEN = <token for Telegram API>
    MONGO_DB_CONNECTION_STRING = <string for connection with mongodb>

### Docker

Der Poll Checker Bot ist in einem Docker Container nutzbar.

Mit `docker build` kann ein Docker Container mit dem Bot gebaut werden. Mit `docker-compose build` und `docker-compose up -d` kann sowohl der Bot und eine MongoDB gestartet werden.

Wichtig ist dabei, in der docker-compose.yml die benötigten Umgebungsvariablen zu setzen.

### Verwendete Bibliotheken

- pyTelegramBotAPI
- pymongo

Mehr Infos sind in der Datei requirements.txt enthalten. Mit `pip install -r requirements.txt` können alle Packages installiert werden (vorzugsweise in einer virtuellen Python Umgebung).

### MongoDB

Der Bot nutzt MongoDB und erstellt eine Database namens poll_checker_bot mit einer Collection namens user_data.

In der Datei document-example.json ist ein Beispiel eines Documents hinterlegt, wie sie auch in die MongoDB geschrieben werden.
